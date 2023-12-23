from dotenv import load_dotenv
from PyPDF2 import PdfReader

def pdf_reader(pdf):
    pdf_read = PdfReader(pdf)
    text = ""
    for page in pdf_read.pages:
        text += page.extract_text()
        
    return text
    

