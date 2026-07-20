import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def ask_gemini(context, question):
    """
    Sends the retrieved context and user question to Gemini.
    """

    prompt = f"""
You are a helpful AI assistant.

Rules:
1. Answer ONLY using the provided context.
2. If the answer is not present in the context, reply exactly:
   "I couldn't find the answer in the uploaded PDF."
3. Keep answers concise and accurate.

-------------------------
Context:
{context}
-------------------------

Question:
{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:

        error = str(e)

        if "429" in error or "RESOURCE_EXHAUSTED" in error:

            return (
                "⚠️ Gemini API quota exceeded.\n\n"
                "Please wait for the quota to reset or use another API key."
            )

        elif "401" in error:

            return (
                "⚠️ Invalid Gemini API Key.\n\n"
                "Please check your .env file."
            )

        elif "404" in error:

            return (
                "⚠️ Gemini model not found.\n\n"
                "Please update the model name."
            )

        else:

            return (
                "⚠️ Unexpected error while contacting Gemini.\n\n"
                f"Details:\n{error}"
            )
