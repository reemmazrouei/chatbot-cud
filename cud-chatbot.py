import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

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