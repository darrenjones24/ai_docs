# File: ai_docs/settings.py

## Summary

This code defines default file suffixes to include/exclude for documentation generation, along with directories to ignore.  It uses `argparse` to handle command-line arguments for repository name, target directory, and excluded directories. It also pulls the Gemini model and project ID from environment variables.


## Logic Flow

```python
import typing
import argparse
import os


DEFAULT_INCLUDE_SUFFIXES = {
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".py",
    ".pyi",
    ".pyx",
    ".rst",
    ".tf",
    ".tfvars",
    ".ts",
    ".tsx",
    ".yaml",
    ".yml",
    "Dockerfile",
    "Jenkinsfil",
}

DEFAULT_EXCLUDE_SUFFIXES = {}

DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".github",
    ".terraform",
    "assets",
    "build",
    "dist",
    "env",
    "docs",
    "env",
    "images",
    "temp",
    "tests",
    "tmp",
    "venv",
}


def parse_args() -> typing.Any:
    """
    Parse command line arguments.
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate documentation for a project using AI.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-n",
        "--name",
        help="local Repository name",
        default="repo_name",
        )

    parser.add_argument(
        "-d",
        "--directory",
        help="top level directory to scan, default is current working directory",
        default=os.getcwd(),
        )

    parser.add_argument(
        "-e",
        "--exclude_dirs",
        nargs='*',
        help="comma separated list of directories to exclude",
        default=","
        )

    return parser.parse_args()

model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-exp-03-25")
project=os.getenv("GEMINI_PROJECT_ID", "sre-ai-dev")
```

**Analysis of the Python Code:**

**1. Imports:**

*   `typing`:  Used for type hinting, making the code more readable and helping with static analysis.
*   `argparse`:  A standard library module used for parsing command-line arguments. This allows users to specify options when running the script.
*   `os`:  A standard library module that provides a way to interact with the operating system, such as getting the current working directory or accessing environment variables.

**2. Constants:**

*   `DEFAULT_INCLUDE_SUFFIXES`: A set containing file extensions that the script will likely process (e.g., `.js`, `.py`, `.md`). Sets are used for efficient membership checking.
*   `DEFAULT_EXCLUDE_SUFFIXES`: An empty set, presumably meant to hold file extensions to exclude from processing. Currently, it excludes no file extensions.
*   `DEFAULT_EXCLUDE_DIRS`:  A set of directory names that the script should skip during processing (e.g., `.git`, `venv`, `tests`).

**3. `parse_args()` Function:**

*   **Purpose:**  This function defines how the script accepts and interprets command-line arguments.  It creates an `ArgumentParser` object, defines the arguments, and then parses them.
*   **Logic:**
    *   `parser = argparse.ArgumentParser(...)`: Initializes an `ArgumentParser` object with a description of the script and sets the formatter to show default values in the help message.
    *   `parser.add_argument(...)`:  Adds three command-line arguments:
        *   `-n` or `--name`:  Allows the user to specify a "repo name". It has a default value of "repo\_name".
        *   `-d` or `--directory`:  Allows the user to specify the top-level directory to scan. It defaults to the current working directory obtained using `os.getcwd()`.
        *   `-e` or `--exclude_dirs`: Allows the user to provide a list of comma-separated directories to exclude.  It defaults to a string containing only a comma. The `nargs='*'` part means that this argument can accept zero or more values, which are collected into a list.
    *   `return parser.parse_args()`:  Parses the command-line arguments provided by the user when the script is run and returns an object containing the parsed values.

**4. Environment Variables:**

*   `model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-exp-03-25")`: Retrieves the value of the environment variable `GEMINI_MODEL`. If this environment variable is not set, it defaults to the string `"gemini-2.5-pro-exp-03-25"`. This suggests the script interfaces with a Gemini AI model.
*   `project=os.getenv("GEMINI_PROJECT_ID", "sre-ai-dev")`: Retrieves the value of the environment variable `GEMINI_PROJECT_ID`. If not set, it defaults to `"sre-ai-dev"`. This likely represents a project ID for the Gemini AI service.

**Overall Purpose of the Code (Inferred):**

This code snippet appears to be the initial setup and configuration part of a script designed to generate documentation for a project using AI, specifically Google's Gemini model.

*   It takes user input for the project name, directory to scan, and directories to exclude.
*   It defines default settings for which file types to include and directory names to exclude during processing.
*   It configures the script to connect to the Gemini AI service using environment variables for the model and project ID.

The code sets the stage for a larger process that likely involves:

1.  Scanning the specified directory (and its subdirectories).
2.  Filtering files based on `DEFAULT_INCLUDE_SUFFIXES` and `DEFAULT_EXCLUDE_SUFFIXES`.
3.  Skipping directories listed in `DEFAULT_EXCLUDE_DIRS` (and potentially those passed via the `--exclude_dirs` argument).
4.  Extracting content from the files.
5.  Using the Gemini AI model (defined by `GEMINI_MODEL` and `GEMINI_PROJECT_ID`) to generate documentation based on the extracted content.

