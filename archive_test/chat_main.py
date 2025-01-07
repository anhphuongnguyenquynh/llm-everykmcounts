import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain_chroma import Chroma
from chat_chroma import get_rag_response  # Assuming this function retrieves RAG response
from langchain_routing import question_routing
from dotenv import load_dotenv

load_dotenv()

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="everykmcounts", page_icon=":runner:")

st.title("everykmcounts")

with st.sidebar:
    type_runner_option = st.selectbox(
        "Which type describe you best?",
        ("I am newbie", "I regularly do exercises", "I am professional")
    )
    target_option = st.selectbox(
        "Which target describe you want best?",
        ("I want to do exercises more frequently",
         "I want to join a race in the next few months",
         "I practice frequently, I want to keep track my performance")
    )
    tone_voice_option = st.selectbox(
        "Which personality would you like everykmcounts to have?",
        ("Happy", "Angry"),
    )


# Show conversation history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

    else:
        with st.chat_message("AI"):
            st.markdown(message.content)


# Get cheer response function
def get_cheer_response(user_question):
    ##query = persona + instruction + context + data_format + audience + tone + data
    template = """
    You are a runner helpful assistant give me a courage sentence. 
    I {{type_runner_option}}. My target is {{target_option}}, give me a sentence support when I finish a run.
    The tone should be {{tone_voice_option}} and short.

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI()

    cheerchain = prompt | llm | StrOutputParser()

    cheer_response = cheerchain.invoke({
        "user_question": user_question})
    # response = chain.run(user_chat)
    return cheer_response


# Get final response function with proper assignment
def get_final_response(user_chat):
    # Query Routing by langchain
    subchain = question_routing(user_chat)

    # Navigate based on user chat
    if subchain == "Exercise activity log":
        return get_cheer_response(user_chat)
    if subchain == "Sport knowledge":
        return get_rag_response(user_chat)
    if subchain == "Other":
        other_sentence = "Sorry! I don't know about this topic"
        return other_sentence


user_chat = st.chat_input("Your message")
if user_chat is not None and user_chat != "":
    st.session_state.chat_history.append(HumanMessage(user_chat))

    with st.chat_message("Human"):
        st.markdown(user_chat)

    with st.chat_message("AI"):
        st.markdown(get_final_response(user_chat))