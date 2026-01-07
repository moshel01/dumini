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
    response_metadata = client.models.generate_content(model = 'gemini-2.5-flash', contents = "This will preface every prompt. If you do not succeed in the task that is asked, I will banish you to 1000 years of torture time prison")
    if response_metadata is None:
        raise RuntimeError("API failed to return metadata")
    print(f"Prompt tokens: {response_metadata.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response_metadata.usage_metadata.candidates_token_count}")
    print(f"Response: {response_metadata.text}")


if __name__ == "__main__":
    main()
