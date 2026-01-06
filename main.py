import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    if api_key is None:
        raise RuntimeError("Key not found")
    print("Hello from dumini!")
    client = genai.Client(api_key=api_key)
    print(client.models.generate_content(model = 'gemini-2.5-flash', contents = "This is a test of your response. Tell me the weather today in palo alto, california.").text)


if __name__ == "__main__":
    main()
