import os
import shutil
import magic
import mimetypes
import uuid
import logging
import gzip
import brotli
from datetime import datetime, timedelta
from typing import Optional, List, Dict

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel
from dotenv import load_dotenv

from backend.utils.utils_image import optimize_image_webp, compare_images
from backend.utils.utils_pdf import optimize_pdf, compare_pdfs
from backend.utils.utils_video import optimize_video, compare_videos
from backend.compare_utils import get_file_type, calculate_compression_ratio
from backend.nlp_utils import detect_sensitive_entities
from backend.diff_utils import create_diff_patch, apply_diff_patch
from backend.office_optimize import optimize_office_document
from backend.utils_ai_selector import ai_select_compression_method
from backend.cleanup import cleanup_old_files

# Load environment variables
load_dotenv()

# --- Configuration ---
API_KEYS = os.getenv("API_KEYS", "demo-key-123").split(',')
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", 5))
TEMP_DIR = os.getenv("TEMP_DIR", "./tmp")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tmp/results_db.sqlite3")
CLEANUP_INTERVAL_HOURS = int(os.getenv("CLEANUP_INTERVAL_HOURS", 24))
FILE_LIFESPAN_HOURS = int(os.getenv("FILE_LIFESPAN_HOURS", 48))

# Ensure temp directories exist
UPLOAD_DIR = os.path.join(TEMP_DIR, "uploads")
DOWNLOAD_DIR = os.path.join(TEMP_DIR, "downloads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# --- Database Setup ---
Base = declarative_base()

class FileMetadata(Base):
    __tablename__ = "file_metadata"
    id = Column(String, primary_key=True, index=True)
    original_filename = Column(String)
    compressed_filename = Column(String, nullable=True)
    mime_type = Column(String)
    size_before = Column(Integer)
    size_after = Column(Integer, nullable=True)
    compression_method = Column(String, nullable=True)
    ratio = Column(Float, nullable=True)
    elapsed_time = Column(Float, nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    sensitive_entities_detected = Column(Boolean, default=False)
    sensitive_entities_summary = Column(Text, nullable=True)
    decompression_time_ms = Column(Float, nullable=True)
    diff_summary = Column(Text, nullable=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- FastAPI App Setup ---
app = FastAPI(
    title="Compressio Backend",
    description="Compressio is compression and optimization API with AI selection.",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key Authentication
api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key

# --- Helper Functions ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def save_upload_file(upload_file: UploadFile) -> str:
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id + "_" + upload_file.filename)
    
    # Check file size
    if upload_file.size > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds the maximum limit of {MAX_UPLOAD_SIZE_MB}MB."
        )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path, file_id

def get_file_path(file_id: str, is_original: bool = True) -> Optional[str]:
    db = SessionLocal()
    metadata = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()
    db.close()
    if not metadata:
        return None
    
    if is_original:
        return os.path.join(UPLOAD_DIR, f"{file_id}_{metadata.original_filename}")
    else:
        return os.path.join(DOWNLOAD_DIR, metadata.compressed_filename) if metadata.compressed_filename else None

# --- API Endpoints ---

@app.get("/health", summary="Health check endpoint")
async def health_check():
    return {"status": "ok", "message": "Compressio backend is running."}

@app.get("/info", summary="Get build and version information")
async def get_info():
    return {
        "app_name": app.title,
        "version": app.version,
        "description": app.description,
        "max_upload_size_mb": MAX_UPLOAD_SIZE_MB,
        "cleanup_interval_hours": CLEANUP_INTERVAL_HOURS,
        "file_lifespan_hours": FILE_LIFESPAN_HOURS,
        "upload_dir": UPLOAD_DIR,
        "download_dir": DOWNLOAD_DIR,
    }

@app.post("/upload", summary="Upload a file for compression", response_model=Dict[str, str])
async def upload_file(
    file: UploadFile = File(...), 
    db: SessionLocal = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    try:
        file_path, file_id = await save_upload_file(file)
        mime_type = magic.Magic(mime=True).from_file(file_path)
        
        new_metadata = FileMetadata(
            id=file_id,
            original_filename=file.filename,
            mime_type=mime_type,
            size_before=file.size,
            upload_time=datetime.utcnow(),
            last_accessed=datetime.utcnow()
        )
        db.add(new_metadata)
        db.commit()
        db.refresh(new_metadata)
        
        return JSONResponse(content={
            "id": file_id,
            "filename": file.filename,
            "mime_type": mime_type,
            "size": file.size
        }, status_code=status.HTTP_202_ACCEPTED) # Accepted for processing
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Upload failed: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to upload file: {str(e)}")

@app.post("/compress", summary="Compress an uploaded file")
async def compress_file(
    file_id: str = Form(...), 
    method: str = Form(...), # e.g., 'gzip', 'brotli', 'webp', 'pdf_optimize', 'ai'
    profile: Optional[str] = Form(None), # e.g., 'web', 'archive', 'network', 'default'
    sensitive_mode: Optional[bool] = Form(False),
    db: SessionLocal = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    db_file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

    original_file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{db_file.original_filename}")
    if not os.path.exists(original_file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Original file not found on disk.")

    file_type = get_file_type(db_file.mime_type)
    optimized_file_path = None
    compression_method_used = method
    start_time = datetime.now()
    sensitive_entities_detected = False
    sensitive_entities_summary = None

    try:
        if method == "ai":
            # AI selects the best method and profile
            selected_method, selected_profile = ai_select_compression_method(
                original_file_path, db_file.mime_type, profile
            )
            compression_method_used = selected_method
            profile = selected_profile # Update profile for further processing if needed
            logging.info(f"AI selected method: {compression_method_used} with profile: {profile}")

        if compression_method_used == "webp" and file_type == "image":
            optimized_filename = f"compressed_{file_id}_{os.path.splitext(db_file.original_filename)[0]}.webp"
            optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
            optimize_image_webp(original_file_path, optimized_file_path, quality=80) # Default quality
        elif compression_method_used == "pdf_optimize" and file_type == "pdf":
            optimized_filename = f"compressed_{file_id}_{db_file.original_filename}"
            optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
            optimize_pdf(original_file_path, optimized_file_path)
        elif compression_method_used == "gzip":
            optimized_filename = f"compressed_{file_id}_{db_file.original_filename}.gz"
            optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
            with open(original_file_path, 'rb') as f_in:
                with gzip.open(optimized_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        elif compression_method_used == "brotli":
            optimized_filename = f"compressed_{file_id}_{db_file.original_filename}.br"
            optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
            with open(original_file_path, 'rb') as f_in:
                compressed_data = brotli.compress(f_in.read())
                with open(optimized_file_path, 'wb') as f_out:
                    f_out.write(compressed_data)
        elif compression_method_used == "office_optimize" and file_type == "document":
            optimized_filename = f"compressed_{file_id}_{db_file.original_filename}"
            optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
            optimize_office_document(original_file_path, optimized_file_path)
        elif compression_method_used == "video_optimize" and file_type == "video":
            optimized_filename = f"compressed_{file_id}_{os.path.splitext(db_file.original_filename)[0]}.mp4"
            optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
            optimize_video(original_file_path, optimized_file_path, crf=28) # Default CRF
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported compression method for {file_type} files: {compression_method_used}")

        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()

        size_after = os.path.getsize(optimized_file_path) if optimized_file_path and os.path.exists(optimized_file_path) else db_file.size_before
        ratio = calculate_compression_ratio(db_file.size_before, size_after)

        # Sensitive entity detection for text-based files
        if sensitive_mode and file_type == "text":
            try:
                with open(original_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                entities = detect_sensitive_entities(content)
                if entities:
                    sensitive_entities_detected = True
                    sensitive_entities_summary = ", ".join([f"{ent.text} ({ent.label_})" for ent in entities])
            except Exception as e:
                logging.warning(f"Sensitive entity detection failed for {file_id}: {e}")

        db_file.compressed_filename = optimized_filename
        db_file.size_after = size_after
        db_file.compression_method = compression_method_used
        db_file.ratio = ratio
        db_file.elapsed_time = elapsed_time
        db_file.last_accessed = datetime.utcnow()
        db_file.sensitive_entities_detected = sensitive_entities_detected
        db_file.sensitive_entities_summary = sensitive_entities_summary
        db.commit()
        db.refresh(db_file)

        return JSONResponse(content={
            "id": db_file.id,
            "size_before": db_file.size_before,
            "size_after": db_file.size_after,
            "method": db_file.compression_method,
            "elapsed": db_file.elapsed_time,
            "ratio": db_file.ratio,
            "sensitive_entities_detected": db_file.sensitive_entities_detected,
            "sensitive_entities_summary": db_file.sensitive_entities_summary,
        }, status_code=status.HTTP_200_OK)

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Compression failed for {file_id} with method {method}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Compression failed: {str(e)}")

@app.get("/result/{file_id}", summary="Get compression result metadata")
async def get_compression_result(
    file_id: str, 
    db: SessionLocal = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    db_file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
    
    db_file.last_accessed = datetime.utcnow()
    db.commit()
    db.refresh(db_file)

    download_url = f"/download/{file_id}" if db_file.compressed_filename else None

    return {
        "id": db_file.id,
        "original_filename": db_file.original_filename,
        "compressed_filename": db_file.compressed_filename,
        "mime_type": db_file.mime_type,
        "size_before": db_file.size_before,
        "size_after": db_file.size_after,
        "compression_method": db_file.compression_method,
        "ratio": db_file.ratio,
        "elapsed": db_file.elapsed_time,
        "upload_time": db_file.upload_time.isoformat(),
        "last_accessed": db_file.last_accessed.isoformat(),
        "download_url": download_url,
        "sensitive_entities_detected": db_file.sensitive_entities_detected,
        "sensitive_entities_summary": db_file.sensitive_entities_summary,
    }

@app.get("/download/{file_id}", summary="Download compressed or original file")
async def download_file(
    file_id: str, 
    original: bool = False, # Set to True to download original file
    db: SessionLocal = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    db_file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

    file_path = None
    filename_to_serve = ""
    
    if original:
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{db_file.original_filename}")
        filename_to_serve = db_file.original_filename
    elif db_file.compressed_filename:
        file_path = os.path.join(DOWNLOAD_DIR, db_file.compressed_filename)
        filename_to_serve = db_file.compressed_filename
    
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found on server.")
    
    db_file.last_accessed = datetime.utcnow()
    db.commit()
    
    return FileResponse(
        path=file_path,
        filename=filename_to_serve,
        media_type=mimetypes.guess_type(filename_to_serve)[0] or "application/octet-stream"
    )

@app.get("/compare/{file_id}", summary="Get comparison statistics, ratio, previews, and diff")
async def compare_files(
    file_id: str,
    db: SessionLocal = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    db_file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

    original_file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{db_file.original_filename}")
    compressed_file_path = os.path.join(DOWNLOAD_DIR, db_file.compressed_filename) if db_file.compressed_filename else None

    if not os.path.exists(original_file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Original file not found on disk.")
    if compressed_file_path and not os.path.exists(compressed_file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compressed file not found on disk.")

    file_type = get_file_type(db_file.mime_type)
    preview_before = None
    preview_after = None
    diff_summary = "N/A"
    decompression_time_ms = None

    try:
        # Generate previews (as base64 PNG)
        # preview_before = create_image_preview(original_file_path, file_type)
        if compressed_file_path:
            # preview_after = create_image_preview(compressed_file_path, file_type)
            pass

        # Compare files and get diff summary/decompression time
        if file_type == "image" and compressed_file_path:
            # For images, compare_images also provides a simple diff summary based on PSNR/SSIM
            similarity, psnr, ssim = compare_images(original_file_path, compressed_file_path)
            diff_summary = f"Image similarity (SSIM): {ssim:.2f}, PSNR: {psnr:.2f} dB"
            # Simulate decompression time for images
            decompression_time_ms = 5 + (db_file.size_after / 1024) * 0.01 # Example simulation
        elif file_type == "pdf" and compressed_file_path:
            # compare_pdfs provides a textual diff summary if applicable, and simulates decompression
            diff_summary, simulated_decompress_time = compare_pdfs(original_file_path, compressed_file_path)
            decompression_time_ms = simulated_decompress_time
        elif file_type == "document" and compressed_file_path:
            # Placeholder for document comparison if needed
            diff_summary = "Document comparison not implemented yet."
            decompression_time_ms = 10 + (db_file.size_after / 1024) * 0.02 # Example simulation
        elif file_type == "video" and compressed_file_path:
            diff_summary = "Video comparison not directly supported via diff. Visual inspection via preview."
            decompression_time_ms = 20 + (db_file.size_after / 1024) * 0.05 # Example simulation
        elif compressed_file_path: # Generic binary/text comparison
            original_content = open(original_file_path, 'rb').read()
            compressed_content = open(compressed_file_path, 'rb').read()
            # Simple check for identical content for diff summary
            if original_content == compressed_content:
                diff_summary = "Files are identical after compression (no visible change)."
            else:
                diff_summary = "Files are different. Use specialized tools for detailed diff."
            decompression_time_ms = 1 + (db_file.size_after / 1024) * 0.005 # Example simulation


        db_file.decompression_time_ms = decompression_time_ms
        db_file.diff_summary = diff_summary
        db_file.last_accessed = datetime.utcnow()
        db.commit()
        db.refresh(db_file)

        return {
            "id": db_file.id,
            "original_filename": db_file.original_filename,
            "compressed_filename": db_file.compressed_filename,
            "size_before": db_file.size_before,
            "size_after": db_file.size_after,
            "ratio": db_file.ratio,
            "elapsed": db_file.elapsed_time,
            "compression_method": db_file.compression_method,
            "decompression_time_ms": db_file.decompression_time_ms,
            "diff_summary": db_file.diff_summary,
            "preview_before": preview_before,
            "preview_after": preview_after,
            "sensitive_entities_detected": db_file.sensitive_entities_detected,
            "sensitive_entities_summary": db_file.sensitive_entities_summary,
        }

    except Exception as e:
        logging.error(f"Comparison failed for {file_id}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to compare files: {str(e)}")

@app.post("/batch_compress", summary="Compress multiple files in a batch")
async def batch_compress(
    items: List[Dict[str, str]], # [{"file_id": "...", "method": "...", "profile": "...", "sensitive_mode": true/false}]
    db: SessionLocal = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    results = []
    for item in items:
        file_id = item.get("file_id")
        method = item.get("method")
        profile = item.get("profile")
        sensitive_mode = item.get("sensitive_mode", False)
        
        if not file_id or not method:
            results.append({"file_id": file_id, "status": "failed", "detail": "Missing file_id or method."})
            continue
            
        try:
            # Directly call the compress_file logic (or refactor it to a shared function)
            # For simplicity, we'll re-use the logic from compress_file
            db_file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()
            if not db_file:
                results.append({"file_id": file_id, "status": "failed", "detail": "File not found."})
                continue
            
            original_file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{db_file.original_filename}")
            if not os.path.exists(original_file_path):
                results.append({"file_id": file_id, "status": "failed", "detail": "Original file not found on disk."})
                continue

            file_type = get_file_type(db_file.mime_type)
            optimized_file_path = None
            compression_method_used = method
            start_time = datetime.now()
            sensitive_entities_detected = False
            sensitive_entities_summary = None

            if method == "ai":
                selected_method, selected_profile = ai_select_compression_method(original_file_path, db_file.mime_type, profile)
                compression_method_used = selected_method
                profile = selected_profile
            
            # ... (compression logic as in compress_file) ...
            if compression_method_used == "webp" and file_type == "image":
                optimized_filename = f"compressed_{file_id}_{os.path.splitext(db_file.original_filename)[0]}.webp"
                optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
                optimize_image_webp(original_file_path, optimized_file_path, quality=80)
            elif compression_method_used == "pdf_optimize" and file_type == "pdf":
                optimized_filename = f"compressed_{file_id}_{db_file.original_filename}"
                optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
                optimize_pdf(original_file_path, optimized_file_path)
            elif compression_method_used == "gzip":
                optimized_filename = f"compressed_{file_id}_{db_file.original_filename}.gz"
                optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
                with open(original_file_path, 'rb') as f_in:
                    with gzip.open(optimized_file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            elif compression_method_used == "brotli":
                optimized_filename = f"compressed_{file_id}_{db_file.original_filename}.br"
                optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
                with open(original_file_path, 'rb') as f_in:
                    compressed_data = brotli.compress(f_in.read())
                    with open(optimized_file_path, 'wb') as f_out:
                        f_out.write(compressed_data)
            elif compression_method_used == "office_optimize" and file_type == "document":
                optimized_filename = f"compressed_{file_id}_{db_file.original_filename}"
                optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
                optimize_office_document(original_file_path, optimized_file_path)
            elif compression_method_used == "video_optimize" and file_type == "video":
                optimized_filename = f"compressed_{file_id}_{os.path.splitext(db_file.original_filename)[0]}.mp4"
                optimized_file_path = os.path.join(DOWNLOAD_DIR, optimized_filename)
                optimize_video(original_file_path, optimized_file_path, crf=28)
            else:
                results.append({"file_id": file_id, "status": "failed", "detail": f"Unsupported compression method for {file_type} files: {compression_method_used}"})
                continue

            end_time = datetime.now()
            elapsed_time = (end_time - start_time).total_seconds()

            size_after = os.path.getsize(optimized_file_path) if optimized_file_path and os.path.exists(optimized_file_path) else db_file.size_before
            ratio = calculate_compression_ratio(db_file.size_before, size_after)

            if sensitive_mode and file_type == "text":
                try:
                    with open(original_file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    entities = detect_sensitive_entities(content)
                    if entities:
                        sensitive_entities_detected = True
                        sensitive_entities_summary = ", ".join([f"{ent.text} ({ent.label_})" for ent in entities])
                except Exception as e:
                    logging.warning(f"Sensitive entity detection failed for {file_id} in batch: {e}")

            db_file.compressed_filename = optimized_filename
            db_file.size_after = size_after
            db_file.compression_method = compression_method_used
            db_file.ratio = ratio
            db_file.elapsed_time = elapsed_time
            db_file.last_accessed = datetime.utcnow()
            db_file.sensitive_entities_detected = sensitive_entities_detected
            db_file.sensitive_entities_summary = sensitive_entities_summary
            db.commit()
            db.refresh(db_file)
            
            results.append({
                "file_id": file_id,
                "status": "success",
                "size_before": db_file.size_before,
                "size_after": db_file.size_after,
                "method": db_file.compression_method,
                "elapsed": db_file.elapsed_time,
                "ratio": db_file.ratio,
            })
        except Exception as e:
            logging.error(f"Batch compression failed for {file_id}: {e}", exc_info=True)
            results.append({"file_id": file_id, "status": "failed", "detail": str(e)})
            
    return JSONResponse(content={"results": results}, status_code=status.HTTP_200_OK)

@app.post("/diff_compress", summary="Create or apply a differential compression patch")
async def diff_compress(
    file_id: str = Form(..., description="ID of the target file (new version for patch, base for restore)"),
    base_file_id: Optional[str] = Form(None, description="ID of the base file (original version for patch, existing for restore)"),
    method: str = Form(..., description="'patch' to create a diff, 'restore' to apply a diff"),
    patch_file_id: Optional[str] = Form(None, description="ID of the patch file to apply (required for method='restore')"),
    db: SessionLocal = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    if method not in ["patch", "restore"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Method must be 'patch' or 'restore'.")

    if method == "patch":
        if not base_file_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="base_file_id is required for 'patch' method.")
        
        target_file_meta = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()
        base_file_meta = db.query(FileMetadata).filter(FileMetadata.id == base_file_id).first()

        if not target_file_meta or not base_file_meta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target or base file not found.")

        target_path = os.path.join(UPLOAD_DIR, f"{file_id}_{target_file_meta.original_filename}")
        base_path = os.path.join(UPLOAD_DIR, f"{base_file_id}_{base_file_meta.original_filename}")

        if not os.path.exists(target_path) or not os.path.exists(base_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target or base file not found on disk.")
        
        patch_data = create_diff_patch(base_path, target_path)
        
        patch_filename = f"patch_{base_file_id}_{file_id}.bin"
        patch_file_path = os.path.join(DOWNLOAD_DIR, patch_filename)
        with open(patch_file_path, 'wb') as f:
            f.write(patch_data)
        
        # Store patch metadata (optional, could be a new table or just return info)
        # For simplicity, we'll just return the patch info
        return JSONResponse(content={
            "status": "success",
            "message": "Patch created successfully.",
            "patch_filename": patch_filename,
            "patch_size": len(patch_data),
            "download_url": f"/download/{patch_filename}" # This needs to be handled differently as it's not a file_id
        })

    elif method == "restore":
        if not patch_file_id or not base_file_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="patch_file_id and base_file_id are required for 'restore' method.")

        base_file_meta = db.query(FileMetadata).filter(FileMetadata.id == base_file_id).first()
        patch_file_path = os.path.join(DOWNLOAD_DIR, patch_file_id) # Assuming patch_file_id is the actual filename

        if not base_file_meta or not os.path.exists(patch_file_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Base file or patch file not found.")
        
        base_path = os.path.join(UPLOAD_DIR, f"{base_file_id}_{base_file_meta.original_filename}")
        if not os.path.exists(base_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Base file not found on disk.")

        output_filename = f"restored_{file_id}_{base_file_meta.original_filename}"
        output_path = os.path.join(DOWNLOAD_DIR, output_filename)
        
        apply_diff_patch(base_path, patch_file_path, output_path)
        
        # You might want to create a new FileMetadata entry for the restored file
        # For now, just return success
        return JSONResponse(content={
            "status": "success",
            "message": "File restored successfully.",
            "restored_filename": output_filename,
            "download_url": f"/download/{output_filename}" # This needs to be handled differently as it's not a file_id
        })

@app.get("/compression_methods", summary="List available compression methods")
async def get_compression_methods(api_key: str = Depends(get_api_key)):
    return {
        "methods": [
            {"name": "AI Selection", "value": "ai", "description": "Automatically selects the best compression method."},
            {"name": "Gzip", "value": "gzip", "description": "General purpose compression."},
            {"name": "Brotli", "value": "brotli", "description": "General purpose compression, often better than gzip."},
            {"name": "WebP (Image)", "value": "webp", "description": "Optimizes images to WebP format."},
            {"name": "PDF Optimize", "value": "pdf_optimize", "description": "Reduces PDF file size."},
            {"name": "Office Document Optimize", "value": "office_optimize", "description": "Optimizes Word, Excel, PowerPoint documents."},
            {"name": "Video Optimize", "value": "video_optimize", "description": "Optimizes video file size."},
        ]
    }

# --- Background Task for Cleanup ---
@app.on_event("startup")
async def start_cleanup_scheduler():
    from fastapi_utils.tasks import repeat_every
    
    @repeat_every(seconds=CLEANUP_INTERVAL_HOURS * 3600, raise_exceptions=True)
    async def periodic_cleanup():
        logging.info("Running periodic cleanup of old files and metadata...")
        cleanup_old_files(UPLOAD_DIR, DOWNLOAD_DIR, FILE_LIFESPAN_HOURS, SessionLocal)
        logging.info("Cleanup complete.")

    # Run cleanup immediately on startup for testing/initial state
    await periodic_cleanup()

# Example of how to integrate cleanup into the main app
# You might want to expose a manual trigger for cleanup or rely solely on the scheduler
@app.post("/trigger_cleanup", summary="Manually trigger cleanup of old files", tags=["Admin"])
async def trigger_cleanup_endpoint(api_key: str = Depends(get_api_key)):
    logging.info("Manual cleanup triggered.")
    cleanup_old_files(UPLOAD_DIR, DOWNLOAD_DIR, FILE_LIFESPAN_HOURS, SessionLocal)
    return {"message": "Cleanup process initiated. Check logs for details."}


if __name__ == "__main__":
    import uvicorn
    # Initialize the database on startup
    Base.metadata.create_all(engine)
    logging.basicConfig(level=logging.INFO) # Set logging level for local run
    uvicorn.run(app, host="0.0.0.0", port=8000)
