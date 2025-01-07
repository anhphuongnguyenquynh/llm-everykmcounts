from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_routing import question_routing
from chat_chroma import get_rag_response 
from dotenv import load_dotenv

load_dotenv()
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

if __name__ == '__main__':
    type_runner_option = "I am newbie"
    target_option = "I want to do exercises more frequently"
    tone_voice_option = "Happy"
    user_chat_1 = 'Tell me about half marathon running'
    user_chat_2 = 'I run 2km today'
    user_chat_3 = 'How to cook Potato?'
    
    #Test routing
    user_route_1 = get_user_response(user_chat_1)
    print(user_route_1)
    user_route_2 = get_user_response(user_chat_2)
    print(user_route_2)
    user_route_3 = get_user_response(user_chat_3)
    print(user_route_3)

    #Test function
    res_1 = get_rag_response(user_chat_1)
    print(res_1)
    res_2 = get_cheer_response(user_chat_2)
    print(res_2)
