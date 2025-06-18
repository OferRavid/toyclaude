import os
import sys
from dotenv import load_dotenv
from google.genai import types, Client
from prompts import system_prompt
from call_function import available_functions

def main():
    if len(sys.argv) <= 1:
        print("Usage: python main.py <user_prompt> [--verbose]")
        exit(1)

    user_prompt = sys.argv[1]

    load_dotenv()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if not response.function_calls:
        print(response.text)
        return

    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")


if __name__ == "__main__":
    main()
