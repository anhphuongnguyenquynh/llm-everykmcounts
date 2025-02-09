import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

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
    

#show conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

#get_response
def get_response(query, chat_history, type_runner_option, target_option, tone_voice_option):
    ##query = persona + instruction + context + data_format + audience + tone + data
    template = """
    You are a runner helpful assistant give me a courage sentence. 
    I {{type_runner_option}}. My target is {{target_option}}, give me a sentence support when I finish a run.
    The tone should be {{tone_voice_option}} and short.

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(
        #input_variables = ["type_runner_option", "target_option", "tone_voice_option"],
        template = template)

    llm = ChatOpenAI()

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "chat_history": chat_history,
        "user_question": query
    })


user_query = st.chat_input("Your message")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = get_response(user_query, st.session_state.chat_history)
        st.markdown(ai_response)
