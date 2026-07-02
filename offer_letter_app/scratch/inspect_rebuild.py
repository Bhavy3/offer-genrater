import docx

doc = docx.Document("scratch/generated_replace_only.docx")
txbx_elements = doc.element.xpath('//*[local-name()="txbxContent"]')

for txbx in txbx_elements:
    p_elements = txbx.xpath('*[local-name()="p"]')
    if p_elements:
        from docx.text.paragraph import Paragraph
        first_p = Paragraph(p_elements[0], doc._body)
        if "Student" in first_p.text:
            print("Student Name XML:")
            print(docx.oxml.xmlchemy.serialize_for_reading(p_elements[0]))
            break
