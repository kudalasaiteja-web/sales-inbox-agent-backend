import os
from google import genai
from dotenv import load_dotenv

load_dotenv()  # reads .env into environment variables

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Say hello in one short sentence."
)

print(response.text)