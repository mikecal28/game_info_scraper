from curses import window
import requests
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# from selenium.webdriver.support.ui import WebDriverWait


def scroll_down():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:

        # Scroll down to the bottom.
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height


pause = 10
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
url = "https://www.ign.com/reviews/games"
driver.get(url)

scroll_down()


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537/6",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "origin": url,
    "referer": url,
}
page = requests.get(url, headers=HEADERS)

# soup = BeautifulSoup(page.content, "html.parser")

soup = BeautifulSoup(driver.page_source, "html.parser")

reviews = soup.find_all("a", class_="item-body")

for review in reviews:
    title = review.find(
        "span", class_="interface jsx-1867969425 item-title bold")
    if title:
        title = title.text.strip()

        score = review.find("figcaption", class_=None)
        if score:
            score = score.text.strip()

        print(f"{title}\n  {score}/10\n")
