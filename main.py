import streamlit as st
from together import Together


st.title("Chatbot")

client = Together(api_key=st.secrets["TOGETHER_API_KEY"])

# Set a default model
if "model" not in st.session_state:
    st.session_state["model"] = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def generate_chat_responses(chat_completion):
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# Accept user input
if prompt := st.chat_input("Input prompt"):
    # Add user message to chat history
    st.session_state.messages.append(
        {"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state.model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        chat_response_generator = generate_chat_responses(stream)
        response = st.write_stream(chat_response_generator)
    st.session_state.messages.append(({"role": "assistant",
                                       "content": response}))
