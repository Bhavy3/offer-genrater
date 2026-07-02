import docx
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph
import copy
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

# 1. Find the 'No' column textbox to use as a template for paragraph alignment and spacing
no_txbx = next(tx for tx in doc.element.xpath('//*[local-name()="txbxContent"]') 
               if Paragraph(tx.xpath('*[local-name()="p"]')[0], doc._body).text.strip() == "No")
no_paras = no_txbx.xpath('*[local-name()="p"]')
no_pPrs = [copy.deepcopy(p.pPr) if p.pPr is not None else None for p in no_paras]

# 2. Rebuild the Names textbox structurally to match the 7-paragraph 'No' textbox
for txbx in doc.element.xpath('//*[local-name()="txbxContent"]'):
    p_elements = txbx.xpath('*[local-name()="p"]')
    if p_elements and "Student Name" in Paragraph(p_elements[0], doc._body).text:
        for p in p_elements:
            txbx.remove(p)
        for row in range(7):
            new_p = OxmlElement('w:p')
            if row < len(no_pPrs) and no_pPrs[row] is not None:
                new_p.append(copy.deepcopy(no_pPrs[row]))
            if row == 0:
                # Recreate Student Name header in Arial Black
                r = OxmlElement('w:r')
                rPr = OxmlElement('w:rPr')
                rFonts = OxmlElement('w:rFonts')
                rFonts.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii', 'Arial Black')
                rPr.append(rFonts)
                rPr.append(OxmlElement('w:b')) # bold
                r.append(rPr)
                t = OxmlElement('w:t')
                t.text = "Student Name"
                r.append(t)
                new_p.append(r)
            elif row in [2, 4, 6]:
                # Recreate names in Arial 12pt
                student_idx = (row - 2) // 2
                name = str(students_data[student_idx].get('Student Name', '')).strip() if student_idx < len(students_data) else ''
                if name:
                    r = OxmlElement('w:r')
                    rPr = OxmlElement('w:rPr')
                    sz = OxmlElement('w:sz')
                    sz.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '24') # 12pt
                    rPr.append(sz)
                    r.append(rPr)
                    t = OxmlElement('w:t')
                    t.text = name
                    r.append(t)
                    new_p.append(r)
            txbx.append(new_p)

# Save
doc.save("scratch/generated_minimal.docx")
print("Saved rebuilt document!")

# Convert to PDF
print("Converting to PDF...")
try:
    from docx2pdf import convert
    convert("scratch/generated_minimal.docx", "scratch/generated_minimal.pdf")
    print("PDF converted successfully!")
except Exception as e:
    print("docx2pdf failed:", e)

# Render to PNG
print("Rendering PDF to PNG...")
import fitz
doc_pdf = fitz.open("scratch/generated_minimal.pdf")
page = doc_pdf.load_page(0)
pix = page.get_pixmap(dpi=150)
pix.save("scratch/test_minimal.png")
print("Saved page to scratch/test_minimal.png")
