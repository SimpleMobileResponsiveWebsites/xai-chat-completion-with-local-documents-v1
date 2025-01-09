import streamlit as st
import requests
import openai

# Streamlit App
st.title("Chat Completion with OpenAI and Local Documents")

# OpenAI API Configuration
st.sidebar.header("API Configuration")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

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
def call_openai_api(messages):
    if not openai_api_key:
        st.error("API key is missing.")
        return None

    openai.api_key = openai_api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
        return response
    except openai.error.OpenAIError as e:
        st.error(f"Error: {e}")
        return None

# Chat Interaction
if st.button("Submit"):
    if not openai_api_key:
        st.error("Please provide your OpenAI API key in the sidebar.")
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

        # Call the OpenAI API
        response = call_openai_api(messages)

        if response:
            # Display the response
            assistant_message = response['choices'][0]['message']['content']
            st.markdown(f"**Assistant:** {assistant_message}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("[Documentation](https://platform.openai.com/docs)")
