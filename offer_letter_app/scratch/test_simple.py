import docx
import os
import shutil

# Copy template to bypass locks
template_path = os.path.abspath(os.path.join("..", "_Vibrant tech lab - kishan , hetansh.docx"))
temp_template = "scratch/temp_template.docx"
shutil.copy2(template_path, temp_template)

# Load document
doc = docx.Document(temp_template)

# Simulation inputs
students_data = [
    {"No": 1, "Student Name": "bhavy", "Enrollment Number": "306"},
    {"No": 2, "Student Name": "krishna", "Enrollment Number": "2415"},
    {"No": 3, "Student Name": "dev", "Enrollment Number": "204"}
]

# Run the exact logic from app.py
issue_date = "18/06/2026"
project_name = "Travels with Strangers"
technology = "Php"

from docx.text.paragraph import Paragraph
all_paragraphs = list(doc.paragraphs)
all_paragraphs.extend([Paragraph(p, doc._body) for p in doc.element.xpath('//w:txbxContent//w:p')])

# Map replacements with strategic newlines
s1 = students_data[0].get('Student Name', '').strip()
s2 = students_data[1].get('Student Name', '').strip()
s3 = students_data[2].get('Student Name', '').strip()

replacements = {
    "Khambhadiya Taksh Khodabhai": f"\n\n{s1}\n\n",
    "Parmar Kishan S.": f"{s2}",
    "Shah Hetansh Bipinbhai": f"\n{s3}",
    "202435802415": "306",
    "202435802495": "2415",
    "202435802587": "204"
}

for i in range(3):
    old_name = ["Khambhadiya Taksh Khodabhai", "Parmar Kishan S.", "Shah Hetansh Bipinbhai"][i]
    new_name = replacements[old_name]
    
    old_enrollment = ["202435802415", "202435802495", "202435802587"][i]
    new_enrollment = replacements[old_enrollment]
    
    for p in all_paragraphs:
        for r in p.runs:
            if old_name in r.text:
                r.text = r.text.replace(old_name, new_name)
            if old_enrollment in r.text:
                r.text = r.text.replace(old_enrollment, new_enrollment)
        # Fallback to paragraph-level replacement if text is split
        if old_name in p.text or old_enrollment in p.text:
            p.text = p.text.replace(old_name, new_name).replace(old_enrollment, new_enrollment)

doc.save("scratch/generated_simple.docx")
print("Saved simple rebuilt document!")

# Convert to PDF
print("Converting to PDF...")
try:
    from docx2pdf import convert
    convert("scratch/generated_simple.docx", "scratch/generated_simple.pdf")
    print("PDF converted successfully!")
except Exception as e:
    print("docx2pdf failed:", e)

# Render to PNG
print("Rendering PDF to PNG...")
import fitz
doc_pdf = fitz.open("scratch/generated_simple.pdf")
page = doc_pdf.load_page(0)
pix = page.get_pixmap(dpi=150)
pix.save("scratch/test_simple.png")
print("Saved page to scratch/test_simple.png")
