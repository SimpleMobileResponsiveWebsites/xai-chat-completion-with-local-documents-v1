import openai
import streamlit as st
import os

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

# Chat Interaction
if st.button("Submit"):
    if not openai_api_key:
        st.error("Please provide your OpenAI API key in the sidebar.")
    elif not user_input:
        st.error("Please enter a message for the assistant.")
    elif not document_content:
        st.error("Please upload a document.")
    else:
        # OpenAI API Call
        try:
            openai.api_key = openai_api_key

            # Construct the prompt with document content
            messages = [
                {"role": "system", "content": "You are a test assistant."},
                {"role": "user", "content": f"The document content is: {document_content}"},
                {"role": "user", "content": user_input}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0
            )

            # Extract the assistant's message
            assistant_message = response['choices'][0]['message']['content']
            st.markdown(f"**Assistant:** {assistant_message}")

        except openai.error.AuthenticationError:
            st.error("Authentication Error: Please check your OpenAI API key.")
        except openai.error.InvalidRequestError as e:
            st.error(f"Invalid Request Error: {e}")
        except openai.error.OpenAIError as e:
            st.error(f"OpenAI API Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("[OpenAI Documentation](https://platform.openai.com/docs)")
