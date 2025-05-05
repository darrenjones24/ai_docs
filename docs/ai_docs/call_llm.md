# File: ai_docs/call_llm.py

## Summary

This code defines a function `call_llm` to interact with a Google LLM, logging prompts and responses to a daily log file. It optionally uses a JSON file (`llm_cache.json`) for caching prompts and their corresponding responses to avoid redundant API calls. A test call is performed to demonstrate functionality.


## Logic Flow

```python
from google import genai
import os
import logging
import json
from datetime import datetime


# Configure logging
log_directory = os.getenv("LOG_DIR", "logs")
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(
    log_directory, f"llm_calls_{datetime.now().strftime('%Y%m%d')}.log"
)

# Set up logger
logger = logging.getLogger("llm_logger")
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent propagation to root logger
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)

# Simple cache configuration
cache_file = "llm_cache.json"


def call_llm(prompt: str, use_cache: bool = True) -> str:
    # Log the prompt
    logger.info(f"PROMPT: {prompt}")

    # Check cache if enabled
    if use_cache:
        # Load cache from disk
        cache = {}
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    cache = json.load(f)
            except:
                logger.warning(f"Failed to load cache, starting with empty cache")

        # Return from cache if exists
        if prompt in cache:
            logger.info(f"RESPONSE: {cache[prompt]}")
            return cache[prompt]

    # Call the LLM if not in cache or cache disabled
    client = genai.Client(
        vertexai=True,
        project=os.getenv("GEMINI_PROJECT_ID", "ai-sre-dev-84b7"),
        location=os.getenv("GEMINI_LOCATION", "us-central1")
    )

    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    
    response = client.models.generate_content(model=model, contents=[prompt])
    response_text = response.text

    # Log the response
    logger.info(f"RESPONSE: {response_text}")

    # Update cache if enabled
    if use_cache:
        # Load cache again to avoid overwrites
        cache = {}
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    cache = json.load(f)
            except:
                pass

        # Add to cache and save
        cache[prompt] = response_text
        try:
            with open(cache_file, "w") as f:
                json.dump(cache, f)
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    return response_text


if __name__ == "__main__":
    test_prompt = "Hello, how are you?"

    # First call - should hit the API
    print("Making call...")
    response1 = call_llm(test_prompt, use_cache=False)
    print(f"Response: {response1}")
```

**Code Description**

The Python code defines a function `call_llm` that interacts with a Large Language Model (LLM) from Google's `genai` library. It also implements a simple caching mechanism to avoid unnecessary API calls. The script also includes basic logging.

**Algorithm and Logic Flow**

1.  **Initialization:**
    *   It starts by importing necessary libraries (`google.genai`, `os`, `logging`, `json`, `datetime`).
    *   It configures a logger to record prompts and responses to a log file. The log file's name includes the current date.  The logging level is set to `INFO`, and log messages are formatted with a timestamp, level, and the message itself.
    *   It defines the name of a cache file (`llm_cache.json`).

2.  **`call_llm(prompt: str, use_cache: bool = True) -> str` Function:**
    *   Takes a `prompt` string (the text to send to the LLM) and a `use_cache` boolean (defaulting to `True`) as input.
    *   Logs the input `prompt` using the logger.
    *   **Caching (if `use_cache` is True):**
        *   Loads the cache from the `llm_cache.json` file. If the file doesn't exist or loading fails, it starts with an empty cache.
        *   Checks if the `prompt` already exists as a key in the `cache`.
        *   If the `prompt` is found in the cache, it logs the cached `response` and returns it immediately, avoiding the LLM call.
    *   **LLM Interaction (if `use_cache` is False or prompt not in cache):**
        *   Creates a `genai.Client` object to connect to the LLM service. It retrieves the project ID and location from environment variables, with fallback defaults.
        *   It gets the model name from environment variables, with a fallback default.
        *   Calls the LLM using `client.models.generate_content`, passing the `prompt`.
        *   Extracts the response text from the LLM's response.
        *   Logs the `response_text` using the logger.
    *   **Cache Update (if `use_cache` is True):**
        *   Loads the cache from file again to avoid overwriting any changes made by other processes.
        *   Adds the `prompt` and `response_text` to the `cache` dictionary.
        *   Saves the updated `cache` to the `llm_cache.json` file.  It catches potential exceptions during saving and logs an error message if the save fails.
    *   Returns the `response_text`.

3.  **`if __name__ == "__main__":` Block (Main Execution):**
    *   Defines a sample `test_prompt`.
    *   Calls the `call_llm` function *without* caching enabled (`use_cache=False`). This ensures a fresh call to the LLM.
    *   Prints the `response` to the console.

**Purpose of the Code**

The code provides a reusable function (`call_llm`) for interacting with a Google LLM.  Its primary purpose is to:

1.  **Abstract LLM interaction:**  It encapsulates the complexity of making API calls to the LLM service.
2.  **Implement Caching:** It uses a simple file-based cache to store prompts and their corresponding responses, which can significantly reduce the number of API calls and improve response times for repeated prompts.
3.  **Provide Logging:** It logs prompts and responses, which is valuable for debugging, monitoring, and auditing purposes.
4.  **Configuration via Environment Variables:** It uses environment variables to configure the LLM project, location, and model, making it more flexible and adaptable to different environments.

In essence, it's a wrapper around the `genai` library that adds caching and logging capabilities to simplify and optimize LLM usage.

