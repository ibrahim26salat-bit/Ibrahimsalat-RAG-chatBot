from utils.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from utils.embeddings import get_embeddings
from utils.vectorstore import create_vectorstore


def process_pdf(pdf_path):
    """
    Reads the uploaded PDF and creates a FAISS vector database.
    """

    documents = load_pdf(pdf_path)

    chunks = split_documents(documents)

    embeddings = get_embeddings()

    db = create_vectorstore(chunks, embeddings)

    return db

from utils.llm import ask_gemini


def answer_question(db, question):

    docs = db.similarity_search(
        question,
        k=6
    )

    if not docs:
        return (
            "I couldn't find the answer in the uploaded PDF.",
            []
        )

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    answer = ask_gemini(
        context,
        question
    )

    return answer, docs
