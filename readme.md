# 🤖 LangGraph Chatbot

A conversational AI chatbot built using **LangGraph**, **Streamlit**, and a locally running **Ollama LLM**.

The chatbot supports **multiple conversations**, **persistent chat memory using SQLite**, **AI streaming**, and **tool calling**. It can search the web, perform mathematical calculations, retrieve information from Wikipedia, and read the content of webpages.

---

## ✨ Features

- 💬 Interactive chatbot interface
- 🧠 Conversation memory using LangGraph
- 🗂️ Multiple chat threads
- 💾 Persistent conversation state using SQLite checkpointing
- 🌊 Streaming AI responses
- 🖥️ Streamlit-based user interface
- 🦙 Local LLM support using Ollama
- 🔄 Previous conversations can be loaded from the sidebar
- 🌐 Web search using DuckDuckGo
- 📖 Wikipedia search and summaries
- 🔗 Webpage content extraction
- 🧮 Mathematical calculations using a calculator tool
- 🔧 LangGraph tool calling and conditional routing

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **LangGraph**
- **LangChain**
- **Ollama**
- **SQLite**
- **DuckDuckGo Search (`ddgs`)**
- **Wikipedia**
- **Requests**
- **BeautifulSoup**
- **python-dotenv**

---

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

---

# ⚙️ Installation

## 1. Clone the Repository

Clone the repository and navigate to the project directory:

```bash
git clone <your-repository-url>
cd ChatBot
```

---

## 2. Create a Virtual Environment

Using `uv`:

```bash
uv venv
```

---

## 3. Activate the Virtual Environment

On Linux/macOS:

```bash
source .venv/bin/activate
```

---

## 4. Install Dependencies

Using `uv`:

```bash
uv pip install -r requirements.txt
```

If you do not have a `requirements.txt` file yet, you can generate one using:

```bash
uv pip freeze > requirements.txt
```

---

# 🦙 Install Ollama

Make sure Ollama is installed and running on your system.

Pull the model used in this project:

```bash
ollama pull llama3.2:3b
```

You can verify that Ollama is running with:

```bash
ollama list
```

---

# ▶️ Run the Application

From the project root:

```bash
streamlit run Frontend/app.py
```

Then open the local URL displayed by Streamlit in your browser.

---

# 🧠 How It Works

The application follows this flow:

```text
User
  ↓
Streamlit Frontend
  ↓
LangGraph
  ↓
Chat Node
  ↓
Ollama LLM
  ↓
Tool Required?
  ↓
Yes ───────────────→ Tool Node
  ↓                       ↓
No                      Tool Result
  ↓                       ↓
AI Response ←─────────────
  ↓
Streamlit UI
```

The LangGraph workflow determines whether the AI needs to use a tool.

If a tool is required, the request is routed to the appropriate tool. After receiving the tool result, the conversation returns to the AI model to generate the final response.

---

# 🔧 Available Tools

## 🌐 Web Search

The chatbot can search the web for current information using DuckDuckGo.

The search tool returns:

- Title
- URL
- Search snippet

---

## 🧮 Calculator

The chatbot can perform mathematical calculations.

Supported operations include:

- Addition, subtraction, multiplication, and division
- Parentheses
- Powers using `**`
- Modulo using `%`
- `sqrt()`
- `abs()`
- `round()`
- `sum()`
- `range()`
- Mathematical constants such as `pi` and `e`

Example:

```text
sum(range(1, 101))
```

---

## 📖 Wikipedia Search

The chatbot can search Wikipedia for:

- Definitions
- Historical information
- Famous personalities
- General concepts

The tool returns a short summary of the requested topic.

---

## 🔗 Webpage Content Extraction

When provided with a webpage URL, the chatbot can fetch and extract the text content from the page.

The tool:

1. Fetches the webpage
2. Removes unnecessary elements such as scripts and styles
3. Extracts readable text
4. Limits the output to prevent excessive LLM context usage

---

# 💾 Conversation Memory

Each conversation is assigned a unique `thread_id`.

```text
Conversation
      ↓
thread_id
      ↓
LangGraph Checkpointer
      ↓
SQLite Database
```

The application uses LangGraph's `SqliteSaver` to persist conversation checkpoints.

This allows previous conversations to be retrieved and loaded later.

---

# 🗂️ Multiple Chat Threads

Users can create multiple conversations using the sidebar.

```text
Sidebar
│
├── ➕ New Chat
│
└── My Conversations
    ├── Chat - 1
    ├── Chat - 2
    ├── Chat - 3
    └── ...
```

Each chat has its own unique `thread_id`.

The chatbot retrieves existing conversation threads from the SQLite checkpoint database when the application starts.

---

# 🌊 Streaming Responses

AI responses are streamed directly to the Streamlit interface.

Instead of waiting for the complete response, text is displayed progressively as it is generated.

```text
LLM
 ↓
AI Message Chunks
 ↓
LangGraph Stream
 ↓
Streamlit write_stream()
 ↓
User Interface
```

---

# 🔧 Tool Execution

When the AI decides that a tool is required, LangGraph routes the request through a `ToolNode`.

```text
Chat Node
    ↓
tools_condition
    ↓
┌───────────────┐
│ Tool Required │
└───────────────┘
    ↓       ↓
   Yes      No
    ↓        ↓
Tool Node   END
    ↓
Chat Node
```

The Streamlit interface displays tool execution status while the chatbot processes the request.

---

# 📚 Learning Purpose

This project was built to learn and practice:

- LangGraph state management
- Building graph-based AI workflows
- LangGraph conditional edges
- Tool calling with LangChain
- `ToolNode` and `tools_condition`
- Conversation threads
- Persistent memory
- SQLite checkpointing
- Local LLMs using Ollama
- Streaming AI responses
- Streamlit session state
- Web search integration
- Wikipedia integration
- Webpage content extraction

---

# 🚀 Future Improvements


---

## 📌 Notes

- The project currently uses the local Ollama model:

```text
llama3.2:3b
```

- Ollama must be running before starting the Streamlit application.
- Conversation data is stored locally using SQLite.
- Chat threads are identified using unique UUID-based `thread_id` values.

---

Built as part of my journey into **Agentic AI and LLM Application Development**. 🤖🚀