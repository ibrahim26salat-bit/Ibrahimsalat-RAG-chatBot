import streamlit as st
import os
from utils.rag import process_pdf, answer_question

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_css():
    with open("css/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# -----------------------------
# CHAT HISTORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.title("🤖 AI PDF Assistant")
    st.caption("Powered by Gemini + FAISS")

    st.markdown("### 📄 Document Assistant")

    st.info(
        """
**LLM**
Google Gemini

**Vector Store**
FAISS

**Embedding**
Sentence Transformers
"""
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        os.makedirs("data", exist_ok=True)

        pdf_path = os.path.join("data", uploaded_file.name)

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if "db" not in st.session_state:

            with st.spinner("Processing PDF..."):

                st.session_state.db = process_pdf(pdf_path)

            st.success("✅ PDF processed successfully!")

        st.markdown("### 📄 PDF Information")

        file_size = uploaded_file.size / (1024 * 1024)

        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**Size:** {file_size:.2f} MB")
        st.write("**Status:** Ready for Questions ✅")

    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):

        st.session_state.messages = []

        if "db" in st.session_state:
            del st.session_state["db"]

        st.rerun()

    st.divider()

    st.markdown("### ℹ️ About")

    st.info(
        """
**AI PDF Assistant**

Version: **1.0**

Built using:

• Google Gemini

• FAISS Vector Database

• Sentence Transformers

• LangChain

• Streamlit

This chatbot answers questions only from the uploaded PDF using Retrieval-Augmented Generation (RAG).
"""
    )

# -----------------------------
# MAIN PAGE
# -----------------------------
st.markdown(
    """
<div style="text-align:center;padding-top:20px;padding-bottom:20px;">
<h1>🤖 AI PDF Assistant</h1>
<h4 style="color:gray;">
Chat with your PDF using Google Gemini + RAG
</h4>
</div>
""",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("LLM", "Gemini")

with col2:
    st.metric("Vector DB", "FAISS")

with col3:
    st.metric("Embeddings", "Sentence Transformer")

st.divider()

st.subheader("💬 Chat")

# -----------------------------
# DISPLAY OLD MESSAGES
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# CHAT INPUT
# -----------------------------
question = st.chat_input("Ask anything about the PDF...")

# -----------------------------
# NEW MESSAGE
# -----------------------------
if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    if "db" not in st.session_state:

        answer = "⚠ Please upload a PDF first."
        docs = []

    else:

        with st.spinner("🤖 Gemini is analyzing the document..."):

            answer, docs = answer_question(
                st.session_state.db,
                question
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):

        st.markdown(answer)

        pages = []

        for doc in docs:

            page = doc.metadata.get("page")

            if page is not None:
                pages.append(page + 1)

        pages = sorted(set(pages))

        if pages:

            st.markdown("---")
            st.markdown("#### 📄 Source Pages")
            st.write(", ".join(f"Page {p}" for p in pages))

# -----------------------------
# DOWNLOAD CHAT
# -----------------------------
if st.session_state.messages:

    chat_text = ""

    for msg in st.session_state.messages:

        chat_text += f"{msg['role'].upper()}:\n"
        chat_text += msg["content"]
        chat_text += "\n\n"

    st.download_button(
        "⬇ Download Conversation",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "© 2026 AI PDF Assistant | Built with Streamlit • LangChain • FAISS • Google Gemini"
)
