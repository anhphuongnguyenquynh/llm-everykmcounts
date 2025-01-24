from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

##Add classify 'Performance question' & 'Greeting'
def question_routing(question):
    classification_template = PromptTemplate.from_template(
    """You are good at classifying a question.
    Given the user question below, classify it as either being about `Exercises activity log`, `Sport knowledge`, 'Greeting' or 'Other'.

    <If the question is about complete an exercise, or user activity log, classify the question as 'Exercises activity log'>
    <If the question is about sport, running, swimming, cycling and similar topics, classify it as 'Sport knowledge'>
    <If the question is about greeting, classify the question as 'Greeting'>
    <If the question is about whether or anything not related to sport, classify the question as 'Other'>

    <question>
    {question}
    </question>

    Classification:"""
    )
    
    classification_chain = classification_template | ChatOpenAI() | StrOutputParser()
    result = classification_chain.invoke({"question": question})
    
    return result

#Test
result1 = question_routing("How to cook potato?")
print(result1)

result2 = question_routing("I run 2km today")
print(result2)

result3 = question_routing("Half marathon training plan")
print(result3)

result4 = question_routing("Goodbye")
print(result4)

