import streamlit as st
import youtube_chat as ytc

st.set_page_config(
    page_title = "Youtube and PDF Chat app",
    page_icon = "🗣️",
)
with st.sidebar:    
    open_ai_key = st.text_input("Enter OpenAI API key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


st.title("Youtube Chatbot")
st.caption("Chat with any yoututbe video")

# video_url = st.text_input("Enter youtube video url", type="default")
url_input = st.form("url")
video_url = url_input.text_input("Enter youtube video url", type="default")
submit = url_input.form_submit_button("Submit")

if submit:    
    if 'video_embeddings' not in st.session_state:
        st.session_state.video_embeddings = ytc.yt_url_to_vectordb(video_url, open_ai_key)

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "assistant", "content": "I'm you are a helpful youtube assistant."},
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not open_ai_key:
        st.info("Please enter your OpenAI API key")
        st.stop()
    if not video_url:
        st.info("Please enter youtube video url")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = ytc.get_query_response(st.session_state.video_embeddings, prompt, open_ai_key)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
