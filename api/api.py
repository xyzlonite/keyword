import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


def get_blogstadard_api(driver):
    result = {}

    try:
        html = driver.page_source
        # Parse the HTML content
        soup = BeautifulSoup(html, "html.parser")

        # Find the index of the opening curly brace
        start_index = soup.text.find("{")

        # Find the index of the closing curly brace
        end_index = soup.text.rfind("}")

        # Extract the JSON data
        json_data = soup.text[start_index : end_index + 1]

        # Convert the BeautifulSoup object to text
        data = json.loads(json_data)

        if len(data["naverBlogPostList"]) == 0:
            return {"error": "검색 결과 X"}

        else:
            naverBlogPostList = data["naverBlogPostList"]

            optimal = 0
            subOptimal = 0
            url = []

            optimal_list = []
            subOptimal_list = []

            for post in naverBlogPostList:
                if post["rowNum"] is None:
                    continue

                if int(post["rowNum"]) < 8:
                    if post["blogLevel"] == "최3" or post["blogLevel"] == "최2" or post["blogLevel"] == "-" or post["blogLevel"] == "":
                        optimal += 1
                        optimal_list.append(post["blogLevel"])
                    else:
                        subOptimal += 1
                        subOptimal_list.append(post["blogLevel"])

                    url.append(post["url"])

                else:
                    break

                result = {
                    "optimal": optimal,
                    "subOptimal": subOptimal,
                    "url": url,
                }

        return result

    except Exception as e:
        print(f"get_blogstadard_api : {e}")
        raise Exception("일일 사용량 초과")


def get_driver(data):
    driver = None
    try:
        user_id = data["user_id"]
        user_pw = data["user_pw"]
        keywords = data["keywords"]

        url = "https://blogstand.net/login/loginForm.do"
        # Instantiate Firefox options
        options = webdriver.FirefoxOptions()

        # Set headless mode
        options.headless = True

        # Instantiate a Firefox webdriver
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

        driver.get(url)

        # wait until someid is clickable
        wait = WebDriverWait(driver, 2)
        wait.until(EC.element_to_be_clickable((By.NAME, "id")))

        # Login section
        tag_id = driver.find_element(By.ID, "username")
        tag_pw = driver.find_element(By.ID, "password")

        tag_id.send_keys(user_id)
        tag_pw.send_keys(user_pw)

        # Click the login button
        login_btn = driver.find_element(By.ID, "loginBtn")
        login_btn.click()
        time.sleep(2)

        # Collecting results
        results = {}

        for keyword in keywords:
            static_url = f"https://blogstand.net/naver/searchKeyword.do?keyword={keyword}&searchType=all&sortOption=sim&dateOption=all&startDate=&endDate=&viewMoreCount="

            driver.get(static_url)

            wait = WebDriverWait(driver, 5)
            wait.until(EC.element_to_be_clickable((By.ID, "rawdata-tab")))
            raw_data_button = driver.find_element(By.ID, "rawdata-tab")

            # Click the button or menu to switch to 'View as raw data'
            raw_data_button.click()

            time.sleep(2)

            results[keyword] = get_blogstadard_api(driver)
            time.sleep(2)

        return results

    except Exception as e:
        print(f"에러: {e}")

    finally:
        if driver is not None:
            driver.quit()
        time.sleep(3)
