from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

classification_template = PromptTemplate.from_template(
    """You are good at classifying a question.
    Given the user question below, classify it as either being about `Exercises activity log`, `Sport knowledge` or 'Other'.

    <If the question is about complete an exercise, or user activity log classify the question as 'Exercises activity log'>
    <If the question is about sport, running, swimming, cycling and similar topics, classify it as 'sport knowledge'>
    <If the question is about whether or anything not related to sport, classify the question as 'Other'>

    <question>
    {question}
    </question>

    Classification:"""
)

classification_chain = classification_template | ChatOpenAI() | StrOutputParser()

#Test
result1 = classification_chain.invoke({"question": "How to cook potato?"})
print(result1)

result2 = classification_chain.invoke({"30 minutes practice yoga in this morning"})
print(result2)

result3 = classification_chain.invoke({"question": "How to run 10km"})
print(result3)