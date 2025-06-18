import os
import sys
from dotenv import load_dotenv
from google import genai

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

def main():
    if len(sys.argv) <= 1:
        print("Usage: python main.py <user_prompt> [--verbose]")
        exit(1)
    user_prompt = sys.argv[1]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=user_prompt,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if len(response.function_calls) > 0:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    # print("Response:")
    # print(response.text)


if __name__ == "__main__":
    main()
