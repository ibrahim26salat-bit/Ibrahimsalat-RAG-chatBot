from langchain_community.vectorstores import FAISS


def create_vectorstore(chunks, embeddings):

    db = FAISS.from_documents(

        documents=chunks,

        embedding=embeddings

    )

    db.save_local("database")

    return db


def load_vectorstore(embeddings):

    db = FAISS.load_local(

        "database",

        embeddings,

        allow_dangerous_deserialization=True

    )

    return db
