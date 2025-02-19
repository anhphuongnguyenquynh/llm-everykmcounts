from dotenv import load_dotenv
import os
from os.path import join, dirname
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
#from langchain_core.runnables import RunnablePassthrough
from langchain.schema.runnable import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from operator import itemgetter

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Define MySQL connection URI
mysql_uri = os.environ.get("MYSQL_URI")

# Load the database
db = SQLDatabase.from_uri(mysql_uri)

#LLM model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

#Create a chain
sql_chain = create_sql_query_chain(llm, db)

#Response
sql_response = sql_chain.invoke({"question": "How many activities are there?"})
print(sql_response)

###FUNCTION RUN QUERY
def run_query(query):
    return db.run(query)

test_sql_result = db.run(sql_response)
print(test_sql_result)

#Prompt + Chain to get natural answer
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
)

full_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        result=lambda vars: run_query(vars["query"]),
        )
        | answer_prompt
        | llm
)

user_question = 'how many activities are there?'
test_full_answer = full_chain.invoke({"question": user_question})
print(test_full_answer.content)

def answer_user_question(question: str):
    response = full_chain.invoke({"question": question})
    return response.content

if __name__ == "__main__":
    user_question = "How many activities are there?"
    response = answer_user_question(user_question)
    print(response.content)