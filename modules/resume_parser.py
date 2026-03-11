import os
import pdfplumber
import docx

def parse_resume(file_path):
    """
    Extracts text from a given resume file (PDF, DOCX, TXT).
    """
    ext = file_path.rsplit('.', 1)[1].lower()
    text = ""
    
    try:
        if ext == 'pdf':
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif ext == 'docx':
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        elif ext == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
    except Exception as e:
        print(f"Error parsing resume {file_path}: {e}")
        
    return text
