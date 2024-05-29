import streamlit as st
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = Ollama(model="phi3")
st.title("Chatbot - Ollama Phi-3")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello there, how can I help you, today?"}]

# Write Message History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"]).write(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

if usr_input := st.chat_input(""):
    with st.chat_message("user"):
        st.markdown(usr_input)
    st.session_state.messages.append({"role": "user", "content": usr_input})
    prompt = ChatPromptTemplate.from_messages([
        ('System', 'You are a helpful assistant. Please respond to the questions.'),
        MessagesPlaceholder(variable_name="history"),
        ('Human', '{input}'),
    ])
    chain = prompt | llm
    response = chain.invoke({
        "input": usr_input,
        "history": st.session_state.messages,
    })
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
