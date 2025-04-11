import streamlit as st
from openai import AzureOpenAI

st.title("Corn Rootworm Chatbot Prototype")

client = AzureOpenAI(
    azure_endpoint = st.secrets["AZURE_ENDPOINT"],
    api_key = st.secrets["OPENAI_API_KEY"],
    api_version = "2025-02-01-preview"
    )


# Define a system prompt for the chatbot
# This is a control version of the chatbot, with no system prompt, to compare system prompts to base gpt-4o
system_prompt = """  """


# Initialize the openai model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What question do you have about the task?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages,
                {"role": "user", "content": prompt}
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
