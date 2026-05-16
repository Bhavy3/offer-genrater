import streamlit as st

import io
import os
import sys

st.set_page_config(page_title="Vibrant Offer Letter", layout="wide")
st.title("📄 Vibrant Technology - Internship Offer Letter")

# ===================== DEFAULT TEMPLATE =====================
# Use relative path for cloud compatibility
DEFAULT_TEMPLATE_PATH = "ALAN BIJO VARGHESE.docx"
# If running locally in a different directory, try to resolve it
if not os.path.exists(DEFAULT_TEMPLATE_PATH):
    # Fallback for local testing
    fallback = r"C:\Users\IQ\OneDrive\Documents\padas 1\vibrant\offer genrater\ALAN BIJO VARGHESE.docx"
    if os.path.exists(fallback):
        DEFAULT_TEMPLATE_PATH = fallback

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("Student Details")
    
    student_name = st.text_input("Student Full Name", value="bhavy gajjar")
    enrollment_no = st.text_input("Enrollment Number", value="2204030100306")
    
    import datetime
    today = datetime.date.today()
    start_date_obj = st.date_input("Starting Date", value=today)
    end_date_obj = st.date_input("Ending Date", value=today + datetime.timedelta(days=30))
    subject = st.text_input("Domain / Subject", value="Java")
    
    start_date = start_date_obj.strftime("%d/%m/%Y")
    end_date = end_date_obj.strftime("%d/%m/%Y")
    
    st.divider()
    st.info("Default template is already loaded")
    
    uploaded_file = st.file_uploader("Upload Different Template (Optional)", type=["docx"])
    
    generate_btn = st.button("🚀 Generate Offer Letter", type="primary", use_container_width=True)

# ===================== GENERATION =====================
if generate_btn:
    import docx
    import tempfile

    # Helper function to copy font styles
    def add_formatted_run(paragraph, text, is_bold=False, ref_font=None):
        r = paragraph.add_run(text)
        r.bold = is_bold
        if ref_font:
            if ref_font.name:
                r.font.name = ref_font.name
            if ref_font.size:
                r.font.size = ref_font.size
            if ref_font.color and ref_font.color.rgb:
                r.font.color.rgb = ref_font.color.rgb
        return r

    try:
        # Load the DOCX template
        if uploaded_file is not None:
            with open("temp_template.docx", "wb") as f:
                f.write(uploaded_file.read())
            doc = docx.Document("temp_template.docx")
        else:
            doc = docx.Document(DEFAULT_TEMPLATE_PATH)

        # The issue date is the starting date (as requested: "starting and todays date must be same")
        issue_date = start_date

        # 1. Update Top Right Date (Paragraph 8)
        for r in doc.paragraphs[8].runs:
            r.text = r.text.replace('11/05/2026', issue_date)

        # 2. Update Name (Paragraph 10)
        runs10 = doc.paragraphs[10].runs
        if len(runs10) >= 6:
            runs10[1].text = student_name
            for i in range(2, 6): 
                runs10[i].text = '' 

        # 3. Update Enrollment (Paragraph 11)
        for r in doc.paragraphs[11].runs:
            r.text = r.text.replace('2241230265', enrollment_no)

        # 4. Update Main Paragraph (Paragraph 18)
        for r in doc.paragraphs[18].runs:
            r.text = r.text.replace('11/05/2026', start_date)
            r.text = r.text.replace('11/08/2026', end_date)
            r.text = r.text.replace('ALAN BIJO ', student_name)
            r.text = r.text.replace('VARGHESE', '')
            r.text = r.text.replace('Data Science', subject)

        # Save to temp docx
        temp_dir = tempfile.mkdtemp()
        docx_path = os.path.join(temp_dir, "offer_letter.docx")
        pdf_path = os.path.join(temp_dir, "offer_letter.pdf")
        doc.save(docx_path)

        with open(docx_path, "rb") as f:
            final_docx = f.read()

        final_pdf = None
        # Convert to PDF only if on Windows (Requires MS Word)
        if sys.platform == "win32":
            try:
                from docx2pdf import convert
                import pythoncom
                pythoncom.CoInitialize() # required for COM in threads
                convert(docx_path, pdf_path)
                with open(pdf_path, "rb") as f:
                    final_pdf = f.read()
            except Exception as e:
                pass

        # ===================== DISPLAY RESULT =====================
        st.success("✅ Offer Letter Generated Successfully!")

        if final_pdf:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    label="📥 Download PDF",
                    data=final_pdf,
                    file_name=f"Offer_Letter_{student_name.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            with col2:
                st.download_button(
                    label="📝 Download Word (DOCX)",
                    data=final_docx,
                    file_name=f"Offer_Letter_{student_name.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            st.info("Live PDF Preview")
            import base64
            base64_pdf = base64.b64encode(final_pdf).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.download_button(
                label="📝 Download Word (DOCX)",
                data=final_docx,
                file_name=f"Offer_Letter_{student_name.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
            st.warning("⚠️ Live PDF preview is not available in the Cloud environment. Please download the DOCX file directly.")

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Make sure the default template exists.")

else:
    st.info("Fill details on the left sidebar and click **Generate**")
    st.caption("Made for clean text replacement using native DOCX formatting")