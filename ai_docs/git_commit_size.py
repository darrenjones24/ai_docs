#!/usr/bin/env python3
import argparse
import subprocess
import sys
from enum import Enum
from typing import Dict, List, Tuple


class CommitSize(Enum):
    EXTRA_SMALL = "XS"  # 0-10 lines
    SMALL = "S"         # 11-50 lines
    MEDIUM = "M"        # 51-200 lines
    LARGE = "L"         # 201-500 lines
    EXTRA_LARGE = "XL"  # 501-1000 lines
    MASSIVE = "XXL"     # 1000+ lines


def get_commit_diff_stats(repo_path: str, commit_a: str, commit_b: str = "HEAD") -> Dict:
    """
    Get statistics about the differences between two commits.
    
    Args:
        repo_path: Path to the Git repository
        commit_a: Base commit hash
        commit_b: Target commit hash (defaults to HEAD)
    
    Returns:
        Dict with statistics about files changed, insertions, and deletions
    """
    try:
        cmd = ["git", "-C", repo_path, "diff", "--numstat", f"{commit_a}..{commit_b}"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Parse the output to get statistics
        stats = {"files_changed": 0, "insertions": 0, "deletions": 0, "total_lines": 0}
        
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
                
            parts = line.split()
            if len(parts) >= 3:
                try:
                    insertions = int(parts[0]) if parts[0] != "-" else 0
                    deletions = int(parts[1]) if parts[1] != "-" else 0
                    
                    stats["files_changed"] += 1
                    stats["insertions"] += insertions
                    stats["deletions"] += deletions
                    stats["total_lines"] += insertions + deletions
                except ValueError:
                    # Skip lines that don't have numeric values
                    continue
        
        return stats
    except subprocess.CalledProcessError as e:
        print(f"Error analyzing commits: {e}", file=sys.stderr)
        print(f"Command output: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def classify_commit_size(total_lines: int) -> CommitSize:
    """
    Classify commit size based on total number of lines changed.
    
    Args:
        total_lines: Total lines changed (insertions + deletions)
    
    Returns:
        CommitSize enum value
    """
    if total_lines <= 10:
        return CommitSize.EXTRA_SMALL
    elif total_lines <= 50:
        return CommitSize.SMALL
    elif total_lines <= 200:
        return CommitSize.MEDIUM
    elif total_lines <= 500:
        return CommitSize.LARGE
    elif total_lines <= 1000:
        return CommitSize.EXTRA_LARGE
    else:
        return CommitSize.MASSIVE


def get_changed_files(repo_path: str, commit_a: str, commit_b: str = "HEAD") -> List[Tuple[str, int, int]]:
    """
    Get list of changed files with their insertions and deletions.
    
    Args:
        repo_path: Path to the Git repository
        commit_a: Base commit hash
        commit_b: Target commit hash (defaults to HEAD)
    
    Returns:
        List of tuples containing (filename, insertions, deletions)
    """
    try:
        cmd = ["git", "-C", repo_path, "diff", "--numstat", f"{commit_a}..{commit_b}"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        files = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
                
            parts = line.split(maxsplit=2)
            if len(parts) >= 3:
                try:
                    insertions = int(parts[0]) if parts[0] != "-" else 0
                    deletions = int(parts[1]) if parts[1] != "-" else 0
                    filename = parts[2]
                    
                    files.append((filename, insertions, deletions))
                except ValueError:
                    # Skip lines that don't have numeric values
                    continue
        
        return files
    except subprocess.CalledProcessError as e:
        print(f"Error analyzing files: {e}", file=sys.stderr)
        print(f"Command output: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Analyze Git commit sizes")
    parser.add_argument("commit", help="Base commit hash to compare with")
    parser.add_argument(
        "--target", default="HEAD", help="Target commit hash (defaults to HEAD)"
    )
    parser.add_argument(
        "--repo", default=".", help="Path to Git repository (defaults to current directory)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed information about changes"
    )
    
    args = parser.parse_args()
    
    # Get commit statistics
    stats = get_commit_diff_stats(args.repo, args.commit, args.target)
    size_category = classify_commit_size(stats["total_lines"])
    
    # Print summary
    print(f"Commit Size: {size_category.value}")
    print(f"Files Changed: {stats['files_changed']}")
    print(f"Lines Added: {stats['insertions']}")
    print(f"Lines Deleted: {stats['deletions']}")
    print(f"Total Lines Changed: {stats['total_lines']}")
    
    if args.verbose:
        print("\nChanged Files:")
        files = get_changed_files(args.repo, args.commit, args.target)
        for filename, insertions, deletions in sorted(files, key=lambda x: x[1] + x[2], reverse=True):
            print(f"  {filename}: +{insertions} -{deletions}")


if __name__ == "__main__":
    main()