def render_response(response, user_prompt, verbose=False):
    if verbose:
        usage = extract_usage_metadata(response)
        print("User prompt: {}".format(user_prompt))
        print(
            "Prompt tokens: {}\nResponse tokens: {}".format(
                usage["prompt_token_count"], usage["candidates_token_count"]
            )
        )
    print("Response: \n{}".format(response.text))


def extract_usage_metadata(response):
    if not hasattr(response, "usage_metadata"):
        raise RuntimeError("response is not valid")

    usage_metadata = response.usage_metadata

    if not hasattr(usage_metadata, "prompt_token_count") or not hasattr(
        usage_metadata, "candidates_token_count"
    ):
        raise RuntimeError("response is not valid")

    return {
        "prompt_token_count": usage_metadata.prompt_token_count,
        "candidates_token_count": usage_metadata.candidates_token_count,
    }
