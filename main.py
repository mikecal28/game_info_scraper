from curses import window
import requests
from bs4 import BeautifulSoup
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# from selenium.webdriver.support.ui import WebDriverWait


def scroll_down():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height


CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
WINDOW_SIZE = "1920,1080"

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
# chrome_options.binary_location = CHROME_PATH

pause = 10
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://www.ign.com/reviews/games"
driver.get(url)
elements = driver.find_elements(By.TAG_NAME, "button")

target = 0
target_element = ""
for e in elements:
    sub_element = e.find_elements(By.TAG_NAME, "div")
    for sub in sub_element:
        if sub.get_attribute("innerText") == "Search":
            target += 1
            break

    if target == 1:
        target_element = e
        break

target_element.click()
driver.implicitly_wait(10)

search_input = driver.find_element(By.TAG_NAME, "input")
# driver.implicitly_wait(10)
# time.sleep(5)

ActionChains(driver).move_to_element(search_input).send_keys("bioshock").perform()
# driver.implicitly_wait(10)
# time.sleep(5)

# search_modal = driver.find_elements(By.CLASS_NAME, "modal-window")
# for element in search_modal:
#     if element.class_name == "modal-window":
#         search_results = element.find_element(By.CLASS_NAME, "search-results")

new_target_element = ""
search_result = driver.find_elements(By.TAG_NAME, "div")
for result in search_result:
    if "BioShock" in result.get_attribute("innerText") and "vita" not in result.get_attribute("innerText"):
        parent = result.find_element(By.XPATH, "./..")
        # grandparent = parent.find_element(By.XPATH, "./..")
        # great_grandparent = grandparent.find_element(By.XPATH, "./..")
        print("yay")
        new_target_element = parent
        break




driver.implicitly_wait(10)
# time.sleep(5)
# new_target_element.click()
ActionChains(driver).move_to_element(new_target_element).click(new_target_element).perform()
print("click")
# driver.implicitly_wait(10)
# time.sleep(5)
# # search_result.click()

# # driver.implicitly_wait(10)
time.sleep(10)


# driver.find_element_by_tag_name("textarea").send_keys("This is the input text which is inputed.")

# scroll_down()


# # HEADERS = {
# #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537/6",
# #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
# #     "accept-encoding": "gzip, deflate, br",
# #     "accept-language": "en-US,en;q=0.9",
# #     "origin": url,
# #     "referer": url,
# # }
# # page = requests.get(url, headers=HEADERS)

# # soup = BeautifulSoup(page.content, "html.parser")

# soup = BeautifulSoup(driver.page_source, "html.parser")

# reviews = soup.find_all("a", class_="item-body")

# for review in reviews:
#     title = review.find("span", class_="interface jsx-1867969425 item-title bold")
#     if title:
#         title = title.text.strip()

#         score = review.find("figcaption", class_=None)
#         if score:
#             score = score.text.strip()

#         print(f"{title}\n  {score}/10\n")
