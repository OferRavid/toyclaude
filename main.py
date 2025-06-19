import os
import sys
from dotenv import load_dotenv
from google.genai import types, Client
from prompts import system_prompt
from call_function import available_functions, call_function, valid_function_calls

def main():
    if len(sys.argv) <= 1:
        print("Usage: python main.py <user_prompt> [--verbose]")
        exit(1)

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    user_prompt = " ".join(args)

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = Client(api_key=api_key)
    
    if verbose:
        print(f"User prompt: {user_prompt}")
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)
        
def generate_content(client: Client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part=function_call_part, verbose=verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response.response
        ):
            raise Exception(f"Error: something went wrong while calling function {valid_function_calls[function_call_part.name]}")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

if __name__ == "__main__":
    main()
