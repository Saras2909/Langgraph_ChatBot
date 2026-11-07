
# 🤖 LangGraph Chatbot

A conversational AI chatbot built using **LangGraph**, **Streamlit**, and a locally running **Ollama LLM**.

The application supports multiple conversations, persistent chat threads using SQLite checkpointing, and streaming AI responses.

## ✨ Features

- 💬 Interactive chatbot interface
- 🧠 Conversation memory using LangGraph
- 🗂️ Multiple chat threads
- 💾 Persistent conversation state using SQLite
- 🌊 Streaming AI responses
- 🖥️ Streamlit-based user interface
- 🦙 Local LLM support using Ollama
- 🔄 Previous conversations can be loaded from the sidebar

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **LangGraph**
- **LangChain**
- **Ollama**
- **SQLite**

## 📁 Project Structure

```text
ChatBot/
│
├── Backend/
│   ├── __init__.py
│   └── graph.py
│
├── Frontend/
│   ├── __init__.py
│   └── app.py
│
├── .gitignore
├── requirements.txt
├── README.md
└── chatbot.ipynb
```

## ⚙️ Installation

### 1. Clone the repository

Clone this repository and navigate to the project directory.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

On Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 🦙 Install Ollama

Make sure Ollama is installed and running on your system.

Pull the model used in this project:

```bash
ollama pull llama3.2:3b
```

## ▶️ Run the Application

From the project root:

```bash
python -m streamlit run Frontend/app.py
```

Then open the local URL displayed by Streamlit in your browser.

## 🧠 How It Works

```text
User
  ↓
Streamlit Frontend
  ↓
LangGraph
  ↓
ChatOllama
  ↓
llama3.2:3b
  ↓
AI Response
```

Each conversation is assigned a unique `thread_id`.

LangGraph uses SQLite checkpointing to maintain the conversation state for each thread.

```text
Conversation
      ↓
thread_id
      ↓
LangGraph Checkpointer
      ↓
SQLite
```

## 🚀 Future Improvements

- Automatic chat title generation
- User authentication
- Conversation title persistence
- FastAPI backend
- React frontend
- PostgreSQL database
- Cloud LLM support
- Docker deployment

## 📚 Learning Purpose

This project was built to learn how to work with:

- LangGraph state management
- Conversation threads
- Persistent memory
- SQLite checkpointing
- Local LLMs using Ollama
- Streaming responses
- Streamlit session state

---

Built as part of my journey into **Agentic AI and LLM application development**.