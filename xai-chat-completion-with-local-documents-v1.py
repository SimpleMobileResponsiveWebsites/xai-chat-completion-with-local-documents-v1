import streamlit as st
import requests
import os

# Streamlit App
st.title("Chat Completion with x.ai and Local Documents")

# x.ai API Configuration
st.sidebar.header("API Configuration")
xai_api_key = st.sidebar.text_input("x.ai API Key", type="password")

# Upload Document
uploaded_file = st.file_uploader("Upload your document", type=["txt", "md", "pdf"])

def extract_text(file):
    """Extract text content from the uploaded file."""
    if file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        st.error("Only .txt files are supported for this demo.")
        return None

document_content = None
if uploaded_file:
    document_content = extract_text(uploaded_file)

# User Input
user_input = st.text_area("Enter your message", placeholder="Type a message for the assistant...")

# API Call Function
def call_xai_api(messages):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {xai_api_key}"
    }
    payload = {
        "messages": messages,
        "model": "grok-beta",
        "stream": False,
        "temperature": 0
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Chat Interaction
if st.button("Submit"):
    if not xai_api_key:
        st.error("Please provide your x.ai API key in the sidebar.")
    elif not user_input:
        st.error("Please enter a message for the assistant.")
    elif not document_content:
        st.error("Please upload a document.")
    else:
        # Build the message payload
        messages = [
            {"role": "system", "content": "You are a test assistant."},
            {"role": "user", "content": f"The document content is: {document_content}"},
            {"role": "user", "content": user_input}
        ]

        # Call the x.ai API
        response = call_xai_api(messages)

        if response:
            # Display the response
            assistant_message = response['choices'][0]['message']['content']
            st.markdown(f"**Assistant:** {assistant_message}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("[Documentation](https://x.ai)")
