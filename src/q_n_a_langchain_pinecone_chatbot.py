# Loading the Packages
import tqdm
from genericpath import exists
import time
import os
from warnings import WarningMessage
import langchain
from openai import OpenAI
import pinecone
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

print(f"all the packages loaded")

## Configure .env file
from dotenv import find_dotenv, load_dotenv

env_file = load_dotenv(find_dotenv(), override=True)
if env_file:
    print(f".env file is loaded\n")
else:
    raise KeyError(".env file not found")

## Configure all the APIs
### Pinecone API
api_key_pinecone = os.environ.get("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key_pinecone)
if pc:
    print("Pincone API successfull")
else:
    raise KeyError("Pinecone API Failed")

### OpenAI API
api_key_openai = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key_openai)
if client:
    print("OpenAI API successfull")
else:
    raise KeyError("OpenAI API Failed")

## Function - for converting Files into Document Loader
def load_document(file: str):
    """This function takes the file path of types (.csv, pdf, docs or docx) and converts into Document Loader using Langchain
    file: Pass on the file path in string format.
    """

    ### Splitting the file into file_name and file_extension
    name, extension = os.path.splitext(file)
    print(
        f"Your File is ready! Name of the file is: {name} and extension detected: {extension}\n"
    )

    ### For .pdf extension
    if extension == ".pdf":
        from langchain.document_loaders import PyPDFLoader

        loader = PyPDFLoader(file_path=file)
        print("File Converted into Document Loader")

    elif extension == ".docs" or ".docx":
        from langchain.document_loaders import Docx2txtLoader

        loader = Docx2txtLoader(file_path=file)
        print("File Converted into Document Loader")

    elif extension == ".csv":
        from langchain.document_loaders import CSVLoader

        loader = CSVLoader(file_path=file)

    else:
        print (f"File Type Not Supported")

    data = loader.load()
    return data


## Function - for Converting loaders into Chunks
def chunk_data(data, chunk_size: int = 256):
    '''This function will convert the document loader into chunks
    '''
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=0
    )

    chunks = text_splitter.split_documents(data)
    print(f"Chunking Completed! Ready for Embedding")
    return chunks

## Function - Turning Chunks to Embeddings and creating Index in Pinecone DB. Storing Embeddings into Pinecone DB.
def insert_embeddings(index_name: str, file:str):
    """This Function will create a new index and store the embeddings and chunks inside it. If the index already exists then it will store the embeddings inside it.
    index_name: Name of new index for creation
    chunks: pass on the embeddings
    """

    if index_name in pc.list_indexes().names():
        print(f"Index {index_name} already exists")
        data = load_document(file=file)
        chunks = chunk_data(data=data)
        ## Embedding - through OpenAI Embedding Models
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1536)
        print("Embedding completed!")
        vector_store = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)
        print(f"Stored in Index {index_name}")
        return vector_store

    ## INSERT EMBEDDINGS
    else:
        data = load_document(file=file)
        chunks = chunk_data(data=data)
        ## Embedding - through OpenAI Embedding Models
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1536)
        print("Embedding completed!")

        ### If the index doesn't exists
        print(
            f"Index {index_name} doesn't exists, Creating Index and embeddings ...",
            end="",
        )
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

        vector_store = PineconeVectorStore.from_documents(documents=chunks, embedding=embeddings, index_name=index_name)
        print(f"Chunks and embeddings and inserted in Pinecone index {index_name}")
        return vector_store

# Select Index Name for creation
index_name = input("Enter Index Name for new index creation: ")
# Pass the file 
file = input("Enter File Path with file name and extension: ")
if index_name and file: 
    vector_store = insert_embeddings(index_name=index_name, file=file)
    print(f"Vector Store Generated")
else:
    print("Specify the correct File Path")
    

def ask_and_get_answer(vector_store, q):
    """func ask_and_get_answer allows a user to ask questions and get answers from vector_stores (where our document knowledge is stored) and generation of answer will happen with the help of LLMs.
    LLM used for this case: OpenAI GPT model.
    vector_store: Knowledge Base stored in Pinecone DB
    q: Query or Question by users
    """
    import langchain
    from langchain.chains import RetrievalQA
    from langchain_openai import ChatOpenAI

    # LLM Used
    llm = ChatOpenAI(model="gpt-4o", temperature=1, n=1)

    # Retreiving the information from knowledge source/base
    retriever = vector_store.as_retriever(search_type="similarity", # using similarity search
                                          search_kwargs={"k":5}) #k = 5 Top 5 similar results

    chain = RetrievalQA.from_chain_type(llm=llm, 
                                        chain_type="stuff", # how the retrieved data is processed, all the retrieved text is fed into the prompt for the LLM. 
                                        retriever=retriever)

    answer = chain.invoke(q)
    return answer

### Let's make the Chatbot/QnA 
i=1
print("Welcome to QnA Chatbot powered by OpenAI, feel free to ask questions or type ['quit'] to exit")
while True:
    q = input(str(f"User Question #{i}: "))
    if q.lower().strip() not in ['quit', 'exit', 'bye']:
        answer = ask_and_get_answer(vector_store=vector_store, q=q)
        print(f"GPT Answer {i}: {answer['result']}")
        print(f"\n {"-"*100} \n")
        i+=1 
        continue    

    elif q.lower().strip() in ['quit', 'exit', 'bye']:
        print('Quitting the Application')
        time.sleep(2)
        print("Bye")
        break

    else:
        print("Enter the query properly")
        time.sleep(2)
        print("Restart the App")
        break
