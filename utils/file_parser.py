import docx2txt
import pdfplumber

def extract_text_from_file(path):
    ext = path.rsplit('.',1)[1].lower()
    if ext == 'pdf':
        text = ""
        with pdfplumber.open(path) as pdf:
            for p in pdf.pages:
                page_text = p.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    elif ext == 'docx':
        return docx2txt.process(path) or ""
    elif ext == 'txt':
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""