import re

def preprocess_text(text):
    """
    Cleans extracted text to prepare for AI evaluation.
    Removes excessive whitespace and non-standard characters.
    """
    if not text:
        return ""
    
    # Remove excessive newlines
    text = re.sub(r'\n+', '\n', text)
    # Remove excessive spaces
    text = re.sub(r' +', ' ', text)
    # Strip leading/trailing whitespace
    return text.strip()
