# File: PLAN.md

## Summary

The `ai_docs` project will be enhanced to generate file summaries and logic flow descriptions. New `AnalyzeLogicFlow` node will analyze code logic.  The `main()` function will orchestrate the execution of both nodes. Markdown files containing the summary and logic flow are output to a `docs` directory. Existing dependencies remain unchanged.


## Logic Flow

Okay, this document outlines a plan to enhance the `ai_docs` project to generate both a summary *and* an analysis of the logic flow of Python code, using separate PocketFlow nodes, and outputting the results in Markdown format. Let's break down the algorithm and logic flow described in the plan.

**Overall Purpose:**

The purpose is to automatically generate documentation for Python code, including both a concise summary and a more detailed description of the code's algorithm/logic.  This automation aims to reduce manual effort in documenting code, improve code understanding, and potentially aid in identifying potential issues or inefficiencies in the logic.

**Algorithm/Logic Flow:**

The process can be divided into three main stages: setup/instantiation, processing files, and generating Markdown output.

**1. Setup/Instantiation:**

*   **Parse Arguments (Implicit):**  The plan assumes that the list of files to process is obtained via `shared_settings["files"]` and the output directory via  `shared_settings["directory"]`. This suggests that the project takes command-line arguments or has a configuration file to specify these settings. The Mermaid diagram starts with "Parse Args", representing this implicit step.
*   **Instantiate Nodes:**  Two instances of PocketFlow nodes are created:
    *   `summariser = Summarise()`: This node is responsible for generating a short summary of the code.  Its `exec` method will use a prompt that asks for a 50-word summary.
    *   `logic_analyzer = AnalyzeLogicFlow()`: This *new* node is responsible for analyzing the code's logic flow. Its `exec` method will use a prompt that instructs the LLM to describe the algorithm, control structures, function calls, and data transformations.
*   **Initialize Result Storage:** An empty dictionary, `results = {}`, is created.  This dictionary will store the summary and logic flow analysis for each processed file.  The keys will be the file paths, and the values will be dictionaries containing the "summary" and "logic_flow" strings.

**2. Processing Files (Main Loop):**

*   **Iterate Through Files:** The code iterates through each file path specified in `shared_settings["files"]`.
*   **Read File Content:** For each `file_path`, the code reads the content of the file into a string variable (named `content` in the plan).  Error handling is mentioned (handling empty files, potential file I/O errors).
*   **Call Nodes' `exec` Methods:**
    *   `summary = summariser.exec(content)`: The `exec` method of the `Summarise` node is called with the file content. This is where the LLM is invoked (implicitly through `call_llm`), using the "Summarize this text in 50 words" prompt to generate the summary.
    *   `logic_flow = logic_analyzer.exec(content)`: The `exec` method of the `AnalyzeLogicFlow` node is called with the file content.  This invokes the LLM using the prompt that asks for a detailed logic flow analysis.  This prompt includes the actual code within triple backticks for proper formatting.
*   **Store Results:**  The generated summary and logic flow analysis are stored in the `results` dictionary: `results[file_path] = {"summary": summary, "logic_flow": logic_flow}`.
*   **Log Progress:** A log message (e.g., using `print`) indicates that the file has been processed.

**3. Generate Markdown Output (Output Loop):**

*   **Determine Output Directory:** The target directory for the generated Markdown files is determined by combining the base directory from `shared_settings["directory"]` with the subdirectory "docs" (`output_base_dir = Path(shared_settings["directory"]) / "docs"`).  The `pathlib` module is used for robust path manipulation.
*   **Create Output Directory:** The "docs" directory (and any necessary parent directories) is created using `output_base_dir.mkdir(parents=True, exist_ok=True)`. `parents=True` creates parent directories if they don't exist, and `exist_ok=True` prevents an error if the directory already exists.
*   **Iterate Through Results:** The code iterates through the `results` dictionary.
*   **Construct Markdown Path:** For each file, the target path for the Markdown file is constructed.  This path preserves the original file's relative structure within the "docs" directory:  `md_path = output_base_dir / Path(file_path).with_suffix(".md")`.  This ensures that if the original file was located in a deeply nested directory structure, the corresponding Markdown file will be created in a matching structure within the "docs" directory. The `.with_suffix(".md")`  ensures the output file ends with the `.md` extension.
*   **Ensure Subdirectories:** The parent directory of the Markdown file is created (if it doesn't already exist) to ensure that the file can be written successfully:  `md_path.parent.mkdir(parents=True, exist_ok=True)`.
*   **Format Content:**  The summary and logic flow analysis are formatted into a Markdown string, including a header for the original file path, "Summary" and "Logic Flow" sections.
*   **Write File:** The formatted Markdown content is written to the corresponding `.md` file, using `with open(...) as f:` to ensure the file is properly closed after writing. The `UTF-8` encoding is specified, which is crucial for handling potentially Unicode characters in the code or the generated content.
*   **Log Output Creation:** A log message indicates that the Markdown file has been generated.

**Control Structures:**

*   **Outer Loop:** Iterates through the list of files to process.
*   **Inner Loop:** Iterates through the results dictionary to generate Markdown files.
*   **Conditional Statements:**  The plan mentions error handling during file reading (implicitly using `try...except` or similar) and skipping empty files.  The `mkdir` call uses `exist_ok=True`, effectively acting as a conditional to prevent errors if the directory already exists.

**Data Transformations:**

*   **File Content -> String:** The file content is read into a string variable.
*   **String -> Summary (LLM):** The LLM (through `Summarise.exec`) transforms the code string into a summary string.
*   **String -> Logic Flow Analysis (LLM):** The LLM (through `AnalyzeLogicFlow.exec`) transforms the code string into a detailed logic flow analysis string.
*   **Strings -> Markdown String:** The summary and logic flow strings are formatted into a Markdown string.

**Function Calls:**

*   `Summarise.exec(content)`
*   `AnalyzeLogicFlow.exec(content)`
*   `call_llm` (implicitly called by `exec` methods)
*   `Path.mkdir(parents=True, exist_ok=True)`
*   `Path.with_suffix(".md")`
*   `open()` with `with` statement for file writing.

**Key Improvements/Considerations:**

*   **Separate PocketFlow Nodes:**  The use of separate `Summarise` and `AnalyzeLogicFlow` nodes allows for customized prompts and potentially different LLM configurations for each task.
*   **Structured Output:**  The generation of Markdown files with well-defined sections makes the documentation more readable and maintainable.
*   **Path Handling:** The use of `pathlib` for path manipulation makes the code more robust and platform-independent.
*   **Error Handling:** The plan mentions error handling for file reading and directory creation.  This is crucial for preventing the program from crashing due to unexpected errors.
*   **UTF-8 Encoding:**  Specifying `UTF-8` encoding when writing the Markdown files is essential for handling potentially Unicode characters in the code or the generated text.
*   **LLM Prompt Engineering:** The effectiveness of the documentation heavily relies on the quality of the prompts used in the `Summarise` and `AnalyzeLogicFlow` nodes. The `AnalyzeLogicFlow` prompt, in particular, needs to be carefully designed to elicit a comprehensive and accurate logic flow analysis.

In summary, the plan describes a well-structured process for automating the generation of code documentation using LLMs, with clear separation of concerns, robust path handling, and structured output.  The success of the plan depends heavily on the prompt engineering for the `AnalyzeLogicFlow` node and the quality of the LLM used by `call_llm`.

