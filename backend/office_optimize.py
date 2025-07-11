import os
import logging
from docx import Document
from pptx import Presentation
from openpyxl import load_workbook

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def optimize_office_document(input_path: str, output_path: str):
    """
    Optimizes MS Office documents (Word, Excel, PowerPoint) by removing extraneous data.
    Note: This is a basic optimization, primarily re-saving the file which can sometimes
    reduce size by cleaning up internal structures. More advanced optimization would require
    specific libraries for each format to remove embedded objects, metadata, etc.
    """
    file_extension = os.path.splitext(input_path)[1].lower()
    
    try:
        if file_extension == '.docx':
            doc = Document(input_path)
            doc.save(output_path)
            logging.info(f"Optimized Word document: {input_path} -> {output_path}")
        elif file_extension in ('.xlsx', '.xls'): # openpyxl only supports .xlsx
            if file_extension == '.xls':
                logging.warning("Old .xls format detected. Basic re-saving might not offer much optimization.")
                # For .xls, might need external tools like win32com on Windows or libreoffice-headless
                # For now, we'll just copy it as a placeholder for unsupported direct optimization
                os.link(input_path, output_path) if hasattr(os, 'link') else shutil.copy2(input_path, output_path)
            else: # .xlsx
                workbook = load_workbook(input_path)
                workbook.save(output_path)
                logging.info(f"Optimized Excel document: {input_path} -> {output_path}")
        elif file_extension in ('.pptx', '.ppt'): # python-pptx only supports .pptx
            if file_extension == '.ppt':
                logging.warning("Old .ppt format detected. Basic re-saving might not offer much optimization.")
                # For .ppt, similar to .xls, direct Python optimization is limited.
                os.link(input_path, output_path) if hasattr(os, 'link') else shutil.copy2(input_path, output_path)
            else: # .pptx
                presentation = Presentation(input_path)
                presentation.save(output_path)
                logging.info(f"Optimized PowerPoint document: {input_path} -> {output_path}")
        else:
            logging.warning(f"Unsupported Office document format for optimization: {file_extension}. Copying original.")
            os.link(input_path, output_path) if hasattr(os, 'link') else shutil.copy2(input_path, output_path)
            
        return output_path
    except Exception as e:
        logging.error(f"Error optimizing office document {input_path}: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    # Example Usage (requires dummy files)
    # Create dummy docx, xlsx, pptx files for testing
    print("This script provides basic Office document optimization. Create dummy files and call the function.")
    # Example:
    # from docx import Document
    # Document().save("test.docx")
    # optimize_office_document("test.docx", "optimized_test.docx") 