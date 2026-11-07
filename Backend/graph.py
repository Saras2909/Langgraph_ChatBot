from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
import sqlite3

from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver


model = ChatOllama(model="llama3.2:3b")


class ChatMessages(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatMessages):
    response = model.invoke(state["messages"])
    return {"messages": [response]}


conn = sqlite3.connect(
    "chatbot.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(conn)


graph = StateGraph(ChatMessages)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


chatbot = graph.compile(checkpointer=checkpointer)


def all_thread():
    all_threads = []

    for checkpoint in checkpointer.list(None):
        thread_id = checkpoint.config["configurable"].get("thread_id")

        if thread_id and thread_id not in all_threads:
            all_threads.append(thread_id)

    return all_threads[::-1]