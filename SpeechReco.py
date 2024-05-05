import streamlit as st
import speech_recognition as sr

def transcribe_speech(api, language):
    # Initialize recognizer class
    r = sr.Recognizer()
    
    # Set language for speech recognition
    if language:
        r.energy_threshold = 4000
        with sr.Microphone() as source:
            st.info("Parlez maintenant...")
            audio_text = r.listen(source)
    else:
        with sr.Microphone() as source:
            st.info("Speak now...")
            audio_text = r.listen(source, timeout=3, phrase_time_limit=5)
        
    st.info("Transcription...")
    
    try:
        # Selecting the API based on user's choice
        if api == "Google Speech Recognition":
            if language:
                text = r.recognize_google(audio_text, language=language)
            else:
                text = r.recognize_google(audio_text)
        elif api == "Wit.ai":
            # You can add more conditions for other APIs if available
            text = r.recognize_wit(audio_text, key='YOUR_WIT.AI_API_KEY')
        else:
            text = "Selected API is not supported"
        
        return text
    except sr.UnknownValueError:
        return "Désolé, je n'ai pas pu comprendre l'audio"
    except sr.RequestError as e:
        return "Impossible de récupérer les résultats de l'API; {0}".format(e)

def main():
    st.title("Application de Reconnaissance Vocale")
    st.write("Cliquez sur le microphone pour commencer à parler:")
    
    # Add a selection box for choosing the API
    api_options = ["Google Speech Recognition", "Wit.ai"]
    selected_api = st.selectbox("Sélectionnez l'API de reconnaissance vocale", api_options)
    
    # Add a checkbox for selecting the language
    st.write("Choisissez la langue:")
    language_options = {"Français": "fr-FR", "Anglais": "en-US"}
    selected_language = st.selectbox("Sélectionnez la langue", list(language_options.keys()))
    
    # Add a button to trigger speech recognition
    if st.button("Commencer l'enregistrement"):
        text = transcribe_speech(selected_api, language_options[selected_language])
        st.write("Transcription: ", text)
        
        # Add an option to save the transcription to a file
        if st.button("Enregistrer la transcription"):
            save_to_file(text)

def save_to_file(text):
    with open("transcription.txt", "w") as file:
        file.write(text)
    st.write("Transcription enregistrée dans le fichier: transcription.txt")

if __name__ == "__main__":
    main()
