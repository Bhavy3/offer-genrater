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

# Find the Names textboxes
txbx_elements = doc.element.xpath('//*[local-name()="txbxContent"]')

names_txbxs = []
for txbx in txbx_elements:
    p_elements = txbx.xpath('*[local-name()="p"]')
    if p_elements:
        from docx.text.paragraph import Paragraph
        first_p = Paragraph(p_elements[0], doc._body)
        if "Student Name" in first_p.text:
            names_txbxs.append(p_elements)

s1 = students_data[0].get('Student Name', '').strip()
s2 = students_data[1].get('Student Name', '').strip()
s3 = students_data[2].get('Student Name', '').strip()

for p_elements in names_txbxs:
    p0 = Paragraph(p_elements[0], doc._body)
    p1 = Paragraph(p_elements[1], doc._body)
    
    # 1. Reset paragraph spacing to defaults
    p0.paragraph_format.line_spacing = None
    p0.paragraph_format.first_line_indent = None
    p0.paragraph_format.left_indent = None
    p0.paragraph_format.space_before = None
    p0.paragraph_format.space_after = None
    
    p1.paragraph_format.line_spacing = None
    p1.paragraph_format.first_line_indent = None
    p1.paragraph_format.left_indent = None
    p1.paragraph_format.space_before = None
    p1.paragraph_format.space_after = None

# Map replacements with strategic newlines
replacements = {
    "Khambhadiya Taksh Khodabhai": f"\n\n{s1}\n\n",
    "Parmar Kishan S.": f"{s2}",
    "Shah Hetansh Bipinbhai": f"\n{s3}",
}

# Run the exact replacement loop from app.py
all_paragraphs = list(doc.paragraphs)
all_paragraphs.extend([Paragraph(p, doc._body) for p in doc.element.xpath('//w:txbxContent//w:p')])

for i in range(3):
    old_name = ["Khambhadiya Taksh Khodabhai", "Parmar Kishan S.", "Shah Hetansh Bipinbhai"][i]
    new_name = replacements[old_name]
    
    old_enrollment = ["202435802415", "202435802495", "202435802587"][i]
    new_enrollment = ["306", "2415", "204"][i]
    
    for p in all_paragraphs:
        for r in p.runs:
            if old_name in r.text:
                r.text = r.text.replace(old_name, new_name)
            if old_enrollment in r.text:
                r.text = r.text.replace(old_enrollment, new_enrollment)
        # Fallback to paragraph-level replacement if text is split
        if old_name in p.text or old_enrollment in p.text:
            p.text = p.text.replace(old_name, new_name).replace(old_enrollment, new_enrollment)

doc.save("scratch/generated_replace_only.docx")
print("Saved simple rebuilt document!")

# Convert to PDF
print("Converting to PDF...")
try:
    from docx2pdf import convert
    convert("scratch/generated_replace_only.docx", "scratch/generated_replace_only.pdf")
    print("PDF converted successfully!")
except Exception as e:
    print("docx2pdf failed:", e)

# Render to PNG
print("Rendering PDF to PNG...")
import fitz
doc_pdf = fitz.open("scratch/generated_replace_only.pdf")
page = doc_pdf.load_page(0)
pix = page.get_pixmap(dpi=150)
pix.save("scratch/test_replace_only.png")
print("Saved page to scratch/test_replace_only.png")
