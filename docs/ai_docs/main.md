# File: ai_docs/main.py

## Summary

This Python script analyzes code in a directory using LLMs. It crawls files, summarizes their content, and analyzes their logic flow using `Summarise` and `AnalyzeLogicFlow` nodes. Results are stored in Markdown files within a "docs" subdirectory.  Command-line arguments control the target directory and exclusion patterns.


## Logic Flow

```python
import logging
from pathlib import Path
from pocketflow import Node
from call_llm import call_llm
from settings import (
    DEFAULT_EXCLUDE_SUFFIXES,
    DEFAULT_INCLUDE_SUFFIXES,
    DEFAULT_EXCLUDE_DIRS,
)
from settings import parse_args
import fetch_files


class Summarise(Node):
    """
    This class identifies abstractions in the code.
    """

    def prep(self,shared):
        return file_contents["data"]
    
    def exec(self, text):
        prompt = f"Summarize this text in 50 words: \n\n {text}"
        return call_llm(prompt)
    
    def post(self, shared, prep_res, exec_res):
        # Store the result in the shared settings
        file_contents["summaries"] = exec_res
        return "default"


# New Node for Logic Flow Analysis
class AnalyzeLogicFlow(Node):
    """
    This class analyzes the code to describe its main algorithm or logic flow.
    """

    # prep and post might not be needed if main loop handles orchestration
    # def prep(self, shared):
    #     pass

    def exec(self, text):
        prompt = f"Analyze the following Python code and describe its main algorithm or logic flow. Focus on the sequence of operations, control structures (loops, conditionals), function calls, and data transformations. Explain the purpose of the code in terms of its logic.\n\nCode:\n```python\n{text}\n```"
        # Assuming call_llm handles potential errors and returns a string
        return call_llm(prompt)

    # def post(self, shared, prep_res, exec_res):
    #     pass


def main() -> None:
    args = parse_args()

    # Create a dictionary of settings to be used in the script
    shared_settings = {
        "name": args.name,
        "directory": args.directory, # Target directory to analyze
        "exclude_patterns": DEFAULT_EXCLUDE_SUFFIXES,
        "exclude_dirs": DEFAULT_EXCLUDE_DIRS,
        "include_suffixes": DEFAULT_INCLUDE_SUFFIXES,
        "additional_exclude_dirs": args.exclude_dirs,
    }
    logging.debug(f"Shared settings: {shared_settings}")

    # Get a list of files from the target directory
    # Ensure paths are relative to the target directory for correct output structure
    target_dir = Path(shared_settings["directory"]).resolve()
    logging.info(f"Analyzing directory: {target_dir}")

    # fetch_files.crawl_files already returns relative paths if called correctly
    # Let's ensure the base directory passed to crawl_files is the target directory
    files_to_process = fetch_files.crawl_files(
        directory=str(target_dir), # Pass absolute path to crawl
        include_patterns=shared_settings["include_suffixes"],
        exclude_suffixes=shared_settings["exclude_patterns"],
        exclude_dirs=shared_settings["exclude_dirs"].union(
            shared_settings["additional_exclude_dirs"]
        ),
    )
    
    # Instantiate nodes
    summariser = Summarise()
    logic_analyzer = AnalyzeLogicFlow()

    results = {}
    logging.info(f"Processing {len(files_to_process)} files...")

    # Process each file
    for relative_file_path in files_to_process:
        absolute_file_path = target_dir / relative_file_path
        logging.debug(f"Processing file: {absolute_file_path}")
        print(f"Processing: {relative_file_path}") # User feedback
        try:
            with open(absolute_file_path, "r", encoding='utf-8') as f:
                content = f.read()
                if content.strip(): # Ensure content is not empty
                    # Call LLM for summary
                    summary = summariser.exec(content)
                    # Call LLM for logic flow
                    logic_flow = logic_analyzer.exec(content)
                    results[relative_file_path] = {"summary": summary, "logic_flow": logic_flow}
                else:
                    logging.warning(f"Skipped empty file: {absolute_file_path}")
                    print(f"Skipped empty file: {relative_file_path}")
        except Exception as e:
            logging.error(f"Error processing file {absolute_file_path}: {e}")
            print(f"Error processing file {relative_file_path}: {e}")

    # Generate Markdown output
    output_base_dir = target_dir / "docs"
    logging.info(f"Generating documentation in: {output_base_dir}")
    try:
        output_base_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create output directory {output_base_dir}: {e}")
        print(f"Error: Could not create output directory {output_base_dir}. Aborting.")
        return # Exit if we can't create the output dir

    for relative_file_path, data in results.items():
        md_filename = Path(relative_file_path).with_suffix(".md")
        md_path = output_base_dir / md_filename
        
        try:
            # Ensure subdirectory exists
            md_path.parent.mkdir(parents=True, exist_ok=True)

            # Format Markdown content
            md_content = f"""# File: {relative_file_path}

## Summary

{data['summary']}

## Logic Flow

{data['logic_flow']}
"""
            # Write the Markdown file
            with open(md_path, "w", encoding='utf-8') as f:
                f.write(md_content)
            logging.info(f"Generated: {md_path}")
            print(f"Generated: {md_path.relative_to(target_dir)}") # Show relative path to user

        except Exception as e:
            logging.error(f"Failed to write Markdown file {md_path}: {e}")
            print(f"Error writing file {md_path.relative_to(target_dir)}: {e}")

    print(f"\nDocumentation generation complete. Files written to: {output_base_dir}")


if __name__ == "__main__":
    main()
```

### Code Description

The Python code defines a program that analyzes source code files within a specified directory and generates Markdown documentation containing summaries and logic flow descriptions of each file using a Large Language Model (LLM). It leverages the `pocketflow` library for defining processing nodes, the `pathlib` library for file system operations, and a custom `call_llm` function to interact with the LLM.

### Execution Analysis

1.  **Initialization:**
    *   The `main` function begins by parsing command-line arguments using `parse_args()` and stores them in the `args` variable.
    *   It creates a `shared_settings` dictionary to hold configuration parameters, including the target directory, file inclusion/exclusion patterns, and other settings.
    *   Logging is initialized for debugging and error tracking.
    *   The target directory is resolved to an absolute path using `Path(shared_settings["directory"]).resolve()`.

2.  **File Discovery:**
    *   The `fetch_files.crawl_files()` function is called to retrieve a list of files to be processed within the target directory.  It accepts the directory path, inclusion/exclusion patterns, and exclusion directories as arguments. The result, `files_to_process`, is a list of *relative* file paths.

3.  **Node Instantiation:**
    *   Instances of the `Summarise` and `AnalyzeLogicFlow` classes (derived from `pocketflow.Node`) are created.  These nodes encapsulate the logic for summarizing and analyzing the logic flow of the code.

4.  **File Processing Loop:**
    *   The code iterates through the `files_to_process` list. Inside the loop:
        *   The absolute path of the current file is constructed by joining the target directory with the relative file path.
        *   The file is opened in read mode (`'r'`) with UTF-8 encoding.
        *   The file content is read into the `content` variable.
        *   A check is performed to ensure that the file content is not empty (`content.strip()`). This prevents the program from making calls to the LLM with empty files.
        *   If the file is not empty:
            *   The `summariser.exec(content)` function is called to generate a summary of the file content.  This passes the file content as input to the LLM.
            *   The `logic_analyzer.exec(content)` function is called to analyze the logic flow of the file content. This also passes the file content to the LLM.
            *   The summary and logic flow are stored in the `results` dictionary, keyed by the relative file path.
        *   If the file is empty, a warning message is logged and printed to the console.
        *   A `try...except` block handles potential exceptions that may occur during file processing (e.g., file not found, permission errors).

5.  **Markdown Output Generation:**
    *   The code creates an output directory (named "docs" inside the target directory).
    *   It iterates through the `results` dictionary. For each file:
        *   A Markdown file name is generated by replacing the file's suffix with ".md".
        *   The code constructs the full path to the Markdown file within the output directory.
        *   The parent directories of the Markdown file are created if they don't exist.
        *   The Markdown content is formatted to include the file name, summary, and logic flow analysis.
        *   The Markdown content is written to the file with UTF-8 encoding.
        *   Logging and console output indicate the successful generation of the Markdown file.
        *   A `try...except` block handles potential exceptions during file writing.

6.  **Completion:**
    *   A completion message is printed to the console, indicating the location of the generated documentation.

### Algorithm and Logic Flow

The program implements a straightforward, sequential algorithm:

1.  **Configuration:** Load settings and parse command-line arguments.
2.  **File Discovery:** Crawl the target directory to find files matching the specified criteria.
3.  **Iterative Processing:** For each file found:
    *   Read the file content.
    *   If the file is not empty:
        *   Call the LLM to summarize the file content.
        *   Call the LLM to analyze the logic flow of the file content.
        *   Store the summary and logic flow in a results dictionary.
4.  **Output Generation:** For each processed file:
    *   Create a corresponding Markdown file in the output directory.
    *   Write the file name, summary, and logic flow to the Markdown file.

The program uses a `for` loop to iterate through the files. It employs `try...except` blocks for error handling during file reading and writing. Conditional statements (`if content.strip()`) are used to avoid processing empty files. The core logic relies on the external `call_llm` function, which is assumed to handle the actual interaction with the LLM.

### Data Transformations

*   **Input:** The program takes a target directory and file inclusion/exclusion patterns as input.
*   **File Content:** The content of each file is read as a string.
*   **LLM Interaction:** The file content is transformed into a prompt for the LLM, and the LLM returns a string containing the summary and logic flow analysis.
*   **Output:** The summary and logic flow are formatted into Markdown content and written to output files.

### Purpose

The program's purpose is to automatically generate documentation for source code files using an LLM. It aims to provide concise summaries and high-level logic flow descriptions, which can be useful for understanding and maintaining large codebases. The generated Markdown files can be easily integrated into documentation systems.

