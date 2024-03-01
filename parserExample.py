import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                         "Chrome/122.0.0.0 Safari/537.36"}


def download(url):
    """
    Downloads the content from the specified URL and saves it as a file in the 'images' directory.

    Parameters:
    url (str): The URL from which to download the content.

    Returns:
    None
    """
    response = requests.get(url, stream=True)
    created_file = open("images\\" + url.split('/')[-1], "wb")
    for data in response.iter_content(1048576):
        created_file.write(data)
    created_file.close()


def get_url():
    """
    This function generates a URL by iterating through a range, sending a GET request to the URL, parsing the HTML response using BeautifulSoup, and finding all the div elements with the specified class. It then constructs a complete URL and yields it.
    """
    for count in range(1, 2):
        url = f"https://scrapingclub.com/exercise/list_basic/?page={count}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="w-full rounded border")
        for item in data:
            card_url = "https://scrapingclub.com" + item.find("a").get("href")
            yield card_url


def get_array():
    """
    This function iterates through URLs, sends requests, parses the response, and yields card data.
    """
    for card_url in get_url():
        response = requests.get(card_url, headers=headers)
        sleep(randint(1, 3))  # random pause between requests
        soup = BeautifulSoup(response.text, "lxml")
        card_data = soup.find("div", class_="my-8 w-full rounded border")

        name = card_data.find("h3", class_="card-title").text
        price = card_data.find("h4", class_="my-4 card-price").text
        description = card_data.find("p", class_="card-description").text
        url_img = "https://scrapingclub.com" + card_data.find("img", class_="card-img-top").get("src")
        download(url_img)
        yield name, price, description, url_img
