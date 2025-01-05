from langchain_core.prompts import ChatPromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
#from langchain.chains.combine_documents import create_stuff_documents_chain
#from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

# Initialize the models
embeddings = OpenAIEmbeddings()
llm = ChatOpenAI()

# Initialize the vector store
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./db/chroma_langchain_db",  # Where to save data locally
)

#Retriever
retriever = vector_store.as_retriever(kwargs={"k": 10})

#get response from rag
def get_rag_response(user_chat):
    #Initialize the models
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()

    #Initialize the vector store
    vvector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./db/chroma_langchain_db",  # Where to save data locally
    )
    
    #Retriever
    retriever = vector_store.as_retriever(kwargs={"k": 10})

    response = retriever.invoke(user_chat)

    return response
        
# Run the main loop
if __name__ == "__main__":
    user_chat = 'Tell me about half marathon running'
    response = get_rag_response(user_chat)
    print(response)