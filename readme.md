# Web Scraper

This project is a web scraper designed to extract product information from e-commerce websites. It uses various scraping strategies and tools to gather data and store it in a structured format.

## Features

- **Web Scraper**: Scrapes product data from multiple pages.
- **Retry Mechanism**: Retries failed requests up to a specified number of times.
- **Notification System**: Sends notifications upon completion or failure of scraping.
- **Data Storage**: Saves scraped data to a JSON file.
- **Currency Mapping**: Extracts and maps currency symbols to currency codes.
- **Product Repository**: Creates an index-based data structure to support caching under the hood instead of using caching solutions like Redis or Memcached.

## Project Structure

```
webscraper/
├── scrappers/
│   ├── web_scrapper.py
│   ├── product_scraper.py
│   ├── playwright_scrapper.py
│   ├── scrapper_strategy.py
│   ├── scrapping_tool.py
│   └── __init__.py
├── repositories/
│   ├── product_repository.py
│   ├── repository.py
│   └── __init__.py
├── models/
│   ├── product_model.py
│   └── __init__.py
├── decorators/
│   ├── retry_on_failure.py
│   └── __init__.py
├── utils/
│   ├── logger.py
│   ├── currency_mapping.py
│   └── __init__.py
├── data_directory/
│   └── products.json
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/webscraper.git
    cd webscraper
    ```
2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```
3. Install Playwright dependencies:

    ```sh
    playwright install
    ```

## Usage

1. Configure the scraper by setting the base URL and other parameters in `app.py`.
2. Run the scraper:

    ```sh
    python -m app.py
    ```
3. Alternatively, you can run the app using Uvicorn:

    ```sh
    uvicorn app:app --reload
    ```

## Future Improvements

- **Testing**: Add unit and integration tests to ensure the reliability and correctness of the scraper.
- **File Partitioning**: If the file size grows, adopt file partitioning to reduce memory footprint and improve performance.

## License

This project is licensed under the MIT License.
