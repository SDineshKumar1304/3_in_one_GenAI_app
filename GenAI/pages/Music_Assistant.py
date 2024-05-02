import streamlit as st
import google.generativeai as genai
import base64

st.title("GenAI Music Assistant🤖💕")
st.markdown(
    """
    <style>
        /* All text */
        body, .css-1akv8q1, h1, .stApp div[data-testid="stText"], .stTextInput, .stTextArea, .stSelectbox, .stButton, .stMarkdown {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)



st.balloons()

instructions="You are Expert in Music Composing  , You have to  write songs in any language in a polite manner"



with open("C:\\Users\\svani\\Downloads\\GenAI-Hackathon\\keys\\DS.Key.txt") as f:
    api_key = f.read()

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=instructions
)

if "memory" not in st.session_state:
    st.session_state["memory"] = []

chat = model.start_chat(history=st.session_state["memory"])

def show_chat_history(chat):
    for message in chat.history:
        sender = "AI" if message.role == "model" else "You"
        st.markdown(f'<p style="color:white;">{sender}: {message.parts[0].text}</p>', unsafe_allow_html=True)

st.markdown('<p style="color:white;">Hi there! How can I assist you today?</p>', unsafe_allow_html=True)

show_chat_history(chat)

user_input = st.text_input("You: ")

if st.button("Clear Chat"):
    st.session_state["memory"] = []
    st.experimental_rerun()

if user_input:
    st.markdown(f'<p style="color:white;">You: {user_input}</p>', unsafe_allow_html=True)
    try:
        response = chat.send_message(user_input)
        for bot in response:
            st.markdown(f'<p style="color:white;">AI: {bot.parts[0].text}</p>', unsafe_allow_html=True)
        st.session_state["memory"] = chat.history
    except genai.generation_types.StopCandidateException:
        st.markdown('<p style="color:white;">AI: I\'m sorry, I couldn\'t understand that. Can you please provide more specific information?</p>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
