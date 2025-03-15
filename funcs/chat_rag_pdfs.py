from langchain_core.prompts import ChatPromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
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
    persist_directory="./vectordb/chroma_langchain_db",  # Where to save data locally
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
                        persist_directory="./vectordb/chroma_langchain_db",  # Where to save data locally
                    )
    
    #Create RetrievalQA Chain
    retriever = vector_store.as_retriever(kwargs={"k": 10})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type = "stuff",
        retriever = vector_store.as_retriever()
    )
    response = qa_chain.invoke(user_chat)
    #response = retriever.invoke(user_chat)
    #return is object {'query': '<question>', 'result': "<answer>"}
    return response['result']
        
# Run the main loop
if __name__ == "__main__":
    user_chat = 'Tell me about half marathon running'
    response = get_rag_response(user_chat)
    print(response)