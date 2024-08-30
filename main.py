import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_vision_response,
                            gemini_pro_response)
import os

working_directory = os.path.dirname(os.path.abspath(__file__))

#setting up the page configuration
st.set_page_config(page_title= "Dzuko",
                   page_icon = "🧠",
                   layout="centered"
)


with st.sidebar:
    selected = option_menu(menu_title="Dzuko",
                            options =["ChatBot", "Image", "Ask me anything"],
                            menu_icon='robot',
                            icons=["chat-left", "file-image-fill", "patch-question-fill"],
                            default_index=0)

#function to translate role btw gemini pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role

if selected == "ChatBot" :
    model = load_gemini_pro_model()

    #initialize chat session in streamlit
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history = [])

    #streamlit page tittle
    st.title("🤖 ChatBot")


    #to desplay the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    #imput field for chat input
    user_prompt = st.chat_input("Ask Dzuko..")
    if user_prompt:
        
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        #desplay
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

#image captioning
if selected == "Image":
    #streamlit page title
    st.title("📷 SnapBot")

    #create a box to upload image
    upload_image = st.file_uploader("upload an image..", type = ["jpg","jpeg","png"])

    if st.button("Generate Caption"):

        image = Image.open(upload_image)
        col1, col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800,500))
            st.image(resized_image)

        default_prompt = "Describe this"

        #getting the response from gemini pro vision model
        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)

#ask me a question
if selected == "Ask me anything":
    st.title("Ask me a question ❔")

    #textbox for the user
    user_prompt = st.text_area(label='', placeholder="Ask Dzuko..")

    if st.button("Get Answer"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)