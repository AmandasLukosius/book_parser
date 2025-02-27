# Book Scraper

A Python web scraper that extracts book data from [Books to Scrape](https://books.toscrape.com/) and saves it as JSON. Uses `httpx` for HTTP requests and `selectolax` for parsing HTML.

## Features
- Extracts book details: Name, Availability, UPC, Price (excluding tax), and Tax.
- Asynchronous data fetching for efficiency.
- Saves extracted data into a JSON file.
- Parses multiple pages automatically.

## Requirements and Installation

Ensure you have Python 3.13.2 and Poetry 2.1.1 installed. 

1. Clone the repository:
   ```sh
   git clone https://github.com/AmandasLukosius/book_parser.git
   cd book-scraper
   ```

2. Install dependencies:
   ```sh
   poetry install
   ```

### Dependencies used
- `httpx` - For making HTTP requests.
- `selectolax` - For parsing HTML content.
- `asyncio` - For handling asynchronous requests.
- `rich` - For better terminal output.

## Usage

Scheduling can be changed in cron file.

Run the scraper with:
```sh
poetry run python book-parser\scraper\main.py
```

The scraped book data will be saved in:
```
book-parser\results\books.json
```

## Project Structure
```
book-parser/
├── results/
│   ├── books.json       # JSON file storing scraped book data
│
├── scraper/
│   ├── helper.py        # Helper functions for handling JSON data
│   ├── main.py          # Main scraper script
│
├── cron                 # Cron jobs for automation
├── Dockerfile           # Docker setup for containerization
├── Poetry.lock          # Dependency lock file
├── pylintrc             # Pylint configuration file
├── pyproject.toml       # Project dependencies and configuration
└── README.md            # Project documentation
```

## How It Works
1. Fetches the book catalog from [Books to Scrape](https://books.toscrape.com/).
2. Parses book links and follows pagination.
3. Extracts book details from each page.
4. Saves data into a structured JSON file.

## TODO:
1. Make DockerFile more lightweight by using python alpine or slim package.
2. Deploy containerized application using Kubernetes.
3. Application could be reworked to use small gRPC microservice dedicated to raw scraped data parsing.
