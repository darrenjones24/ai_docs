# Project Enhancement Plan: AI Docs Generation

**Goal:** Enhance the `ai_docs` project to generate both a summary and a description of the main algorithm/logic flow for each processed file, using distinct PocketFlow nodes, and output the combined results into structured Markdown files within a `docs` directory in the target project.

**Detailed Plan:**

1.  **Define Separate PocketFlow Nodes:**
    *   **File:** `ai_docs/main.py`
    *   **Node 1 (Summary):** Keep the existing `Summarise` node. Its `exec` method will retain the prompt: `f"Summarize this text in 50 words: \n\n {text}"`.
    *   **Node 2 (Logic Flow):** Create a *new* class `AnalyzeLogicFlow(Node)`. Its `exec` method will use the prompt: `f"Analyze the following Python code and describe its main algorithm or logic flow. Focus on the sequence of operations, control structures (loops, conditionals), function calls, and data transformations. Explain the purpose of the code in terms of its logic.\n\nCode:\n\`\`\`python\n{text}\n\`\`\`"`.
    *   **Node `prep`/`post`:** For simplicity in this plan, we'll assume the `prep` and `post` methods of these nodes are minimal or unused, and the main loop will handle data flow and result aggregation.

2.  **Orchestrate Node Execution in `main()`:**
    *   **File:** `ai_docs/main.py`
    *   **Instantiation:** Create instances of both nodes: `summariser = Summarise()`, `logic_analyzer = AnalyzeLogicFlow()`.
    *   **Result Storage:** Initialize an empty dictionary `results = {}`.
    *   **File Iteration:** Loop through each `file_path` in `shared_settings["files"]`.
    *   **Processing:**
        *   Read the content of `file_path`. Handle potential errors and skip empty files.
        *   Call the summarizer: `summary = summariser.exec(content)` (this implicitly uses `call_llm`).
        *   Call the logic analyzer: `logic_flow = logic_analyzer.exec(content)` (this also uses `call_llm`).
        *   Store both results: `results[file_path] = {"summary": summary, "logic_flow": logic_flow}`.
        *   Log progress (e.g., `print(f"Processed: {file_path}")`).

3.  **Generate Markdown Output:**
    *   **File:** `ai_docs/main.py` (after the processing loop)
    *   **Determine Output Directory:** Define the base path for documentation: `output_base_dir = Path(shared_settings["directory"]) / "docs"`. Use `pathlib.Path` for robust path handling.
    *   **Create Base Directory:** Ensure the `docs` directory exists: `output_base_dir.mkdir(parents=True, exist_ok=True)`.
    *   **Iterate and Write Files:** Loop through `results.items()`. For each `file_path`, `data` pair:
        *   **Construct Markdown Path:** Create the target path, preserving the original file's relative structure within the `docs` directory: `md_path = output_base_dir / Path(file_path).with_suffix(".md")`.
        *   **Ensure Subdirectories:** Make sure the parent directory for the Markdown file exists: `md_path.parent.mkdir(parents=True, exist_ok=True)`.
        *   **Format Content:** Create the Markdown string:
            ```markdown
            # File: {file_path}

            ## Summary

            {data['summary']}

            ## Logic Flow

            {data['logic_flow']}
            ```
        *   **Write File:** Write the formatted content to `md_path` (using `with open(...) as f:` and `f.write(...)`, specifying UTF-8 encoding).
        *   Log output creation (e.g., `print(f"Generated: {md_path}")`).

4.  **Dependencies/Settings:**
    *   No changes anticipated for `call_llm.py`, `fetch_files.py`, or `settings.py` based on this plan. The `pathlib` module is already used in `fetch_files.py`, so it's available.

**Workflow Diagram (Mermaid):**

```mermaid
graph TD
    A[Start: main.py] --> B{Parse Args};
    B --> C[crawl_files];
    C --> D{Get Filtered File List};
    D --> E{Loop Through Files};
    E -- File Path --> F[Read File Content];
    F -- Content --> G[Instantiate Summarise Node];
    F -- Content --> H[Instantiate AnalyzeLogicFlow Node];
    G -- Content --> I[Call Summarise.exec];
    H -- Content --> J[Call AnalyzeLogicFlow.exec];
    I -- Summary Prompt --> K{call_llm};
    J -- Logic Flow Prompt --> K;
    K -- Result --> L{Collect Summary};
    K -- Result --> M{Collect Logic Flow};
    L & M -- Store Results --> N{results Dict};
    N --> O{End File Loop};
    O --> P{Determine Output Dir (target/docs)};
    P --> Q{Create Output Dir};
    Q --> R{Loop Through Results};
    R -- Result Data --> S{Construct MD Path (target/docs/...)};
    S --> T{Create MD Subdirs};
    T --> U{Format MD Content};
    U --> V[Write MD File];
    V --> W{End Results Loop};
    W --> X[End];

    subgraph LLM Calls
        K;
    end

    subgraph File Processing Loop (main.py)
        E; F; G; H; I; J; L; M; N; O;
    end

     subgraph Markdown Output Loop (main.py)
        P; Q; R; S; T; U; V; W;
    end