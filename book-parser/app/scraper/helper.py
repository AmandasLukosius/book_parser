"""Helper functions"""
import json
from pathlib import Path
from rich import print as printf

def get_repo_dir() -> Path:
    """
    Returns base path of repository. We use this for path building.

    Returns:
        current_path (str): string representing the current working directory
    """
    return Path.cwd()

def is_duplicate(upc: str, data: dict) -> bool:
    """
    Checking if scraped book data already exists in books.json file

    Args:
        upc (str): Unique book ID
        data (dict): Current book data stored in JSON

    Returns:
        bool: True if duplicate, False otherwise
    """
    return any(book["upc"] == upc for book in data["books"])

def save_data(new_book: object, filename: str):
    """
    Updating books to our current json file excluding duplicates

    Args:
        new_book (obj): Book object
        filename (str): Path to JSON file

    """
    with open(filename,'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        if not is_duplicate(new_book.upc, file_data):
            printf(new_book)
            file_data["books"].append(new_book.__dict__)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
