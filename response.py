from available_functions import call_function


def render_response(response, user_prompt, verbose=False):
    if verbose:
        usage = extract_usage_metadata(response)
        print("User prompt: {}".format(user_prompt))
        print(
            "Prompt tokens: {}\nResponse tokens: {}".format(
                usage["prompt_token_count"], usage["candidates_token_count"]
            )
        )
    else:
        print("Response: \n{}".format(response.text))


def run_function_call(response, verbose):
    if not response.function_calls:
        return []
    results = []
    for func in response.function_calls:
        f = call_function(func, verbose)
        if len(f.parts) == 0:
            raise Exception(f"function {f.name} parts is empty")
        if not f.parts[0].function_response:
            raise Exception(f"function {f.name} resp is none")
        if not f.parts[0].function_response.response:
            raise Exception(f"function {f.name} resp.resp is none")
        results.append(f.parts[0])
        if verbose:
            print(f"-> {f.parts[0].function_response.response}")
    return results


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
