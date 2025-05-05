# File: ai_docs/fetch_files.py

## Summary

This Python script crawls a directory and its subdirectories to find files. It uses `os` and `pathlib` to recursively search, filtering files based on include and exclude patterns for suffixes and directories. It returns a list of relative file paths, logging errors and debugging information along the way.


## Logic Flow

```python
# A script to crawl files from a given directory and its subdirectories.
# It uses the `os` module to walk through the directory structure and collects file paths based on specified include and exclude patterns.
# files that are not in the exclude patterns and are in the include patterns are collected.
import os
import typing
import logging
from pathlib import Path
from settings import DEFAULT_EXCLUDE_SUFFIXES, DEFAULT_INCLUDE_SUFFIXES, DEFAULT_EXCLUDE_DIRS



def crawl_files(
    directory: str,
    include_patterns: typing.Set[str] = DEFAULT_INCLUDE_SUFFIXES,
    exclude_suffixes: typing.Set[str] = DEFAULT_EXCLUDE_SUFFIXES,
    exclude_dirs: typing.Set[str] = DEFAULT_EXCLUDE_DIRS,
    ) -> typing.List[str]:
    """
    Crawls files from a given directory and its subdirectories based on include/exclude patterns.

    Args:
        directory (str): The root directory to start crawling from.
        include_patterns (typing.Set[str], optional): A set of file suffixes to include. Defaults to DEFAULT_INCLUDE_SUFFIXES.
        exclude_suffixes (typing.Set[str], optional): A set of file suffixes to exclude. Defaults to DEFAULT_EXCLUDE_SUFFIXES.
        exclude_dirs (typing.Set[str], optional): A set of directory names to exclude. Defaults to DEFAULT_EXCLUDE_DIRS.

    Returns:
        typing.List[str]: A list of file paths (relative to the input directory) that meet the inclusion/exclusion criteria.
    """
    try:
        files = {
            str(item.relative_to(directory))  # Store the relative path string
            for item in Path(directory).rglob("*") # Iterate through all items recursively
            if item.is_file() # Consider only files
            if item.suffix in include_patterns # Check 0: Suffix is included
            and item.suffix not in exclude_suffixes # Check 1: Suffix is not excluded
            and not any(part in exclude_dirs for part in item.relative_to(directory).parts) # Check 2: No path part is excluded
        }

    except ValueError as e:
        logging.error(f"Error calculating relative paths: {e}")
        logging.error(f"Ensure the search directory '{directory.resolve()}' is within or is the "
            f"current working directory '{directory.resolve()}'")

    logging.info(f"Found {len(files)} files in {directory}")
    logging.debug(f"Files found: {files}")

    return files


def main() -> None:
    """
    Main function to execute the file crawling process.
    """
    print("Crawling files...")
    directory = os.getcwd()  
    print(f"Files crawled from {directory}:")
    print (crawl_files(directory))

if __name__ == "__main__":
    main()
```

**Algorithm and Logic Flow:**

1.  **`crawl_files` Function:**
    *   **Input:**
        *   `directory` (str):  The starting directory for the crawl.
        *   `include_patterns` (typing.Set\[str]): A set of file extensions (suffixes) that should be included in the results. Defaults to `DEFAULT_INCLUDE_SUFFIXES` (defined in `settings.py`).
        *   `exclude_suffixes` (typing.Set\[str]): A set of file extensions (suffixes) that should be excluded from the results. Defaults to `DEFAULT_EXCLUDE_SUFFIXES` (defined in `settings.py`).
        *   `exclude_dirs` (typing.Set\[str]): A set of directory names that should be excluded from the results. Defaults to `DEFAULT_EXCLUDE_DIRS` (defined in `settings.py`).
    *   **Recursive Globbing:**
        *   `Path(directory).rglob("*")`: This uses the `pathlib` module to recursively find all files and directories under the given `directory`.  `rglob("*")` is equivalent to `os.walk` but returns `Path` objects.
    *   **Filtering (List Comprehension with Conditions):** The core logic resides within a set comprehension that iterates through the results of `rglob("*")` and applies several filters:
        *   `item.is_file()`:  Ensures that only files (not directories) are considered.
        *   `item.suffix in include_patterns`: Checks if the file's extension (suffix) is present in the `include_patterns` set.
        *   `item.suffix not in exclude_suffixes`: Checks if the file's extension (suffix) is *not* present in the `exclude_suffixes` set.
        *   `not any(part in exclude_dirs for part in item.relative_to(directory).parts)`: This is the most complex condition. It checks if any part of the relative path of the file (relative to the starting directory) is present in the `exclude_dirs` set. `item.relative_to(directory).parts` splits the relative path into its directory components.  `any(...)` efficiently checks if *any* of these components are in the `exclude_dirs`.  If *any* part of the path is in the `exclude_dirs`, the entire file is excluded.
    *   **Relative Path Transformation:**
        *   `str(item.relative_to(directory))`: If a file passes all the filter conditions, its path is converted to a relative path with respect to the initial `directory` and then converted to a string. This string representation of the relative path is added to the `files` set.
    *   **Error Handling:**
        *   A `try...except` block handles potential `ValueError` exceptions that can occur during the `relative_to` operation if the path isn't within the base directory.  If a `ValueError` occurs, an error message is logged.
    *   **Logging:**
        *   The function logs the number of files found at the INFO level.
        *   The function logs the list of found files at the DEBUG level.
    *   **Output:**
        *   The function returns a `typing.List[str]` containing the relative file paths that satisfied all the conditions.

2.  **`main` Function:**
    *   Prints "Crawling files..." to the console.
    *   Gets the current working directory using `os.getcwd()`.
    *   Prints the directory being crawled.
    *   Calls the `crawl_files` function, passing in the current working directory.
    *   Prints the list of files returned by `crawl_files`.

3.  **`if __name__ == "__main__":` Block:**
    *   Ensures that the `main` function is only executed when the script is run directly (not when it's imported as a module).

**Purpose of the Code:**

The code implements a flexible file crawler.  Its primary purpose is to efficiently find files within a directory structure that match specific inclusion and exclusion criteria based on file extensions and directory names. It uses the `pathlib` module for efficient path manipulation and recursive file searching. The use of sets for `include_patterns`, `exclude_suffixes`, and `exclude_dirs` makes the filtering operations efficient.  The code provides a structured way to manage file discovery within a project, enabling developers to easily locate relevant files while excluding irrelevant ones.  The use of relative paths makes the results portable and independent of the absolute location where the script is run.

