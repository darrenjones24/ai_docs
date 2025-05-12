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
    ".venv",
    ".env",
    "__pycache__",
    "build",
    "dist",
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