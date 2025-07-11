import os
import logging
from pypdf import PdfReader, PdfWriter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def optimize_pdf(input_path: str, output_path: str, compress_images: bool = True) -> str:
    """
    Optimizes a PDF file by re-saving it, potentially compressing images within it.
    This is a basic optimization that can reduce file size, especially if the original
    PDF was not well-optimized.
    """
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        if compress_images:
            # This implicitly tries to compress images when writing if supported by pypdf
            # For explicit image compression, you'd need a more advanced library or approach
            pass # pypdf handles some optimization on save

        with open(output_path, 'wb') as f_out:
            writer.write(f_out)
        
        logging.info(f"Optimized PDF: {input_path} -> {output_path}")
        return output_path

    except Exception as e:
        logging.error(f"Error optimizing PDF {input_path}: {e}", exc_info=True)
        raise

def compare_pdfs(pdf1_path: str, pdf2_path: str) -> tuple[str, float]:
    """
    Compares two PDF files (very basic: page count and text content diff for first page).
    Returns a summary string and simulated decompression time.
    """
    summary = "PDF Comparison: "
    simulated_decompress_time_ms = 50.0 # Base simulation time
    
    try:
        reader1 = PdfReader(pdf1_path)
        reader2 = PdfReader(pdf2_path)

        summary += f"Pages: {len(reader1.pages)} vs {len(reader2.pages)}. "

        # Basic text content comparison for the first page
        text1 = ""
        text2 = ""
        if len(reader1.pages) > 0:
            text1 = reader1.pages[0].extract_text() or ""
        if len(reader2.pages) > 0:
            text2 = reader2.pages[0].extract_text() or ""

        if text1 == text2:
            summary += "First page text content is identical."
        else:
            summary += "First page text content differs."

        # Simulate decompression time based on file size
        size_after = os.path.getsize(pdf2_path)
        simulated_decompress_time_ms += (size_after / 1024) * 0.05 # Add 0.05ms per KB

    except Exception as e:
        logging.warning(f"Error during PDF comparison for {pdf1_path} and {pdf2_path}: {e}")
        summary = f"PDF Comparison Error: {e}"

    return summary, simulated_decompress_time_ms

if __name__ == "__main__":
    # Example Usage (requires a dummy PDF file)
    # from pypdf import PdfWriter
    # writer = PdfWriter()
    # writer.add_blank_page(500, 700)
    # with open("dummy_input.pdf", "wb") as fp: writer.write(fp)

    input_pdf = "dummy_input.pdf"  # Replace with a real PDF file for testing
    output_pdf = "optimized_dummy_input.pdf"

    if os.path.exists(input_pdf):
        print(f"Optimizing {input_pdf}...")
        try:
            optimize_pdf(input_pdf, output_pdf)
            print(f"Original size: {os.path.getsize(input_pdf)} bytes")
            print(f"Optimized size: {os.path.getsize(output_pdf)} bytes")
            summary, decompress_time = compare_pdfs(input_pdf, output_pdf)
            print(f"Comparison Summary: {summary}")
            print(f"Simulated Decompression Time: {decompress_time:.2f} ms")
        except Exception as e:
            print(f"Optimization/comparison failed: {e}")
        finally:
            # Clean up generated files
            if os.path.exists(output_pdf):
                os.remove(output_pdf)
    else:
        print(f"Please create a dummy PDF file named '{input_pdf}' for testing.") 