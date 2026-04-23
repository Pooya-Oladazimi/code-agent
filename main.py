import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from response import render_response, run_function_call
from prompts import system_prompt
from available_functions import available_functions
import sys


load_dotenv()
parser = argparse.ArgumentParser(description="Chat bot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
user_prompt = args.user_prompt
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError()

gemini_client = genai.Client(api_key=api_key)
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

for _ in range(20):
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, temperature=0, tools=[available_functions]
        ),
    )
    if not response.function_calls:
        render_response(response, args.verbose)
        sys.exit(0)
    if response.candidates:
        # add the previous conversation to the history
        for can in response.candidates:
            if can.content:
                messages.append(can.content)
    function_results = run_function_call(response, args.verbose)
    messages.append(types.Content(role="user", parts=function_results))

print("Agent failed to answer this query.")
sys.exit(1)
