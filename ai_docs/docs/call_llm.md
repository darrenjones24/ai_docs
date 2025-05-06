# File: call_llm.py

## Summary

This code defines a function `call_llm` that interacts with a Google LLM (Gemini) API.  It logs prompts and responses, utilizes a JSON file for caching responses to avoid redundant API calls, and includes error handling for loading/saving the cache. The main block calls the function.


## Logic Flow

The code defines a function `call_llm` that interacts with a Large Language Model (LLM) via the `google.genai` library and implements a simple caching mechanism to reduce API calls.

The script begins by setting up logging to a file named "llm_calls_{date}.log" in a "logs" directory. It configures a logger to write informational messages, including prompts and responses.

The core logic resides within the `call_llm` function. This function accepts a prompt string and a boolean flag, `use_cache`, as input.

First, it logs the input prompt using the configured logger. Then, if `use_cache` is true, it attempts to load a JSON file named "llm_cache.json" into a dictionary. If the file exists and can be loaded, it checks if the prompt already exists as a key in the dictionary. If the prompt is found in the cache, the cached response is logged and immediately returned, avoiding an LLM API call. If loading the cache fails, a warning is logged, and the process continues as if there was no cache.

If caching is disabled (`use_cache` is false) or the prompt is not found in the cache, the function proceeds to call the LLM API. It initializes a `genai.Client` using environment variables for project ID, location, and model name. It then uses the client to generate content based on the provided prompt. The LLM's response is then stored in the `response_text` variable. This response text is then logged using the logger.

After receiving the response from the LLM, if `use_cache` is true, the function attempts to update the cache. It loads the cache again (to avoid overwriting any changes made by other concurrent calls).  Then, it adds the current prompt and its corresponding response to the cache dictionary. Finally, it attempts to save the updated cache dictionary back to the "llm_cache.json" file. If saving the cache fails, an error message is logged.

Finally, the function returns the LLM's `response_text`.

The `if __name__ == "__main__":` block demonstrates a simple usage of the `call_llm` function.  It defines a test prompt and calls the `call_llm` function with the prompt and `use_cache` set to `False`, demonstrating a direct API call.  The returned response is printed to the console.

