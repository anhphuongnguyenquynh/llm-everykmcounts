import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain_chroma import Chroma
import pandas as pd
import logging
from sqlalchemy import create_engine
from chat_rag_pdfs_func import get_rag_response
from user_query_routing_func import question_routing
from get_activity_strava_func import get_bearer_token, get_activities
from update_activity_mysqldb import json_to_df, reformat_dataframe, update_df_mysql_db
from chat_with_db_func import answer_user_question
import requests
import random

from dotenv import load_dotenv

load_dotenv()

st.title("everykmcounts :runner:")

##STREAMLIT SIDEBAR
with st.sidebar:
    #Button connect with Strava
    #st.link_button(label = "Connect with Strava", 
    #               url = "https://www.strava.com/oauth/authorize?client_id=130686&response_type=code&redirect_uri=http://localhost:8501/exchange_token&approval_prompt=force&scope=activity:read_all")
    st.markdown("<a href = \"https://www.strava.com/oauth/authorize?client_id=130686&response_type=code&redirect_uri=http://localhost:8501/&approval_prompt=force&scope=activity:read_all\" target= '_self' >Connect with Strava </a>", unsafe_allow_html=True)
    

    # if "code" in st.query_params:
    #     response = requests.post("http://localhost:8001/connect-with-strava", json={"code": st.query_params["code"]})
    #     st.write(response.json()) # token
    #     st.write("Connect with strava successfully :'>")
    #     #st.write(st.query_params["code"])
    
    # if "token" in session:
    #     requests.get('http://localhost:8001/user_info', { headers={token: session.token} })
    
    #Connect with strava => User authorize => Save code to get access token => Use access token to get athlete activity => Update to mysql DB
    if "code" in st.query_params:
        strava_code = st.query_params["code"]
        #st.write(strava_code, 'strava_code')
        #1.Get activity from strava
        ##1.1Get access token
        access_token = get_bearer_token(strava_code)
        #st.write(access_token, 'access_token')
        ##1.2Get activity
        activities = get_activities(access_token=access_token)
        #st.write(activities)

        #2.Update to mysql database
        ##2.1 Convert to dataframe
        df_activities = json_to_df(activities)
        #st.write(df_activities)

        ##2.2 Reformat dataframe prepare for update mysql database
        format_df = reformat_dataframe(df_activities)
        #st.write(format_df)

        ##2.2 Update mysql database
        status_update = update_df_mysql_db(format_df)
        #st.write(status_update)

        st.write("Connect with Strava successfully :sparkles: :sparkles: :sparkles:")
        
    
    #Ask user for runner_type and target
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

#Get greeting response function
def get_greeting_response(user_chat):
    greetings = ["Glad to help you. Share with me your exercises or ask me anything about sport",
                 "Welcome to everykmcounts!"]
    return random.choice(greetings)

#Get final response with proper assignment
def get_user_response(user_chat):
    #Routing user query by langchain
    subchain = question_routing(user_chat)

    if subchain == "Sport knowledge":
        return get_rag_response(user_chat)
    if subchain == "Exercises activity log":
        return get_cheer_response(user_chat)
    if subchain == "Greeting":
        return get_greeting_response(user_chat)
    if subchain == "Ask data":
        return answer_user_question(user_chat)
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

