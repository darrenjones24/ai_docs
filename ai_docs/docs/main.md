# File: main.py

## Summary

This Python script analyzes code in a directory using LLMs. It crawls files, summarizes their content, and analyzes their logic flow using `Summarise` and `AnalyzeLogicFlow` nodes.  Results are stored in a dictionary and then outputted as Markdown files within a "docs" subdirectory, providing code summaries and logic flow descriptions.


## Logic Flow

The code's primary purpose is to analyze Python source code files within a specified directory and generate corresponding Markdown documentation that includes a summary and an analysis of the code's logic flow using a large language model (LLM).

The script begins by parsing command-line arguments using `parse_args` to configure settings like the target directory, file suffixes to include or exclude, and directories to exclude from analysis. It then uses these settings to crawl the specified directory using `fetch_files.crawl_files`, generating a list of Python files to process.  `crawl_files` returns file paths relative to the target directory.

For each file found, the script reads the file's content. It then calls an LLM (via the `call_llm` function) twice: once to generate a summary of the code's purpose and once to analyze and describe the code's algorithm and logic flow. The prompts include instructions to analyze the provided code string and return specific details based on those instructions. Error handling is included in the read, summarize, and analyze file processing steps.

After processing each file, the script stores the generated summary and logic flow analysis in a dictionary called `results`.

Finally, the script iterates through the `results` dictionary and generates a Markdown file for each processed Python file. The Markdown file contains the original filename, the LLM-generated summary, and the LLM-generated logic flow analysis, all properly formatted.  The Markdown files are written to a "docs" subdirectory within the original target directory. Error handling is also included here to avoid problems during file creation. The script also logs progress and errors and provides some output to the user via `print` statements.

Two Node classes, `Summarise` and `AnalyzeLogicFlow` are defined that encapsulate the LLM calls, though the `prep` and `post` methods are not actually being used. The `Summarise` node generates a summary, while the `AnalyzeLogicFlow` node focuses on describing the code's algorithm and logic flow.

In summary, the algorithm consists of parsing arguments, finding files, reading files, generating LLM-powered summaries and logic flow analyses, and then generating Markdown documentation files.

