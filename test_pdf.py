import os
import docx
import win32com.client
from docx2pdf import convert

docx_path = os.path.abspath(r"c:\Users\IQ\OneDrive\Documents\padas 1\vibrant\offer genrater\test_pdf_local.docx")
pdf_path = os.path.abspath(r"c:\Users\IQ\OneDrive\Documents\padas 1\vibrant\offer genrater\test_pdf_local.pdf")

doc = docx.Document()
doc.add_paragraph("Test")
doc.save(docx_path)

try:
    convert(docx_path, pdf_path)
    print("Success docx2pdf, created:", pdf_path)
except Exception as e:
    import traceback
    traceback.print_exc()
