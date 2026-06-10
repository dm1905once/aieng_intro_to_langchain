# Write your solution below
# install the required packages:
# pip install langchain-core python-dotenv langchain-openai

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import dotenv
import os

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    base_url=os.getenv("BASE_URL")
)

question = input()
template = PromptTemplate.from_template(
    """
    You are a helpful assistant who answers questions about planets in the solar system users may have. You are asked: {planet}.
    Your answer should be 4 lines, each line providing details about the following aspects:
        Physical characteristics of the planet (size, composition, atmosphere);
        Notable features of the planet (rings, moons, surface conditions)
        Scientific or historical significance about the planet
        Fun or surprising facts about the planet
    """
)

prompt = template.invoke({"planet": question})
response = llm.invoke(prompt)
print(response.content)