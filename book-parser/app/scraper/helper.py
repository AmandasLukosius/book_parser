"""
Helper functions
"""
import json
from pathlib import Path
from rich import print as printf

def get_repo_dir() -> str:
    """
    Returns base path of repository. We use this for path building.

    Returns:
        current_path (str): string representing the current working directory
    """
    return Path.cwd()

def is_duplicate(upc, data):
    """
    Checking if scraped book data already exists in books.json file

    Args:
        upc (str): unique book id
        data (dict): current book data stored in json

    Returns:
        boolean: is duplicate or not
    """
    duplicate = False
    for book in data['books']:
        if book['upc'] == upc:
            duplicate = True
            break

    return duplicate

def save_data(new_book, filename):
    """
    Updating books to our current json file excluding duplicates

    Args:
        new_book (obj): book object
        filename (str): path to result json file

    """
    with open(filename,'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        if not is_duplicate(new_book.upc, file_data):
            printf(new_book)
            file_data["books"].append(new_book.__dict__)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
