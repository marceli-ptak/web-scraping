from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import datetime
import configparser
from unidecode import unidecode
import re

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')
# Retrieve the path to chromedriver from the configuration file
chromedriver_path = config['webdriver']['chromedriver_path']


def accept_cookies(driver):
    """
        Accepts cookies on a webpage using the provided WebDriver instance.

        This function waits for the cookies acceptance button to become clickable,
        then clicks on it. If the button is not found or has already been accepted,
        an appropriate message is printed.

        Parameters:
        driver (selenium.webdriver.Chrome): The WebDriver instance used to interact with the webpage.

        Returns:
        None
    """
    try:
        # Wait for the cookies acceptance button, then clik on it
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()
        print("Cookies accepted")
    except Exception as e:
        print("Cookies acceptance button not found or already accepted")


def normalize_text(text):
    """
        Normalizes the given text by removing any diacritical marks.

        This function uses the `unidecode` library to convert any accented characters
        to their closest ASCII equivalents.

        Parameters:
        text (str): The text to be normalized.

        Returns:
        str: The normalized text with diacritical marks removed, or the original text if it is None.
    """
    if text:
        return unidecode(text)
    return text


def get_listing_details(driver, url, city):
    """
    Retrieves detailed information about a real estate listing from the given URL.

    This function navigates to the specified URL using the provided WebDriver instance,
    waits for the page to load, and extracts various details about the listing such as
    address, area, number of rooms, floor, rent, building ownership, construction status,
    outdoor features, car parking, heating, price, market type, lift availability, build year,
    advertiser type, extra information, and building type.

    Parameters:
    driver (selenium.webdriver.Chrome): The WebDriver instance used to interact with the webpage.
    url (str): The URL of the real estate listing to be scraped.
    city (str): The city for which the listing details are being retrieved.

    Returns:
    dict: A dictionary containing the extracted details of the listing. If a detail is not found,
          its value will be set to None.
    """
    driver.get(url)
    time.sleep(1)  # Add delay to fully load page

    details = {}

    try:
        details['adres'] = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Adres"]').text
    except:
        details['adres'] = None

    try:
        details['area'] = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-area"]').text
    except:
        details['area'] = None

    try:
        details['number_of_rooms'] = driver.find_element(By.CSS_SELECTOR, 'a[data-cy="ad-information-link"]').text
    except:
        details['number_of_rooms'] = None

    try:
        details['floor'] = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-floor"]').text
    except:
        details['floor'] = None

    try:
        details['rent'] = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-rent"]').text
    except:
        details['rent'] = None

    try:
        details['building_ownership'] = driver.find_element(By.CSS_SELECTOR,
                                                            'div[data-testid="table-value-building_ownership"]').text
    except:
        details['building_ownership'] = None

    try:
        details['construction_status'] = driver.find_element(By.CSS_SELECTOR,
                                                             'div[data-testid="table-value-construction_status"]').text
    except:
        details['construction_status'] = None

    try:
        details['outdoor'] = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-outdoor"]').text
    except:
        details['outdoor'] = None

    try:
        details['car'] = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-car"]').text
    except:
        details['car'] = None

    try:
        details['heating'] = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-heating"]').text
    except:
        details['heating'] = None

    try:
        details['price'] = driver.find_element(By.CSS_SELECTOR, 'strong[data-cy="adPageHeaderPrice"]').text
    except:
        details['price'] = None

    try:
        details['market'] = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-market"]').text
    except:
        details['market'] = None

    try:
        details['lift'] = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-lift"]').text
    except:
        details['lift'] = None

    try:
        details['build_year'] = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-build_year"]').text
    except:
        details['build_year'] = None

    try:
        details['advertiser_type'] = driver.find_element(By.CSS_SELECTOR,
                                                         'div[data-testid="table-value-advertiser_type"]').text
    except:
        details['advertiser_type'] = None

    try:
        details['extra_info'] = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-extras_types"]').text
    except:
        details['extra_info'] = None

    try:
        details['building_type'] = driver.find_element(By.CSS_SELECTOR,
                                                       'div[data-testid="table-value-building_type"]').text
    except:
        details['building_type'] = None

    details['url'] = url

    return details


def scrape_otodom(city):
    """
        Scrapes real estate listings from Otodom for a given city.

        This function initializes a Chrome WebDriver, navigates to the Otodom website,
        and scrapes real estate listings for the specified city. It collects various
        details about each listing and returns them as a list of dictionaries.

        Parameters:
        city (str): The city for which the listings are being scraped.

        Returns:
        list: A list of dictionaries, each containing details of a real estate listing.
    """
    # Setting the path to chromedriver using the Service class
    service = Service(chromedriver_path)

    # Initialization of WebDriver using the Service class
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    base_url = f'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{city}?limit=72'

    listings = []
    seen_links = set()
    driver.get(base_url)

    # Get total number of results
    WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.css-15svspy.ezcytw17')))
    total_text = driver.find_element(By.CSS_SELECTOR, 'div.css-15svspy.ezcytw17').text
    total_num = int(re.findall(r'\d+', total_text)[-1])

    # Calculate the number of pages
    num_pages = (total_num + 71) // 72

    for page in range(1, num_pages + 1):
        url = f"{base_url}&page={page}"
        driver.get(url)
        time.sleep(1)  # Add delay to load page fully

        try:
            # Wait for the elements to be visible
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.css-17rb9mp a')))
            # Download advert links
            ad_elements = driver.find_elements(By.CSS_SELECTOR, 'div.css-17rb9mp a')
            links = [elem.get_attribute('href') for elem in ad_elements]
        except Exception as e:
            print(f"Elements not found on page {page} for city {city}: {e}")
            continue
        for link in links:
            if link not in seen_links:  # Check if link is not added
                print(f"Scraping {link}")
                details = get_listing_details(driver, link, city)
                listings.append(details)
                seen_links.add(link)  # Add link to avoid duplicates

    driver.quit()

    return listings


def main():
    """
        Main function to scrape real estate listings from Otodom for multiple cities and save the data to a CSV file.

        This function iterates over a predefined list of cities, scrapes real estate listings for each city using the
        `scrape_otodom` function, normalizes the text data, and saves the combined results to a CSV file.

        Parameters:
        None

        Returns:
        None
    """
    cities = ['warszawa', 'krakow', 'lodz', 'wroclaw', 'poznan', 'gdansk']
    all_listings = []

    for city in cities:
        print(f"Scraping data for {city}")
        listings = scrape_otodom(city)
        all_listings.extend(listings)

    df = pd.DataFrame(all_listings)
    df = df.applymap(normalize_text)
    df.to_csv(f'otodom_listings_{datetime.now().strftime("%Y-%m-%d")}.csv', index=False, encoding='utf-8', sep=';')
    print(f"Scraping completed. Data saved to otodom_listings_{datetime.now().strftime("%Y-%m-%d")}.csv")
    print(df)

if __name__ == "__main__":
    main()