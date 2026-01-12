import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    if api_key is None:
        raise RuntimeError("Key not found")
    print("Hello from dumini!")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description = "Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    got_final_result = False
    for _ in range(20):
        results = []
        response = client.models.generate_content(model = 'gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0))
        if response is None:
            raise RuntimeError("API failed to return metadata")
        if response.function_calls is None:
            print(f"Response: {response.text}")
            got_final_result = True
            break
        if response.candidates is not None:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls != None:
            for function in response.function_calls:
                function_call_result = call_function(function, args.verbose)
                if function_call_result.parts is None:
                    raise Exception()
                elif function_call_result.parts[0].function_response is None:
                    raise Exception()
                elif function_call_result.parts[0].function_response.response is None:
                    raise Exception()
                else:
                    results.append(function_call_result.parts[0])
                    if args.verbose == True:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=results))
    if got_final_result == False:
        sys.exit("The model failed to produce a response with the given # of iterations")
    


if __name__ == "__main__":
    main()
