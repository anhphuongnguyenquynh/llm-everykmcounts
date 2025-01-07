import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain_chroma import Chroma
from chat_chroma import get_rag_response
from langchain_routing import question_routing
from dotenv import load_dotenv

load_dotenv()

st.title("everykmcounts :runner:")

##SIDEBAR
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

##FUNCTION GET RESPONSE
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

#Get final response with proper assignment
def get_user_response(user_chat):
    #Routing user query by langchain
    subchain = question_routing(user_chat)

    if subchain == "Sport knowledge":
        return get_rag_response(user_chat)
    if subchain == "Exercises activity log":
        return get_cheer_response(user_chat)
    if subchain == "Other":
        other_sentence = "I don't know about this topic"
        return other_sentence    
    
    
##CHATBOT INTERFACE
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_chat := st.chat_input("Log your exercise activity today. Ask me anything about sports."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_chat})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_chat)
    
    response = get_user_response(user_chat)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

