# app.py
import streamlit as st
from chatbot import ask  # Importing the ask function from chatbot.py

# Set up page
st.set_page_config(page_title="Lecture Notes Chatbot", layout="wide")
st.title("📘 Lecture Notes Chatbot (Llama3 + LangChain)")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input("Ask a question about CTSE or Software Engineering:", key="user_input")
    submit = st.form_submit_button("Ask")

# Process the user query
if submit and user_query:
    try:
        with st.spinner("🤖 Thinking..."):
            answer = ask(user_query)
        # Save Q&A to history
        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("Bot", answer))
    except Exception as e:
        st.session_state.chat_history.append(("Bot", f"⚠️ Error: {str(e)}"))

# Display chat history
# for role, msg in st.session_state.chat_history:
#     if role == "You":
#         st.markdown(f"**🧑 {role}:** {msg}")
#     else:
#         st.markdown(f"**🤖 {role}:** {msg}")

# Chat display area as a scrollable stack
st.markdown("""
    <style>
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 10px;
        background-color: #fafafa;
        border: 1px solid #ddd;
        border-radius: 10px;
    }
    .chat-message {
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 10px;
    }
    .chat-user {
        background-color: #DCF8C6;
        text-align: right;
    }
    .chat-bot {
        background-color: #F1F0F0;
    }
    </style>
    <div class="chat-container">
""", unsafe_allow_html=True)


# Display chat history heading only when chat exists
if st.session_state.chat_history:
    st.markdown("### Chat History")

# Chat display area (scrollable style effect)
chat_container = st.container()

# Display the latest interaction (most recent at top)
with chat_container:
    if len(st.session_state.chat_history) >= 2:
        # Get the last user and bot message pair (most recent interaction)
        last_interaction = st.session_state.chat_history[-2:]

        for role, msg in last_interaction:
            if role == "You":
                st.markdown(
                    f"""
                    <div style='background-color:#DCF8C6;padding:10px;border-radius:10px;margin:5px 0;text-align:right'>
                        <strong>🧑 You:</strong><br>{msg}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style='background-color:#F1F0F0;padding:10px;border-radius:10px;margin:5px 0'>
                        <strong>🤖 Bot:</strong><br>{msg}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # Now display the rest of the chat history below the latest one
    for role, msg in st.session_state.chat_history[:-2]:  # Skip the last two interactions already displayed
        if role == "You":
            st.markdown(
                f"""
                <div style='background-color:#DCF8C6;padding:10px;border-radius:10px;margin:5px 0;text-align:right'>
                    <strong>🧑 You:</strong><br>{msg}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='background-color:#F1F0F0;padding:10px;border-radius:10px;margin:5px 0'>
                    <strong>🤖 Bot:</strong><br>{msg}
                </div>
                """,
                unsafe_allow_html=True
            )



# Close container div
st.markdown("</div>", unsafe_allow_html=True)

