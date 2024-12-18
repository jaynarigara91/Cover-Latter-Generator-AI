import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain.document_loaders import PyPDFLoader
from chain import Chains
import tempfile

def create_streamlit_app():
    st.title("📧 Cover Latter Generator")
    url_input = st.text_input("Enter a Job Career URL:")
    uploaded_cv = st.file_uploader("Upload a you CV", type=["pdf"])
    submit_button = st.button("Submit")

    if submit_button:
        try:
            Chain = Chains()
            loader = WebBaseLoader([url_input])
            page_detail = loader.load().pop().page_content
            job_detail = Chain.get_job_detail(page_detail)
            
            if uploaded_cv is not None:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(uploaded_cv.read())
                    temp_file_path = temp_file.name
                    
            detail_cv = PyPDFLoader(temp_file_path).load().pop().page_content
            Mail = Chain.get_email(job_detail,detail_cv)
            st.code(Mail, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Cover latter Generator", page_icon="📧")
    create_streamlit_app()