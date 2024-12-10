import streamlit as st
import requests

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses google-bert/bert-base-multilingual-cased model to generate responses. "
    "To use this app, you need to provide an google-bert/bert-base-multilingual-cased API key, which you can get on huggingface website. "
)

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def is_nested_list(variable):
    # Проверить, является ли переменная списком
    if isinstance(variable, list):
        # Проверить, содержит ли список только другие списки
        return all(isinstance(item, list) for item in variable)
    return False

# Ask user for their google-bert/bert-base-multilingual-cased API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# bert_api_key = st.text_input("google-bert/bert-base-multilingual-cased API Key", type="password")
bert_api_key = st.text_input("google-bert/bert-base-multilingual-cased API Key", value="", type="password")
if not bert_api_key:
    st.info("Please add your API key to continue.", icon="🗝️")
else:
    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("The answer to the universe is [MASK]."):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        API_URL = "https://api-inference.huggingface.co/models/google-bert/bert-base-multilingual-cased"
        api_key_0 = "Bearer " + bert_api_key
        headers = {"Authorization": api_key_0}
        
        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            # Query the API
            response = query({"inputs": prompt})
            result = ""
            try:
                # Process the response
                if is_nested_list(response):
                    for item in response:
                        result += item[0]["sequence"]
                        result += ". \n"
                else:
                    result += response[0]["sequence"]
            except:
                print("Failed to process the response")
                result += "Something went wrong"
            # Add result to messages
            st.session_state.messages.append({"role": "assistant", "content": result})
            # Display the assistant's response
            st.markdown(result)