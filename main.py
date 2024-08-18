import configparser
import os
from agents.destination_info import get_destination_data
from streamlit_chat import message

from helpers.helpers import (
    find_question_type,
    answer_non_travel_question,
    get_destination,
    get_location_curiosity
)
import streamlit as st

# Set up API Keys and Configs
config = configparser.ConfigParser()
config.read("config.ini")

OPENAI_API_KEY = config.get("API", "OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Configure streamlit
if "history" not in st.session_state:
    st.session_state.history = []


# Make a function to take in a question and answer:
def generate_answer(question: str) -> str:
    # FInd out if it is a travel question or note
    is_travel_question = find_question_type(question)

    ans = ""
    if not is_travel_question:
        return answer_non_travel_question(question)
    else:
        travel_question_answer = get_destination(question)
        if "false__no_destination" in travel_question_answer:
            ans = answer_non_travel_question(question)
            return ans
        else:
            destination = travel_question_answer
            is_curious = get_location_curiosity(destination=destination, question=question)
            if is_curious:
                ans = answer_non_travel_question(question)
                return ans
            ans = get_destination_data(
                destination=destination, question=question
            )
            return ans


def get_chatbot_reply():
    user_message = st.session_state.input_text
    result = generate_answer(user_message)

    st.session_state.history.append({"message": user_message,
                                     "is_user": True})
    st.session_state.history.append({"message": result,
                                     "is_user": False})


# Streamlit application
st.header("Chatbot for your Next Adventure")

st.markdown("""
    ##### Ask me about anything!
    I work best with travel related questions, and I can find you a tour with real time data!
""")

prompt = st.text_input(placeholder="Enter your message here!",
                       label="Talk to the bot:",
                       key="input_text",
                       on_change=get_chatbot_reply)

for i, chat in enumerate(st.session_state.history):
    message(**chat, key=str(i))



