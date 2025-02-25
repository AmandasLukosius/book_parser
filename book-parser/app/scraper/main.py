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
class Book:     # pylint: disable=missing-class-docstring
    name: str
    availability: str
    upc: str
    price_exc_tax: str
    tax: str


@dataclass
class Response:     # pylint: disable=missing-class-docstring
    body_html: HTMLParser
    next_page: dict


def get_page(client, url: str):
    """
    Returns parsed html content

    Args:
        client (obj): httpx client
        url (str): url to parse

    Returns:
        reponse: parsed page data
    """
    resp = client.get(url)
    data = HTMLParser(resp.text)
    if data.css_first("li.next"):
        next_page = data.css_first("li.next a").attributes
    else:
        next_page = {"href": None}
    return Response(body_html=data, next_page=next_page)


def parse_links(html: str):
    """
    Extract all links of books on the page

    Args:
        html (obj): html object

    Returns:
        list: list of urls of books in one page
    """
    links = html.css("article.product_pod h3 a")
    return [link.attrs["href"] for link in links]


def get_value(html, selector, index):
    """
    Selectings values from html

    Args:
        html (obj): html document
        selector (str): html selector
        index (int): index of selector

    Returns:
        boolean: parsed value
    """
    try:
        value = html.css(selector)[index].text(strip=True)
        return value
    except:     # pylint: disable=bare-except
        return "none"


def generate_book_entry(html):
    """
    Function to return parsed book values

    Args:
        html (obj): html document

    Returns:
        object: filtered out required book data
    """
    new_book = Book(
        name = get_value(html, "h1", 0),
        availability = get_value(html, "table tbody tr td", 5),
        upc = get_value(html, "table tbody tr td", 0),
        price_exc_tax = get_value(html, "table tbody tr td", 3),
        tax = get_value(html, "table tbody tr td", 4),
    )
    return new_book


def validate_url(value):
    """
    Function to return parsed value from html

    Args:
        value (str): html document

    Returns:
        str: filtered out required book data
    """
    if "catalogue" not in value:
        return "catalogue/" + value

    return value

async def get_data(client, url):
    """
    Async function to parse html and save data to json
    """
    resp = await client.get(url)
    html = HTMLParser(resp.text)
    save_data(new_book=generate_book_entry(html), filename=abspath(BOOK_JSON))


async def parse_data(links):
    """
    Async function to parse data from individual pages
    """
    async with httpx.AsyncClient() as client:
        tasks = []
        for link in links:
            tasks.append(get_data(client, link))
        return await asyncio.gather(*tasks)


def main():
    """
    Main logic to iterate through all links in every page.
    """
    url = "https://books.toscrape.com/"
    client = httpx.Client()

    while True:
        data = get_page(client, url)
        links = [BASE_URL + validate_url(link) for link in parse_links(data.body_html)]
        asyncio.run(parse_data(links))

        if data.next_page["href"] is None:
            client.close()
            break
        next_page_url = validate_url(data.next_page["href"])
        url = BASE_URL + str(next_page_url)


if __name__ == "__main__":
    main()
