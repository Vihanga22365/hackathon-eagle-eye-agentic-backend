import os
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key

def web_search_tool(search_query: str):
    """
    Perform an online web search.
    
    Parameters:
        search_query (str): The search query.
    
    Returns:
        dict: The search results in JSON format.
    """
    llm = ChatOpenAI(model="gpt-4o-mini")

    tool = {"type": "web_search_preview"}
    llm_with_tools = llm.bind_tools([tool])

    response = llm_with_tools.invoke(search_query)
    return response 