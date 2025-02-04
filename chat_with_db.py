from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase

# Load environment variables
load_dotenv()

# Define MySQL connection URI
mysql_uri = 'mysql+mysqlconnector://root:7913qpzm&@localhost:3306/llm_everykmcounts'

# Load the database
db = SQLDatabase.from_uri(mysql_uri)

# Function to retrieve and format the schema as a string
def get_schema(db):
    try:
        table_infos = db.get_table_info()
        schema_lines = []
        for table_name, columns in table_infos.items():
            column_names = ", ".join(columns.keys())  # Extract column names as a comma-separated string
            schema_lines.append(f"Table: {table_name}\nColumns: {column_names}")
        return "\n".join(schema_lines)
    except Exception as e:
        print(f"Error processing schema: {e}")
        return ""

###CREATE A SQL CHAIN###
# Define the SQL query generation template
template = """
Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query: 
"""

# Create the prompt template
prompt = ChatPromptTemplate.from_template(template)

# Initialize the LLM
llm = ChatOpenAI()

# Define the SQL chain
sql_chain = (
    RunnablePassthrough.assign(schema=lambda inputs: get_schema(db))  # Get schema as string
    | prompt  # Format the input
    | llm.bind(stop=["SQLResult:"])  # Pass it to the LLM
    | StrOutputParser()  # Parse the output
)

###CREATE THE FULL CHAIN###
response_template = """Based on the table schema below, question, sql query, and sql response, 
write a summarize response base on the SQL response in short, clear:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
prompt_response = ChatPromptTemplate.from_template(response_template)

#Run query
def run_query(query):
    return db.run(query)

#Define the chain
full_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        schema=lambda inputs: get_schema(db),
        response=lambda vars: run_query(vars["query"]),
    )
    | prompt_response
    #| model = llm
)

# Main function to test the chain
if __name__ == "__main__":
    #Print the đatabase scheme
    print(get_schema(db))
    # User question
    user_question = "how many strava activity id do activites have?"
    
    # Run the chain
    response = sql_chain.invoke({"question": user_question})
    
    # Print the SQL query generated
    print("Generated SQL Query:")
    print(response)

    #Print the full chain
    user_response = full_chain.invoke({"question": user_question})
    print(user_response)

    #print(db.run("SELECT COUNT(*) AS total_activity FROM activity"))
