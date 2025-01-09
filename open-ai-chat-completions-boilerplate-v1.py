import openai
import os
import streamlit as st

# Setup OpenAI API key (Ensure your key is securely stored, for example, using environment variables)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prepare the messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, who won the world series in 2020?"}
]

# Try to send a request to OpenAI's GPT-4 model and get the assistant's reply
try:
    # API call to OpenAI for a chat completion (make sure you're using the correct method)
    response = openai.ChatCompletion.create(
        model="gpt-4",           # Model being used (e.g., gpt-4)
        messages=messages,       # The chat history
        temperature=0.7          # Temperature to control randomness
    )

    # Extract the assistant's reply from the response
    assistant_message = response['choices'][0]['message']['content']
    st.markdown(f"**Assistant:** {assistant_message}")

except openai.AuthenticationError:
    st.error("Authentication Error: Please check your OpenAI API key.")
except openai.InvalidRequestError as e:
    st.error(f"Invalid Request Error: {e}")
except openai.OpenAIError as e:
    st.error(f"OpenAI API Error: {e}")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
