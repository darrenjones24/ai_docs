# File: fetch_files.py

## Summary

This script crawls a directory and its subdirectories to find files. It uses `os` to traverse the directory structure and `pathlib` to construct paths. Files are collected based on include and exclude patterns for suffixes and directories, returning a list of relative file paths. A main method demonstrates use of crawl_files from the current directory.


## Logic Flow

The code defines a function `crawl_files` that recursively traverses a directory and its subdirectories to identify files that meet specific criteria. It uses the `os` module and `pathlib` for directory traversal and file system operations.

The `crawl_files` function first takes a directory path as input, along with optional sets of include and exclude file suffixes, and directories to exclude. It walks the directory tree using `Path(directory).rglob("*")`, retrieving every item within the directory and its subdirectories.

For each item, it checks if it is a file using `item.is_file()`. If it is a file, it further checks if its suffix is present in the `include_patterns` set and absent from the `exclude_suffixes` set. Additionally, it verifies that no part of the relative path is present in the `exclude_dirs` set. The relative path is calculated using `item.relative_to(directory)`. Only the files satisfying all these conditions are collected and stored as relative paths (strings) in a set.

The `main` function calls the `crawl_files` function using the current working directory. Finally, it prints the results of the file crawling operation to the standard output.

The primary data transformations involve converting Path objects to their relative string representations using `str(item.relative_to(directory))`, and building a set of these string representations.

