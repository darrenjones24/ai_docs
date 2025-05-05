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
    print("Crawling files...")
    directory = os.getcwd()  
    print(f"Files crawled from {directory}:")
    print (crawl_files(directory))

if __name__ == "__main__":
    main()