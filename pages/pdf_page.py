import time
import streamlit as st
import pdf_chat as pfc
from PyPDF2 import PdfReader
with st.sidebar:    
    open_ai_key = st.text_input("Enter OpenAI API key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

def main():
    st.title("PDF Chatbot")
    st.caption("Chat with any pdf file")        
    
    pdf = st.file_uploader("upload your pdf", type='pdf')
    if pdf is None:
        st.info("Please upload a pdf file")
    else:
        pdf_read = pfc.pdf_reader(pdf)
        st.write(pdf_read)


if __name__ == '__main__':
    main()
