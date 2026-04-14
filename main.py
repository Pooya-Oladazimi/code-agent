import argparse
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
parser = argparse.ArgumentParser(description="Chat bot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()
user_prompt = args.user_prompt
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError()

gemini_client = genai.Client(api_key=api_key)

response = gemini_client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_prompt,
)

if not hasattr(response, "usage_metadata"):
    raise RuntimeError("response is not valid")

usage_metadata = response.usage_metadata

if not hasattr(usage_metadata, "prompt_token_count") or not hasattr(
    usage_metadata, "candidates_token_count"
):
    raise RuntimeError("response is not valid")

print("User prompt: {}".format(user_prompt))
print(
    "Prompt tokens: {}\nResponse tokens: {}".format(
        usage_metadata.prompt_token_count, usage_metadata.candidates_token_count
    )
)
print("Response: \n {}".format(response.text))
