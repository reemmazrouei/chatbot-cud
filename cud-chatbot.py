import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import PyPDF2
#This loads in all the environment variables.
load_dotenv('.env')

#The block of code below is used to configure the settings of the page itself.
st.set_page_config(
    page_icon=('⚡'),
    page_title='Chat with CUD Chatbot!',
    layout='centered',
)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

#Now we can initialize the Chatbot with the API key using the code below.
gen_ai.configure(api_key = GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

#Now we define a function that will help us chat with the CUD Chatbot using input and responses.
def translate_role_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role

# Function to extract text from uploaded PDF file
def extract_text_from_pdf(uploaded_file):
    text = ''
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text

#Now we create a chat session with the chatbot
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.title("👾 CUD Chatbot 👾")

#Displays chat history with the bot
if 'chat_session' in st.session_state:
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_streamlit(message.role)):
            st.markdown(message.parts[0].text)

#User input
input_user = st.chat_input('How can I help you?')
if input_user:
    st.chat_message('user').markdown(input_user)
    gemini_response = st.session_state.chat_session.send_message(input_user)
    
    #The line below is used to display the response
    with st.chat_message('assistant'):
        st.markdown(gemini_response.text)

# File uploader for PDFs
uploaded_file = st.file_uploader('Upload PDF', type=['pdf'])
if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.write('*PDF Content:*')
    st.write(pdf_text)

    # Allow the chatbot to respond to questions regarding the PDF content
    chat_input = st.text_input('Ask a question about the PDF content')
    if st.button('Ask'):
        gemini_response = st.session_state.chat_session.send_message(chat_input)
        with st.chat_message('assistant'):
            st.markdown(gemini_response.text)
