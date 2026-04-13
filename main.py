import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError()

gemini_client = genai.Client(api_key=api_key)

response = gemini_client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
)

if not hasattr(response, "prompt_token_count") or not hasattr(
    response, "candidates_token_count"
):
    raise RuntimeError("response is not valid")

print(
    "User prompt: Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
)
print(
    "Prompt tokens: {}\nResponse tokens: {}".format(
        response.prompt_token_count, response.candidates_token_count
    )
)
print("Response: \n {}".format(response.text))
