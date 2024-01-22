import os
import io
import base64
from PIL import Image
import pdf2image
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ##Convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        ## Converts to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mimo_type":"image/jpeg",
            "data":base64.b64encode(img_byte_arr).decode() ## encode to base64

        }]

        return pdf_parts
    else:
        raise FileNotFoundError("No file is UPLOADED")
    


## Write Streamlip App
    
st.set_page_config(page_title="Expert for ATS")
st.header("ATS for RESUME")
input_text = st.text_area("JobDescription: ", key = "input")
uploaded_file = st.file_uploader("Upload your CV(PDF)...", type = 'pdf')

if uploaded_file is not None:
    st.write("File uploaded succesully")

submit1 = st.button("Tell me about the CV")
# submit2 = st.button("How can I Improvise my SKILLS")
submit3 = st.button("How much Percent Match")

input_prompt1 = """
Your Expert in Technical HR Manager in the field od Data science, Full stack,
 and web technologies ..etc, then your task is to review provided resume against 
 the JD
"""

input_prompt3 = """
Your Expert in Technical HR Manager in the field od Data science, Full stack,
 and web technologies ..etc, Evaluate Resume
"""


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the CV")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the CV")






