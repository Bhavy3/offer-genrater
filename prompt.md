Create a professional Streamlit web application for generating internship offer letters automatically using the provided PDF template as the exact design reference.

OBJECTIVE:
The application should allow users to enter student details into a form and instantly generate a professional PDF offer letter that matches the uploaded template design 100% accurately.

IMPORTANT:
DO NOT redesign the letter manually.
USE the uploaded PDF as the fixed background/template.
Only overlay dynamic student information on top of the template.

APP REQUIREMENTS:

1. TECHNOLOGY
- Python
- Streamlit
- PyMuPDF (fitz)
- Pillow
- reportlab

2. UI DESIGN
Create a clean and modern Streamlit UI with:
- Title: "Offer Letter Generator"
- Left-side input form
- Right-side live preview section
- Professional spacing and layout
- Generate PDF button
- Download PDF button after generation

3. FORM FIELDS
Create editable input fields for:
- Student Name
- College Name
- Enrollment Number
- Starting Date
- Ending Date
- Subject

4. INPUT FORMAT EXAMPLE

Name: Vora Mohammad Mudassir
College Name: Shreyarth University
Enrollment No: 2402104179
Starting Date: 18/05/2026
Ending Date: 05/06/2026
Subject: Data Analysis

5. TEMPLATE HANDLING
- Use the uploaded PDF as the original offer letter template
- Keep:
  - Logo
  - Footer
  - Header
  - Signature
  - Colors
  - Spacing
  - Background
exactly unchanged

6. TEXT OVERLAY
Overlay the student details at the correct positions on the PDF.

Replace/add:
- Student name
- College name
- Enrollment number
- Internship subject
- Start date
- End date

7. OUTPUT
When the user clicks "Generate Offer Letter":
- Generate a new PDF
- Show live preview inside Streamlit
- Allow instant PDF download

8. FILE STRUCTURE

offer_letter_app/
│
├── app.py
├── template.pdf
├── output/
├── fonts/

9. CODE REQUIREMENTS
- Write clean and beginner-friendly code
- Add comments explaining important sections
- Use reusable functions
- Handle missing fields validation
- Use temporary files safely

10. EXTRA FEATURES
- Add success message after generation
- Auto filename:
  Offer_Letter_<StudentName>.pdf

11. VERY IMPORTANT
The final generated offer letter must visually match the uploaded PDF template as closely as possible.

Do not create fake placeholder designs.
Do not use random templates.
Use the uploaded PDF directly as the reference/template.

12. BONUS IF POSSIBLE
- Add drag-and-drop PDF template upload
- Add dark/light mode compatibility
- Keep code production-ready

Generate the complete working code in one file.