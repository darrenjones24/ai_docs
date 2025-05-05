# File: ai_docs/llm_cache.json

## Summary

This Python script generates project documentation using AI. It defines settings for file inclusion/exclusion and directory skipping. It uses command-line arguments, crawls files, and leverages the Gemini model via API calls to summarize files, storing the results in a cache for subsequent use.


## Logic Flow

The Python code aims to automatically generate documentation for a software project using AI, specifically Google's Gemini model. Here's a breakdown of its logic:

1.  **Configuration and Argument Parsing:**

    *   The `settings.py` file defines default settings like file suffixes to include/exclude (`DEFAULT_INCLUDE_SUFFIXES`, `DEFAULT_EXCLUDE_SUFFIXES`) and directories to exclude from scanning (`DEFAULT_EXCLUDE_DIRS`).  These are defined as sets for efficient lookups.
    *   The `parse_args()` function uses the `argparse` module to handle command-line arguments.  These arguments allow the user to specify the repository name (`-n`, `--name`), the top-level directory to scan (`-d`, `--directory`), and additional directories to exclude (`-e`, `--exclude_dirs`). The `os.getcwd()` function is used to default the directory to the current working directory if not specified via command line. The `nargs='*'` argument to `add_argument` lets users specify multiple arguments for `exclude_dirs`.
    *   It retrieves the Gemini model name and project ID from environment variables (`GEMINI_MODEL`, `GEMINI_PROJECT_ID`), providing default values if these environment variables are not set.

2.  **File Crawling (`fetch_files.py`):**

    *   The `crawl_files()` function recursively scans a directory and its subdirectories for files.
    *   It uses `pathlib.Path` for efficient path manipulation.
    *   It filters files based on:
        *   Inclusion: The file suffix must be in the `include_patterns` set.
        *   Exclusion: The file suffix must *not* be in the `exclude_suffixes` set.
        *   Directory Exclusion: No part of the file's relative path can be in the `exclude_dirs` set.  This prevents scanning of unwanted directories like `.git` or `venv`.  It uses `item.relative_to(directory).parts` to split the path into its components.
    *   Error Handling: Contains a `try...except` block to catch `ValueError` exceptions that can occur when calculating relative paths (e.g., if the directory is not a subdirectory of the current working directory).
    *   Logging:  Uses the `logging` module to log the number of files found and, at the debug level, the list of files.

3.  **LLM Interaction (`call_llm.py`):**

    *   The `call_llm()` function interacts with the Google Gemini API to generate text (in this case, summaries).
    *   It implements a caching mechanism using a JSON file (`llm_cache.json`) to store prompts and their corresponding responses.  This speeds up the process if the same prompt is encountered again.
    *   Logging: Logs both prompts and responses using the `logging` module.  The logs are stored in files named `llm_calls_YYYYMMDD.log` in the `logs` directory.
    *   Cache Handling:  The caching logic attempts to load the cache from disk, uses it if the prompt is found, and saves the updated cache back to disk. It includes error handling to prevent crashes if the cache file is corrupted or cannot be saved.
    *   API Call: Uses the `google.genai` library to make the API call to Gemini. It retrieves the project ID, location, and model name from environment variables.

4.  **Main Logic (`main.py`):**

    *   The `main()` function is the entry point of the program.
    *   It calls `parse_args()` to retrieve command-line arguments.
    *   It creates a `shared_settings` dictionary to store configuration data, including the arguments parsed, and the default include/exclude lists.
    *   It calls `fetch_files.crawl_files()` to get a list of files to process. The excluded directories are a union of the default excluded directories and the directories specified in the command line arguments.
    *   It iterates through the list of files. For each file:
        *   It reads the file's contents into the `file_contents["data"]` dictionary.
    *   It creates an instance of the `Summarise` class (likely a part of the `pocketflow` framework, though the exact details are not clear from the snippet). This class is responsible for creating a prompt and calling the llm
    *   It calls the `run` method of the `Summarise` node to summarise the extracted file content using an llm.
    *   Finally, it prints the summary (stored in `file_contents['summaries']`).

5. **Pocketflow Integration**

   *   The code appears to be using a simple dataflow framework called "pocketflow". The nodes have a `prep`, `exec` and `post` method
   *   The `Summarise` node is defined which will call the llm
   *   The `prep` method creates the prompt and accesses the shared content by calling `shared_settings["data"][\"settings.py\"]`
   *   The `exec` method calls the llm with the prompt
   *   The `post` method stores the summary in `shared_settings["summaries"]`

**Purpose:** The overall purpose of the code is to automate the generation of documentation for a project by scanning source files, filtering them based on specified criteria, and using an AI model to create summaries of their contents. The caching mechanism is used to speed up the process and reduce the number of API calls made to the language model.  The use of command-line arguments and environment variables provides flexibility in configuring the script's behavior.

