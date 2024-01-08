from curses import window
import requests
from bs4 import BeautifulSoup
import time
import re
import copy

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

game = input("Enter Game Name: ")
game_array = game.split(" ")
new_array = []
for name in game_array:
    name = re.sub(r'\W+', '', name)
    new_array.append(name)

game_name = "-".join(new_array).lower().replace("'", "").replace(":", "")

url_array = [f"https://www.ign.com/games/{game_name}",
             f"https://www.gameinformer.com/product/{game_name}"]

for i in range(len(url_array)):

    url = url_array[i]
    driver.get(url)

    # scroll_down()

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

    bodies = soup.find_all("body")

    score = ""

    for body in bodies:
        title = ""
        if i == 0:
            title = body.find(
                "h1", class_="display-title")
        elif i == 1:
            title = body.find(
                "span", class_="field field--name-title field--type-string field--label-hidden")

        if title:
            title = title.text.strip()

            score = ""
            if i == 0:
                score = body.find("figcaption")
            elif i == 1:
                score = body.find(
                    "div", class_="field field--name-field-review-score field--type-entity-reference field--label-hidden gi5-field-review-score gi5-entity-reference field__item")

            if score:
                score = score.text.strip()

        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        while True:

            if title and score and isinstance(title, str) and isinstance(score, str):
                print()
                if i == 0:
                    print("IGN:")
                elif i == 1:
                    print("Game Informer:")
                print(f"{title}\n  {score}/10\n")
                title = ""
                score = ""
                break

            # Scroll down to the bottom.
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script(
                "return document.body.scrollHeight")

            if not title:
                if i == 0:
                    title = body.find(
                        "h1", class_="display-title")
                elif i == 1:
                    title = body.find(
                        "span", class_="field field--name-title field--type-string field--label-hidden")

            if title:
                if not isinstance(title, str):
                    title = title.text.strip()

                if i == 0:
                    score = body.find("figcaption")
                elif i == 1:
                    score = body.find(
                        "div", class_="field field--name-field-review-score field--type-entity-reference field--label-hidden gi5-field-review-score gi5-entity-reference field__item")

                if score:
                    score = score.text.strip()
                    break

            if new_height == last_height or title and score and isinstance(title, str) and isinstance(score, str):
                print()
                if i == 0:
                    print("IGN:")
                elif i == 1:
                    print("Game Informer:")

                print(f"{title}\n  {score}/10\n")
                title = ""
                score = ""
                break

            last_height = new_height
