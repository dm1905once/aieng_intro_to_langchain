from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_chroma import Chroma
from langchain_core.tools import tool
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

# Define tools
@tool("PlanetDistanceSun")
def planet_distance_sun_tool(planet_name: str) -> str:
    match planet_name.lower():
        case "earth":
            return "Earth is approximately 1 AU from the Sun."
        case "mars":
            return "Mars is approximately 1.5 AU from the Sun."
        case "jupiter":
            return "Jupiter is approximately 5.2 AU from the Sun."
        case "pluto":
            return "Pluto is approximately 39.5 AU from the Sun."
        case _:
            return f"Information about the distance of {planet_name} from the Sun is not available in this tool."

@tool("PlanetRevolutionPeriod")
def planet_revolution_period_tool(planet_name: str) -> str:
    match planet_name.lower():
        case "earth":
            return "Earth takes approximately 1 Earth year to revolve around the Sun."
        case "mars":
            return "Mars takes approximately 1.88 Earth years to revolve around the Sun."
        case "jupiter":
            return "Jupiter takes approximately 11.86 Earth years to revolve around the Sun."
        case "pluto":
            return "Pluto takes approximately 248 Earth years to revolve around the Sun."
        case _:
            return f"Information about the revolution period of {planet_name} is not available in this tool."

@tool("PlanetGeneralInfo")
def planet_general_info_tool(planet_name : str) -> str:
    results = db.similarity_search(planet_name)
    if results:
        return results[0].page_content
    else:
        return f"Additional information for {planet_name} is not available in this tool."

# Run queries
