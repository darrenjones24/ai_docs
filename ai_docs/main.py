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
        prompt = f"Analyze the following Python code and describe its main algorithm or logic flow. Focus on the sequence of operations, control structures (loops, conditionals), function calls, and data transformations. Do not include the code in the output. Explain the purpose of the code in terms of its logic.\n\nCode:\n```python\n{text}\n```"
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
