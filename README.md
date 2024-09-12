About the project 
====================

This is a webscraping project built in Python.
-----------------------------------------------

- The project is built to scrape the [fbref website](https://fbref.com/en/) to get basic team and player data
- The project makes use of the BeautifulSoup, pandas, and requests library in order to successfully scrape the website to provide data that powers applications that require it

Get started
----------------

## Table of Contents

- Installation
- Usage
- Project Structure

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Ace7codes/football-data-webscraping.git
    cd football-data-webscraping
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```
    FOR MAC
    python3 -m venv venv
    source venv/bin/activate 
    ```

    ```
    FOR WINDOWS
    python -m venv venv
    source venv/Scripts/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the scraper script:
    ```bash
    python scraper.py
    ```

2. The scraped data will be saved in a CSV file in the `data` directory.

## Project Structure
- `data/`: Directory where the scraped data is stored.
- `scraper.py`: Main script for scraping data.
- `requirements.txt`: List of dependencies required for the project.
- `README.md`: Project documentation.

