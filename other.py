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

game_name = "-".join(new_array).lower()

url_array = [f"https://www.ign.com/games/{game_name}",
             f"https://www.gameinformer.com/product/{game_name}",
             f"https://www.commonsensemedia.org/game-reviews/{game_name}"]

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

    for body in bodies:
        title = ""
        if i == 0:
            title = body.find(
                "h1", class_="display-title jsx-2978383395")
        elif i == 1:
            title = body.find(
                "span", class_="field field--name-title field--type-string field--label-hidden")
        elif i == 2:
            title = body.find(
                "h1", class_="heading--sourceserifpro")

        if title:
            title = title.text.strip()

            score = ""
            if i == 0:
                score = body.find("h2", class_="title1 jsx-2518848117")
            elif i == 1:
                score = body.find(
                    "div", class_="field field--name-field-review-score field--type-entity-reference field--label-hidden gi5-field-review-score gi5-entity-reference field__item")
            elif i == 2:
                the_score = body.find_all("div", class_="col-12 col-sm-6")
                score = []
                for review in the_score:
                    review_check = str(review)
                    if "Sex, Romance &amp; Nudity" in review_check:
                        review = review.find(
                            "div", class_="content-grid-item content-grid-item--shadow")['data-text']
                        score.append(review[3:-5])

            if score and i < 2:
                score = score.text.strip()
            elif score and i == 2:
                score = score

        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        while True:

            if title and score and isinstance(title, str) and isinstance(score, str) or i == 2 and title and score and isinstance(title, str):
                print()
                if i == 0:
                    print("IGN:")
                elif i == 1:
                    print("Game Informer:")
                elif i == 2:
                    print("Common Sense:")
                    print(f"{title}")
                    for s in score:
                        print(f"{s}\n")
                    title = ""
                    score = ""
                    break
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
                        "h1", class_="display-title jsx-2978383395")
                elif i == 1:
                    title = body.find(
                        "span", class_="field field--name-title field--type-string field--label-hidden")
                elif i == 2:
                    title = body.find(
                        "h1", class_="heading--sourceserifpro")

            if title:
                if not isinstance(title, str):
                    title = title.text.strip()

                if i == 0:
                    score = body.find("h2", class_="title1 jsx-2518848117")
                elif i == 1:
                    score = body.find(
                        "div", class_="field field--name-field-review-score field--type-entity-reference field--label-hidden gi5-field-review-score gi5-entity-reference field__item")
                elif i == 2:
                    the_score = body.find_all("div", class_="col-12 col-sm-6")
                    score = []
                    for review in the_score:
                        review_check = str(review)
                        if "Sex, Romance &amp; Nudity" in review_check:
                            # print("Doing deep copy...")
                            # review_2 = copy.deepcopy(review)
                            # print("Deep copy done.")
                            review = review.find(
                                "div", class_="content-grid-item content-grid-item--shadow")['data-text']
                            score.append(review[3:-5])

                if score and i < 2:
                    score = score.text.strip()
                    break
                elif score and i == 2:
                    score = score
                    break

            if new_height == last_height or title and score and isinstance(title, str) and isinstance(score, str) or i == 2 and title and score and isinstance(title, str):
                print()
                if i == 0:
                    print("IGN:")
                elif i == 1:
                    print("Game Informer:")
                elif i == 2:
                    print("Common Sense:")
                    print(f"{title}")
                    for s in score:
                        print(f"{s}\n")
                    title = ""
                    score = ""
                    break
                print(f"{title}\n  {score}/10\n")
                title = ""
                score = ""
                break

            last_height = new_height
