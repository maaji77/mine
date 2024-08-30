import streamlit as st
from gtts import gTTS
from googletrans import Translator
import os
import tempfile

# Initialize the translator
translator = Translator()

# Supported languages
LANGUAGES = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
}

# Title of the app
st.title("Multi-Language Chatbot")

# Language selection
language = st.selectbox("Select Language:", list(LANGUAGES.keys()))
lang_code = LANGUAGES[language]

# Chatbot interaction
user_input = st.text_area("Enter your message:")

# Button to generate response
if st.button("Send"):
    if user_input:
        # Translate user input to English (assuming bot's default language is English)
        translated_input = translator.translate(user_input, dest='en').text

        # Here you would normally generate a response from the chatbot
        # For this example, we simulate a response
        bot_response = f"You said '{translated_input}', how can I help you?"

        # Translate the response back to the selected language
        translated_response = translator.translate(bot_response, dest=lang_code).text

        # Display the response
        st.write(translated_response)

        # Convert the response to speech
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            tts = gTTS(text=translated_response, lang=lang_code)
            tts.save(tmp.name + '.mp3')
            st.audio(tmp.name + '.mp3', format="audio/mp3")
    else:
        st.error("Please enter a message.")
