# Otodom Scraper

## Overview
This project is a web scraper for real estate listings from Otodom. It uses Selenium to navigate and extract data from the website.

## Requirements
- Python 3.12.6 or higher

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/marceli-ptak/web-scraping.git 
    ```
2. Navigate to the project directory:
    ```bash
    cd otodom-scraper
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Download the `chromedriver` executable from the following link (compatible with your Chrome version):
    - [ChromeDriver - WebDriver for Chrome](https://developer.chrome.com/docs/chromedriver/downloads/version-selection)

## Configuration
Before running the scraper, you need to set the path to `chromedriver` in the `config.ini` file.

1. Open the `config.ini` file in the project directory.
2. Ensure the following content is present in the `config.ini` file:
    ```ini
    [webdriver]
    chromedriver_path = C:\chromedriver-win64\chromedriver.exe
    ```
   Replace `C:\chromedriver-win64\chromedriver.exe` with the actual path to your `chromedriver` executable.

## Usage
To run the scraper, execute the following command:
```bash
python otodom-scraper.py
```

The scraped data will be saved in the project directory as a CSV file.  
Example file with scraped data is attached to the repository under the name otodom_listings.csv.


## Support
If you encounter any issues, feel free to contact me.