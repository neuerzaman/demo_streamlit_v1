#pip install google-genai

import streamlit as st, os, time
from google import genai
from google.genai import types
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from langchain_google_genai import ChatGoogleGenerativeAI  # For interacting with Google Gemini via LangChain
from langgraph.prebuilt import create_react_agent  # For creating a ReAct agent
from langchain_core.messages import HumanMessage, AIMessage  # For message formatting

# Set the title and a caption for the web page
def setup_page():
    st.set_page_config(
        page_title="	⚡ Voice Chatbot",
        layout="centered"
    )
    st.header("Chatbot using Gemini 2.5 Flash!" )
    st.caption("A simple and friendly chat but have many options using LangGraph with Google's Gemini model")

    # Create a sidebar section for app settings using 'with st.sidebar:'
    with st.sidebar:
        # Add a subheader to organize the settings
        st.sidebar.header("Options", divider='rainbow')
        hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
        st.markdown(hide_menu_style, unsafe_allow_html=True)
    
# Create a text input field for the Google AI API Key.
# 'type="password"' hides the key as the user types it.
google_api_key = st.text_input("Google AI API Key", type="password")
    
def get_clear():
    clear_button=st.sidebar.button("Start new session", key="clear")
    return clear_button

# Check if the user has provided an API key.
# If not, display an informational message and stop the app from running further.
if not google_api_key:
    st.info("Please add your Google AI API key in the sidebar to start chatting.", icon="🗝️")
    st.stop()

# This block of code handles the creation of the LangGraph agent.
# It's designed to be efficient: it only creates a new agent if one doesn't exist
# or if the user has changed the API key in the sidebar.

def get_choice():
    choice = st.sidebar.radio("Choose:", ["Converse with Gemini 2.5",
                                          "Chat with PDFs",
                                          "Chat with an image",
                                          "Chat with audio",
                                          "Chat with video"],)
    return choice

def get_clear():
    clear_button=st.sidebar.button("Start new session", key="clear")
    return clear_button


# This block of code handles the creation of the LangGraph agent.
# It's designed to be efficient: it only creates a new agent if one doesn't exist
# or if the user has changed the API key in the sidebar.


def main():
    choice = get_choice()
    
    if choice == "Converse with Gemini 2.5":
        st.subheader("Ask Gemini")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']
    
        if 'message' not in st.session_state:
            st.session_state.message = " "
        
        if clear not in st.session_state:
            chat = client.chats.create(model="gemini-2.5-flash", config=types.GenerateContentConfig(
                system_instruction="You are a helpful assistant. Your answers need to brief and concise.",))
            prompt = st.chat_input("Enter your question here")
            if prompt:
                with st.chat_message("user"):
                    st.write(prompt)
        
                st.session_state.message += prompt
                with st.chat_message(
                    "model", avatar="🧞‍♀️",
                ):
                    response = chat.send_message(st.session_state.message)
                    st.markdown(response.text) 
                    st.sidebar.markdown(response.usage_metadata)
                st.session_state.message += response.text
                    
    elif choice == "Chat with PDFs":
        st.subheader("Chat with your PDF file")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']
    
        if 'message' not in st.session_state:
            st.session_state.message = " "
        
        if clear not in st.session_state:
        
            uploaded_files2 = st.file_uploader("Choose 1 or more files",  type=['pdf'], accept_multiple_files=True)
               
            if uploaded_files2:
                merger = PdfMerger()
                for file in uploaded_files2:
                        merger.append(file)
    
                fullfile = "merged_all_files.pdf"
                merger.write(fullfile)
                merger.close()

                file_upload = client.files.upload(file=fullfile) 
                chat2b = client.chats.create(model=MODEL_ID,
                    history=[
                        types.Content(
                            role="user",
                            parts=[
    
                                    types.Part.from_uri(
                                        file_uri=file_upload.uri,
                                        mime_type=file_upload.mime_type),
                                    ]
                            ),
                        ]
                        )
                prompt2b = st.chat_input("Enter your question here")
                if prompt2b:
                    with st.chat_message("user"):
                        st.write(prompt2b)
            
                    st.session_state.message += prompt2b
                    with st.chat_message(
                        "model", avatar="🧞‍♀️",
                    ):
                        response2b = chat2b.send_message(st.session_state.message)
                        st.markdown(response2b.text)
                        st.sidebar.markdown(response2b.usage_metadata)
                    st.session_state.message += response2b.text
            
    elif choice == "Chat with an image":
        st.subheader("Chat with your PDF file")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']
    
        if 'message' not in st.session_state:
            st.session_state.message = " "
        
        if clear not in st.session_state:
            uploaded_files2 = st.file_uploader("Choose your PNG or JPEG file",  type=['png','jpg'], accept_multiple_files=False)
            if uploaded_files2:
                file_name2=uploaded_files2.name
                file_upload = client.files.upload(file=file_name2)
                chat3 = client.chats.create(model=MODEL_ID,
                    history=[
                        types.Content(
                            role="user",
                            parts=[
    
                                    types.Part.from_uri(
                                        file_uri=file_upload.uri,
                                        mime_type=file_upload.mime_type),
                                    ]
                            ),
                        ]
                        )
                prompt3 = st.chat_input("Enter your question here")
                if prompt3:
                    with st.chat_message("user"):
                        st.write(prompt3)
            
                    st.session_state.message += prompt3
                    with st.chat_message(
                        "model", avatar="🧞‍♀️",
                    ):
                        response3 = chat3.send_message(st.session_state.message)
                        st.markdown(response3.text)
                    st.session_state.message += response3.text
                
    elif choice == "Chat with audio":
        st.subheader("Chat with your audio file")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']
    
        if 'message' not in st.session_state:
            st.session_state.message = " "
        
        if clear not in st.session_state:
            uploaded_files3 = st.file_uploader("Choose your mp3 or wav file",  type=['mp3','wav'], accept_multiple_files=False)
            if uploaded_files3:
                file_name3=uploaded_files3.name
                file_upload = client.files.upload(file=file_name3)
                chat4 = client.chats.create(model=MODEL_ID,
                    history=[
                        types.Content(
                            role="user",
                            parts=[
    
                                    types.Part.from_uri(
                                        file_uri=file_upload.uri,
                                        mime_type=file_upload.mime_type),
                                    ]
                            ),
                        ]
                        )
                prompt5 = st.chat_input("Enter your question here")
                if prompt5:
                    with st.chat_message("user"):
                        st.write(prompt5)
            
                    st.session_state.message += prompt5
                    with st.chat_message(
                        "model", avatar="🧞‍♀️",
                    ):
                        response4 = chat4.send_message(st.session_state.message)
                        st.markdown(response4.text)
                    st.session_state.message += response4.text

    elif choice == "Chat with video":
        st.subheader("Chat with your video file")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']
    
        if 'message' not in st.session_state:
            st.session_state.message = " "
        
        if clear not in st.session_state:
            uploaded_files4 = st.file_uploader("Choose your mp4 or mov file",  type=['mp4','mov'], accept_multiple_files=False)
            
            if uploaded_files4:
                file_name4=uploaded_files4.name
                video_file = client.files.upload(file=file_name4)
                while video_file.state == "PROCESSING":
                    time.sleep(10)
                    video_file = client.files.get(name=video_file.name)
                
                if video_file.state == "FAILED":
                  raise ValueError(video_file.state)
                
                chat5 = client.chats.create(model=MODEL_ID,
                    history=[
                        types.Content(
                            role="user",
                            parts=[
    
                                    types.Part.from_uri(
                                        file_uri=video_file.uri,
                                        mime_type=video_file.mime_type),
                                    ]
                            ),
                        ]
                        )
                prompt4 = st.chat_input("Enter your question here")
                if prompt4:
                    with st.chat_message("user"):
                        st.write(prompt4)
            
                    st.session_state.message += prompt4
                    with st.chat_message(
                        "model", avatar="🧞‍♀️",
                    ):
                        response5 = chat5.send_message(st.session_state.message)
                        st.markdown(response5.text)
                    st.session_state.message += response5.text
                    
                
if __name__ == '__main__':
    setup_page()
    client = genai.Client(api_key=google_api_key)
    MODEL_ID = "gemini-2.5-flash"
    main()
