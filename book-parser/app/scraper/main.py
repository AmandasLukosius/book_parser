"""
Main file for parsing books from https://books.toscrape.com/
"""
import asyncio
from dataclasses import dataclass
from os.path import join, abspath

import httpx
from selectolax.parser import HTMLParser
from helper import get_repo_dir, save_data

BASE_URL = "https://books.toscrape.com/"
BOOK_JSON = join(get_repo_dir(), 'book-parser', 'app', 'results', 'books.json')


@dataclass
class Book:
    """
    Data structure representing book information.
    """
    name: str
    availability: str
    upc: str
    price_exc_tax: str
    tax: str


@dataclass
class Response:
    """
    Data structure for holding parsed HTML content and next page information
    """
    body_html: HTMLParser
    next_page: dict


def get_page(client: httpx.Client, url: str) -> Response:
    """
    Fetch and parse HTML content from a given URL.

    Args:
        client (httpx.Client): HTTP client for making requests
        url (str): URL to fetch

    Returns:
        reponse: Parsed HTML content and next page data
    """
    resp = client.get(url)
    data = HTMLParser(resp.text)
    if data.css_first("li.next"):
        next_page = data.css_first("li.next a").attributes
    else:
        next_page = {"href": None}
    return Response(body_html=data, next_page=next_page)


def parse_links(html: HTMLParser) -> list[str]:
    """
    Extract all links of books on the page

    Args:
        html (HTMLParser): Parsed HTML document

    Returns:
        list: List of book URLs found on the page
    """
    return [link.attrs["href"] for link in html.css("article.product_pod h3 a")]


def get_value(html: HTMLParser, selector: str, index: int) -> str:
    """
    Extract a value from the HTML document based on a CSS selector

    Args:
        html (HTMLParser): Parsed HTML document
        selector (str): CSS selector to search for
        index (int): Index of the selected element

    Returns:
        str: Extracted text or "none" if not found
    """
    try:
        return html.css(selector)[index].text(strip=True)
    except IndexError:
        return "none"


def generate_book_entry(html: HTMLParser) -> Book:
    """
    Create a book instance from parsed HTML

    Args:
        html (HTMLParser): Parsed HTML document

    Returns:
        Book: Extracted book information
    """
    return Book(
        name = get_value(html, "h1", 0),
        availability = get_value(html, "table tbody tr td", 5),
        upc = get_value(html, "table tbody tr td", 0),
        price_exc_tax = get_value(html, "table tbody tr td", 3),
        tax = get_value(html, "table tbody tr td", 4),
    )


def validate_url(url: str) -> str:
    """
    Function to return parsed value from html

    Args:
        url (str): Relative or absolute book URL

    Returns:
        str: Adjusted absolute URL
    """
    return f"catalogue/{url}" if "catalogue" not in url else url


async def get_data(client: httpx.AsyncClient, url: str):
    """
    Fetch and parse book data asynchronously.

    Args:
        client (httpx.AsyncClient): HTTP client for making asynchronous requests.
        url (str): Book URL to fetch
    """
    resp = await client.get(url)
    html = HTMLParser(resp.text)
    save_data(new_book=generate_book_entry(html), filename=abspath(BOOK_JSON))


async def parse_data(links: list[str]):
    """
    Parse book data asynchronously from multiple URLs.

    Args:
        links (list[str]): List of book URLs to parse.

    Returns:
        list: List of completed async tasks.
    """
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(*(get_data(client, link) for link in links))


def main():
    """
    Main function to iterate through all book pages and parse data.
    """
    url = BASE_URL
    client = httpx.Client()

    while True:
        data = get_page(client, url)
        links = [BASE_URL + validate_url(link) for link in parse_links(data.body_html)]
        asyncio.run(parse_data(links))

        if not data.next_page["href"]:
            client.close()
            break

        url = BASE_URL + validate_url(data.next_page["href"])


if __name__ == "__main__":
    main()
