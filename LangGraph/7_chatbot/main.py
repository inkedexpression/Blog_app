import streamlit as st
from backend import chatbot ,model , reterive_threads
from langchain_core.messages import HumanMessage , SystemMessage , AIMessage
import uuid


# =============================== utility function =============================================================================
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)

def load_conversation(thread_id):
    state  = chatbot.get_state(config={'configurable':{'thread_id':thread_id}})
    return state.values.get('messages',[])

def generate_title(user_input):
    messages = [
        SystemMessage(content="""Generate a very short title (max 5 words) 
        for a conversation that starts with this message. 
        Return ONLY the title. No quotes. No explanation."""),
        HumanMessage(content=user_input)
    ]
    response = model.invoke(messages)

    return response.content.strip()
# =============================== session state =============================================================================

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread'] = reterive_threads()

add_thread(st.session_state['thread_id'])

if 'chat_title' not in st.session_state:
    st.session_state['chat_title'] = {}
# ============================================sidebar UI============================================================================

st.sidebar.markdown(
    '<h1 style = color:#b6e3bf> ARIA✨</h1>',
    unsafe_allow_html=True
)

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.markdown('##### My Conversation')

for thread_id in st.session_state['chat_thread'][::-1]:
    title = st.session_state['chat_title'].get(thread_id,"New Conversation")

    if st.sidebar.button(title,key=str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_message = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                 role = 'assistant'

            temp_message.append({'role':role,'content':message.content})

        st.session_state['message_history'] = temp_message
        st.rerun()
        

# ================================main UI ======================================================================================
CONFIG = {'configurable':{'thread_id':st.session_state['thread_id']},'run_name':'chat_run'}


# disaply all history 
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('type here...') # get input

# handle input 
if user_input:

    # add to history
    st.session_state['message_history'].append({'role':'user','content':user_input})

    # Show immediately without waiting for rerun
    with st.chat_message('user', avatar='🕸️'):
        st.markdown(user_input)

    # adding title to the conv in side bar
    if st.session_state['thread_id'] not in st.session_state['chat_title']:
        title = generate_title(user_input)

        st.session_state['chat_title'][st.session_state['thread_id']] = title
    

    def stream_response():
        for message_chunk , metadata in chatbot.stream(
            {'messages':[HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode='messages'
        ):
            if isinstance(message_chunk,AIMessage):
                yield message_chunk.content

    ai_message = st.write_stream(stream_response())
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})