from dotenv import load_dotenv

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Giridhar\Downloads\elliptical-tree-414214-b89ceb63b537.json"

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input,prompt):
#     model=genai.GenerativeModel('gemini-pro-vision')
#     response=model.generate_content([input,pdf_content[0],prompt])
#     return response.text

# def get_gemini_response(prompt, pdf_content, input_text):
#     model = genai.GenerativeModel('gemini-pro-vision')
#     response = model.generate_content([input_text, pdf_content[0], prompt])
#     return response.text
def get_gemini_response(input_prompt, pdf_content, input_text):
    model = load_model('gemini-1.5-flash')  # Update model to the new version
    response = model.generate_content([input_text, pdf_content[0], input_prompt])
    return response



def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("Application Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


# submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. 
give me the percentage of match if the resume matches the job description 
. First the output should come as application is blank if that file dosen't contain any text then keywords missing  and last final thoughts. 
"""

# if submit1:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_prompt1,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")

if submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")



   



