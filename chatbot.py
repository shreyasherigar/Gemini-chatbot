# 
import time
import os
import joblib
import streamlit as st
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyAhKRHjuc5_L9i3TowkZxlemd_UUogSEhg") 
new_chat_id = f'{time.time()}'

# Create data directory if it doesn't exist
if not os.path.exists('data/'):
    os.mkdir('data/')

# Load past chats
try:
    past_chats = joblib.load('data/past_chats_list')
except:
    past_chats = {}

# Sidebar for selecting past chats
with st.sidebar:
    st.write('Past Chats')
    if 'chat_id' not in st.session_state:
        st.session_state.chat_id = st.selectbox(
            label='Past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    else:
        st.session_state.chat_id = st.selectbox(
            label='Past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
        )
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

# Load messages and history
try:
    st.session_state.messages = joblib.load(f'data/{st.session_state.chat_id}-st_messages')
    st.session_state.gemini_history = joblib.load(f'data/{st.session_state.chat_id}-gemini_messages')
except:
    st.session_state.messages = []
    st.session_state.gemini_history = []

# Initialize the model
st.session_state.model = genai.GenerativeModel('gemini-pro')
st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.gemini_history)

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(name=message['role']):  # Specify name argument
        st.markdown(message['content'])

# Chat input and message handling
if prompt := st.chat_input('Message here'):
    if st.session_state.chat_id not in past_chats:
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')

    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    response = st.session_state.chat.send_message(prompt, stream=True)

    with st.chat_message(name='assistant'):  # Specify name for assistant
        message_placeholder = st.empty()
        full_response = ''
        
        for chunk in response:
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
                message_placeholder.write(full_response)
        
        message_placeholder.write(full_response)

    st.session_state.messages.append({'role': 'assistant', 'content': full_response})
    st.session_state.gemini_history = st.session_state.chat.history

    # Save messages and history
    joblib.dump(st.session_state.messages, f'data/{st.session_state.chat_id}-st_messages')
    joblib.dump(st.session_state.gemini_history, f'data/{st.session_state.chat_id}-gemini_messages')


# import time
# import os
# import json
# import streamlit as st
# import google.generativeai as genai

# # Configure the API key
# genai.configure(api_key="AIzaSyAhKRHjuc5_L9i3TowkZxlemd_UUogSEhg")  # Replace with your actual API key 
# new_chat_id = f'{time.time()}'

# # Create data directory if it doesn't exist
# if not os.path.exists('data/'):
#     os.mkdir('data/')

# # Load past chats
# try:
#     with open('data/past_chats_list.json', 'r') as f:
#         past_chats = json.load(f)
# except (FileNotFoundError, json.JSONDecodeError):
#     past_chats = {}

# # Sidebar for selecting past chats
# with st.sidebar:
#     st.write('Past Chats')
#     if 'chat_id' not in st.session_state:
#         st.session_state.chat_id = st.selectbox(
#             label='Past chat',
#             options=[new_chat_id] + list(past_chats.keys()),
#             format_func=lambda x: past_chats.get(x, 'New Chat'),
#             placeholder='_',
#         )
#     else:
#         st.session_state.chat_id = st.selectbox(
#             label='Past chat',
#             options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
#             index=1,
#             format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
#             placeholder='_',
#         )
#     st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

# # Load messages and history
# try:
#     with open(f'data/{st.session_state.chat_id}-st_messages.json', 'r') as f:
#         st.session_state.messages = json.load(f)
#     with open(f'data/{st.session_state.chat_id}-gemini_messages.json', 'r') as f:
#         st.session_state.gemini_history = json.load(f)
# except (FileNotFoundError, json.JSONDecodeError):
#     st.session_state.messages = []
#     st.session_state.gemini_history = []

# # Initialize the model
# st.session_state.model = genai.GenerativeModel('gemini-pro')
# st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.gemini_history)

# # Display past messages
# for message in st.session_state.messages:
#     with st.chat_message(name=message['role']):
#         st.markdown(message['content'])

# # Chat input and message handling
# if prompt := st.chat_input('Message here'):
#     if st.session_state.chat_id not in past_chats:
#         past_chats[st.session_state.chat_id] = st.session_state.chat_title
#         with open('data/past_chats_list.json', 'w') as f:
#             json.dump(past_chats, f)

#     with st.chat_message('user'):
#         st.markdown(prompt)

#     st.session_state.messages.append({'role': 'user', 'content': prompt})

#     response = st.session_state.chat.send_message(prompt, stream=True)

#     with st.chat_message(name='assistant'):
#         message_placeholder = st.empty()
#         full_response = ''
        
#         for chunk in response:
#             for ch in chunk.text.split(' '):
#                 full_response += ch + ' '
#                 time.sleep(0.05)
#                 message_placeholder.write(full_response)
        
#         message_placeholder.write(full_response)

#     st.session_state.messages.append({'role': 'assistant', 'content': full_response})
#     st.session_state.gemini_history = st.session_state.chat.history

#     # Save messages and history
#     with open(f'data/{st.session_state.chat_id}-st_messages.json', 'w') as f:
#         json.dump(st.session_state.messages, f)

#     # Convert gemini_history to a serializable format (e.g., a list of text strings)
#     serializable_gemini_history = [{'text': str(item)} for item in st.session_state.gemini_history]
#     with open(f'data/{st.session_state.chat_id}-gemini_messages.json', 'w') as f:
#         json.dump(serializable_gemini_history, f)
