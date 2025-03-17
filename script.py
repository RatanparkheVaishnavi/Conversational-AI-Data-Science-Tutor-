import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
os.environ["GOOGLE_API_KEY"] = "AIzaSyBwAxaTIxIHGZ9oiQRdvwbeRXQCDLjq724"
# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)
# Set up memory for conversation history
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Conversation chain
conversation = ConversationChain(llm=llm, memory=memory, input_key="input")

# Streamlit UI
st.set_page_config(page_title="Data Science Tutor", layout="wide")
st.title("🤖 Conversational AI Data Science Tutor")
st.write("Ask me any Data Science-related question!")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# File uploader
st.subheader("Upload Files (CSV, Images, or Text)")
uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt", "png", "jpg", "jpeg"])

if uploaded_file:
    file_details = {"filename": uploaded_file.name, "type": uploaded_file.type, "size": uploaded_file.size}
    st.write("File Uploaded Successfully!", file_details)
    
    if uploaded_file.type in ["image/png", "image/jpeg"]:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    elif uploaded_file.type == "text/csv":
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        st.write("CSV File Preview:")
        st.dataframe(df)
    elif uploaded_file.type == "text/plain":
        text_content = uploaded_file.read().decode("utf-8")
        st.write("Text File Content:")
        st.text(text_content)

# User input
user_query = st.text_input("Your Question:")
if st.button("Ask"):
    if user_query:
        response = conversation.run(user_query)
        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("Tutor", response))

# Display chat history
st.subheader("Chat History")
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)
