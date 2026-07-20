from langchain_core.prompts import ChatPromptTemplate


def create_prompt():

    template = """
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
say:

"I couldn't find the answer in the uploaded PDF."

Context:

{context}

Question:

{question}
"""

    return ChatPromptTemplate.from_template(template)
