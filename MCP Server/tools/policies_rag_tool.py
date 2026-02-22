import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY', '').strip()
if openai_api_key:
    os.environ['OPENAI_API_KEY'] = openai_api_key


embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def policies_rag_tool(question: str) -> str:
    """
      Ask a question using the RAG.
      User can ask a question about our company and get the answer from the RAG.

      Args:
          question (str): The question to ask

      Returns:
          str: The answer to the question


    """
    faiss_db_path = os.path.join(os.path.dirname(__file__), "rag", "faiss_db")
    docsearch = FAISS.load_local(faiss_db_path, embeddings, allow_dangerous_deserialization=True)
    retriever = docsearch.as_retriever(search_kwargs={"k": 5})

    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    return context
