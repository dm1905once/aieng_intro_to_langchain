from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_chroma import Chroma
import dotenv
import os

# Environment
dotenv.load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    base_url=os.getenv("BASE_URL")
)

# Load documents
loader = DirectoryLoader(
    path="planets/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    show_progress=True
)
documents = loader.load()

# Set up embedding model
embeddings_model = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    base_url=os.getenv("BASE_URL"),
)

# Create vector db
db = Chroma(
    collection_name="planets",
    embedding_function=embeddings_model
)

# add documents
db.add_documents(documents=documents)

# Run queries
query = input()
results = db.similarity_search(query)
print(results[0].page_content)