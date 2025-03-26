import streamlit as st
import speech_recognition as sr
import pyttsx3
import requests

# Set your Mistral API key
MISTRAL_API_KEY = "PdUU4XtVP6juMrwpHtBYC4tbv49hjCJg"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Predefined responses
predefined_responses = {
    "What should we know about your life story in a few sentences": 
        "I have a background in Computer Science with a passion for AI and Machine Learning. I've worked on projects in NLP and Computer Vision, and I'm constantly learning and growing in this space.",
    "What’s your number one superpower": 
        "My #1 superpower is adaptability. I can quickly learn new concepts, adapt to different work environments, and solve complex problems effectively.",
    "What are the top three areas you would like to grow in": 
        "I’d like to improve my expertise in large-scale AI model deployment, learn more about reinforcement learning, and enhance my leadership skills in AI teams.",
    "What misconception do your coworkers have about you": 
        "A common misconception is that I prefer working alone. In reality, I enjoy teamwork and collaborating to solve problems efficiently.",
    "How do you push your boundaries and limits": 
        "I challenge myself by taking on new, difficult projects and setting ambitious learning goals. I also stay updated with the latest advancements in AI and actively contribute to open-source projects."
}

def speech_to_text():
    """Convert speech to text using SpeechRecognition"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand the audio.")
        return None
    except sr.RequestError:
        st.error("Could not request results, please check your internet connection.")
        return None

def get_response(user_input):
    """Get bot response from predefined answers or Mistral API"""
    user_input = user_input.lower().strip()

    for question, response in predefined_responses.items():
        if question.lower().strip() == user_input:
            return response

    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "mistral-tiny", "messages": [{"role": "user", "content": user_input}]}
    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error: Unable to fetch response from Mistral API."

def text_to_speech(response_text):
    """Speak the response synchronously"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(response_text)
    engine.runAndWait()

# Streamlit UI
st.title("🎤 AI Voice Bot")

st.write("Click the button below and speak.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if st.button("Speak Now"):
    user_input = speech_to_text()
    if user_input:
        bot_response = get_response(user_input)
        
        st.session_state.conversation.append(("You", user_input))
        st.session_state.conversation.append(("Bot", bot_response))

        for speaker, message in st.session_state.conversation:
            st.subheader(f"**{speaker}:**")
            st.write(message)

        # Speak the response
        text_to_speech(bot_response)
