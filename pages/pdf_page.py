import time
import streamlit as st
import pdf_chat as pfc
from PyPDF2 import PdfReader
with st.sidebar:    
    open_ai_key = st.text_input("Enter OpenAI API key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

def main():
    st.title("PDF Chatbot")
    st.caption("Chat with any pdf file!!")        
    
    pdf = st.file_uploader("upload your pdf", type='pdf')
    if pdf is None:
        st.info("Please upload a pdf file")
    else:
        if open_ai_key is None:
            st.info("Please enter your OpenAI API key")
            st.stop()
        st.session_state.pdf_embeddings = pfc.pdf_reader(pdf, open_ai_key)
        # st.write(st.session_state.pdf_embeddings)
    if 'message' not in st.session_state:
         st.session_state['message'] = [
        {"role": "assistant", "content": "I'm you are a helpful PDF assistant."},
    ]
         
    for msg in st.session_state.message:
        st.chat_message(msg["role"]).write(msg["content"])
    
    if prompt := st.chat_input():
        if not open_ai_key:
            st.info("Please enter your OpenAI API key")
            st.stop()
        if pdf is None:
            st.info("Please upload a pdf file")
            st.stop()
        st.session_state.message.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = pfc.get_query_response(st.session_state.pdf_embeddings, prompt, open_ai_key)
        st.session_state.message.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)    
        


if __name__ == '__main__':
    main()
