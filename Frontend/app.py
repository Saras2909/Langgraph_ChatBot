import streamlit as st
from langchain_core.messages import HumanMessage,AIMessageChunk,ToolMessage
import uuid
from Backend.graph import chatbot, all_thread
# ===================== Utils =====================

def generate_thread_id():
    return str(uuid.uuid4())


def chat_name(thread_id):
    if thread_id not in st.session_state["chat_name_dict"]:
        chat_number = len(st.session_state["chat_name_dict"]) + 1
        st.session_state["chat_name_dict"][thread_id] = f"Chat - {chat_number}"


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)
        chat_name(thread_id)


def reset_chat():
    thread_id = generate_thread_id()

    st.session_state["thread_id"] = thread_id
    st.session_state["message_history"] = []

    add_thread(thread_id)


def load_chat(thread_id):
    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return state.values.get("messages", [])


# ===================== Session Startup =====================

if "chat_name_dict" not in st.session_state:
    st.session_state["chat_name_dict"] = {}

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = all_thread()

# Create names for existing threads
for thread_id in st.session_state["chat_threads"]:
    chat_name(thread_id)

# Add current thread if it doesn't exist
add_thread(st.session_state["thread_id"])


# ===================== Sidebar =====================

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("➕ New Chat"):
    reset_chat()
    st.rerun()


st.sidebar.header("My Conversations")

for thread_id in reversed(st.session_state["chat_threads"]):

    chat_title = st.session_state["chat_name_dict"][thread_id]

    if st.sidebar.button(chat_title, key=f"chat_{thread_id}"):

        st.session_state["thread_id"] = thread_id

        messages = load_chat(thread_id)
        temp_messages = []

        for message in messages:

            if isinstance(message, HumanMessage):
                role = "user"
            else:
                role = "assistant"

            # Skip tool messages if they appear in history
            if isinstance(message, ToolMessage):
                continue

            if message.content:
                temp_messages.append(
                    {
                        "role": role,
                        "content": message.content
                    }
                )

        st.session_state["message_history"] = temp_messages

        st.rerun()


# ===================== Chat UI =====================

# Show previous messages
if not st.session_state["message_history"]:

    with st.chat_message("assistant"):
        st.write("How can I help you?")

else:

    for message in st.session_state["message_history"]:

        with st.chat_message(message["role"]):
            st.write(message["content"])


# ===================== User Input =====================

user_input = st.chat_input("Type here...")
if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input
        }
    )


    if user_input.lower() == "bye":
        ai_message = "Goodbye! Have a great day! 👋"
        with st.chat_message("assistant"):
            st.write(ai_message)
        st.session_state["message_history"].append(
            {
                "role": "assistant",
                "content": ai_message
            }
        )
    else:
        config = {
            "configurable": {
                "thread_id": st.session_state["thread_id"]
            }
        }
        # ===================== AI Streaming =====================
        with st.chat_message("assistant"):
            status_holder = {"box": None}
            def ai_only_stream():
                for message_chunk, metadata in chatbot.stream(
                    {
                        "messages": [
                            HumanMessage(content=user_input)
                        ]
                    },
                    config=config,
                    stream_mode="messages",
                ):
                    # Tool execution
                    if isinstance(message_chunk, ToolMessage):
                        tool_name = getattr(
                            message_chunk,
                            "name",
                            "tool"
                        )
                        if status_holder["box"] is None:
                            status_holder["box"] = st.status(
                                f"🔧 Using `{tool_name}`...",
                                expanded=True
                            )
                        else:
                            status_holder["box"].update(
                                label=f"🔧 Using `{tool_name}`...",
                                state="running",
                                expanded=True
                            )
                    # AI text streaming
                    elif isinstance(message_chunk, AIMessageChunk):
                        if message_chunk.content:
                            # Sometimes content can be a list
                            if isinstance(message_chunk.content, str):
                                yield message_chunk.content
            ai_message = st.write_stream(ai_only_stream())
            # Tool completed
            if status_holder["box"] is not None:
                status_holder["box"].update(
                    label="✅ Tool finished",
                    state="complete",
                    expanded=False
                )
        # ===================== Save AI Message =====================
        if ai_message:
            st.session_state["message_history"].append(
                {
                    "role": "assistant",
                    "content": ai_message
                }
            )