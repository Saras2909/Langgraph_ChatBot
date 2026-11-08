from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
import sqlite3
from langchain_ollama import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import BaseMessage
from langchain.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
import math
from ddgs import DDGS
import wikipedia
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
model = ChatOllama(model = 'llama3.2:3b')
wikipedia.set_lang("en")



#------------------------Tools-------------------
#Tools
@tool
def search_tool(query: str) -> str:
    """Search the web for current information."""

    results = DDGS().text(query, max_results=5)

    return "\n\n".join(
        f"Title: {r['title']}\n"
        f"URL: {r['href']}\n"
        f"Snippet: {r['body']}"
        for r in results
    )

@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression accurately.

    Use this tool whenever numerical calculation or arithmetic is required.

    Supported:
    - Basic arithmetic: +, -, *, /, %, **
    - Parentheses: ( )
    - Mathematical functions: sqrt(), abs(), round()
    - Common aggregation functions: sum()
    - Constants: pi, e
    - Python functions: range() can be used with sum()

    Examples:
    - "5000000 * (0.085 / 12)"
    - "100 * 101 / 2"
    - "sum(range(1, 101))"
    - "sqrt(144)"
    - "2 ** 10"
    - "round(10 / 3, 2)"

    Do not use this tool for web searches, factual questions,
    Wikipedia lookups, or text processing.
    """

    try:
        allowed_globals = {
            "__builtins__": {},
            "sqrt": math.sqrt,
            "abs": abs,
            "round": round,
            "sum": sum,
            "range": range,
            "pi": math.pi,
            "e": math.e,
        }

        result = eval(expression, allowed_globals, {})

        return str(result)

    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


@tool
def search_wikipedia(query: str) -> str:
  """Searches Wikipedia and returns a short summary of the topic.

  Use this for factual definitions, historical context, famous personalities,
  and concepts.
  """
  try:
    summary = wikipedia.summary(query, sentences=4)
    return summary
  except wikipedia.exceptions.DisambiguationError as e:
    return f"Topic is too broad. Did you mean one of these? {', '.join(e.options[:5])}"
  except wikipedia.exceptions.PageError:
    return "No Wikipedia page found for this topic."
  except Exception as e:
    return f"Error querying Wikipedia: {str(e)}"


@tool
def fetch_webpage_text(url: str) -> str:
  """Fetches a webpage URL and extracts its main text content.

  Use this to read full articles or web pages when given a specific link.
  """
  headers = {"User-Agent": "Mozilla/5.0"}
  try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script and style tags
    for element in soup(["script", "style", "nav", "footer"]):
      element.decompose()

    text = soup.get_text(separator=" ", strip=True)
    # Truncate output to prevent hitting LLM context limits
    return text[:4000]
  except Exception as e:
    return f"Failed to retrieve page content: {str(e)}"
tools = [fetch_webpage_text,search_tool,calculator,search_wikipedia]

chatbot_with_tools = model.bind_tools(tools)

#--------------------Schema(State)----------------

class ChatMessages(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


#Chat node functions
def chat_node(state:ChatMessages) -> ChatMessages:
    response = chatbot_with_tools.invoke(state['messages'])
    return {"messages":[response]}


conn = sqlite3.connect(
    "chatbot.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(conn)
tool_node = ToolNode(tools)

#------------Graph---------------
graph = StateGraph(ChatMessages)
graph.add_node("chat_node",chat_node)
graph.add_node("tool_node",tool_node)

graph.add_edge(START,"chat_node")
graph.add_conditional_edges(
    "chat_node",
    tools_condition,
    {
        "tools": "tool_node",
        END: END
    }
)
graph.add_edge("tool_node", "chat_node")

chatbot = graph.compile(checkpointer=checkpointer)

#----------------To Retrieve Existing Chats------------------
def all_thread():
    all_threads = []

    for checkpoint in checkpointer.list(None):
        thread_id = checkpoint.config["configurable"].get("thread_id")

        if thread_id and thread_id not in all_threads:
            all_threads.append(thread_id)

    return all_threads[::-1]
