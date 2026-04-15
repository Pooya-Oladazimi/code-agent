import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from response import render_response


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

response = gemini_client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
)

render_response(response, user_prompt, args.verbose)
