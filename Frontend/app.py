import streamlit as st
from langchain_core.messages import BaseMessage,HumanMessage
import uuid



from Backend.graph import chatbot,all_thread
# **********************Utils*****************
def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
        chat_name(thread_id)

def load(thread_id):
    state = chatbot.get_state(
        config={
            'configurable': {
                'thread_id': thread_id
            }
        }
    )
    return state.values.get('messages', [])

def chat_name(thread_id):
    if thread_id not in st.session_state["chat_name_dict"]: 
        chat_number = len(st.session_state["chat_name_dict"]) + 1
        st.session_state["chat_name_dict"][thread_id] = (
            f"Chat - {chat_number}"
        )

# *********************Session startup*************


if 'chat_name_dict' not in st.session_state:
    st.session_state['chat_name_dict'] = {}


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = all_thread()

for thread_id in st.session_state["chat_threads"]:
    chat_name(thread_id)

add_thread(st.session_state['thread_id'])
# *************** Sidebar UI ***********

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()



st.sidebar.header("My Conversations")

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(st.session_state['chat_name_dict'][thread_id]):
        st.session_state['thread_id'] = thread_id
        messages = load(thread_id)
        temp_messages = []
        for message in messages:
            if isinstance(message,HumanMessage):
                role = 'user'
            else :
                role = 'assistant'
            temp_messages.append({'role':role,'content':message.content})
        st.session_state['message_history'] = temp_messages


# **************ChatBot UI**************


with st.chat_message('assistant'):
    st.text('How can i help you')

for i in st.session_state['message_history']:


    with st.chat_message(i.get('role')):
        st.text(i.get('content'))
    

user_input = st.chat_input("Type Here")
if user_input:    
    if(user_input == 'bye'):
        with st.chat_message("assistant"):
            st.text("Goodbye! Have a great day!")
    with st.chat_message("User"):
        st.text(user_input)
        st.session_state['message_history'].append({'role':"User","content":user_input})
        
    with st.chat_message('assistant'):
        config = {'configurable':{'thread_id':st.session_state['thread_id']}}
        ai_message = st.write_stream(
            message_chunk.content for message_chunk,metdata in chatbot.stream(
            {"messages": [user_input]},
            config = config,
            stream_mode = 'messages'
            )
        )

        st.session_state['message_history'].append({'role':"assistant","content":ai_message})


