import json
import time

import undetected_chromedriver as uc
from bs4 import BeautifulSoup

# from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.utils import ChromeType


def get_blogstadard_api(driver):
    result = {}

    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        data = json.loads(soup.text)

        if len(data["naverBlogPostList"]) == 0:
            return {"error": "검색 결과 X"}

        else:
            naverBlogPostList = data["naverBlogPostList"]

            # print(f"soup.text: {soup.text}")
            # print(f"naverBlogPostList: {naverBlogPostList}")

            # Test Code
            # naverBlogPostList = fake_data["naverBlogPostList"]

            optimal = 0
            subOptimal = 0
            # period = []
            url = []

            optimal_list = []
            subOptimal_list = []
            # period_list = []
            # period_list2 = []

            for post in naverBlogPostList:
                # print(f' post["rowNum"]: { post["rowNum"]}')

                if post["rowNum"] is None:
                    continue

                if int(post["rowNum"]) < 8:
                    # print(f' post["blogLevel"]: { post["blogLevel"]}')

                    if post["blogLevel"] == "최3" or post["blogLevel"] == "최2" or post["blogLevel"] == "-" or post["blogLevel"] == "":
                        optimal += 1
                        optimal_list.append(post["blogLevel"])
                    else:
                        subOptimal += 1
                        subOptimal_list.append(post["blogLevel"])

                    # print(f' post["writeDate2"]: { post["writeDate2"]}')
                    # period_list.append(post["writeDate2"])

                    # if "시간" in post["writeDate2"]:
                    #     period.append(0)
                    #     # print(f"시간 period: {period}")
                    #     period_list2.append(0)

                    # else:
                    #     if post["writeDate2"] == "어제":
                    #         period.append(1)
                    #         period_list2.append(1)

                    #     elif post["writeDate2"] == "":
                    #         continue

                    #     else:
                    #         string = post["writeDate2"].replace("일 전", "").replace("일전", "")
                    #         integer_string = re.sub("[^0-9]", "", string)

                    #         period.append(int(integer_string))

                    #         period_list2.append(int(integer_string))

                    url.append(post["url"])

                else:
                    break

                # average_period = round(sum(period) / len(period))

                result = {
                    # "averagePeriod": average_period,
                    "optimal": optimal,
                    "subOptimal": subOptimal,
                    "url": url,
                }

            # print(f"result: {result}")

        return result

    except Exception as e:
        print(f"get_blogstadard_api : {e}")
        raise Exception("일일 사용량 초과")


def get_driver(data):
    try:
        user_id = data["user_id"]
        user_pw = data["user_pw"]
        keywords = data["keywords"]

        url = "https://blogstand.net/login/loginForm.do"

        # options = webdriver.ChromeOptions()

        # # 지정한 user-agent로 설정

        # # 맥
        # # options.add_argument(
        # #     "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
        # #     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664 Safari/537.36"
        # # )

        # # 윈도우
        # options.add_argument(
        #     "user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64 )\
        #      AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        # )

        # # 브라우저가 백그라운드에서 실행됩니다.

        # # chromedriver 열기
        # options.add_argument("headless")  # 브라우저가 백그라운드에서 실행됩니다.
        # options.add_argument("start-maximized")  # 창 최대화
        # options.add_argument("--no-sandbox")  # root 권한으로 실행
        # options.add_argument("--disable-dev-shm-usage")  # 메모리 사용량 제한 해제 (크롬 59 이상부터 필요)
        # options.add_argument("disable-infobars")  # 테스트 중 자동화된 테스트 소프트웨어라는 문구가 뜨는 것을 막아줌
        # options.add_argument("--disable-extensions")  # 확장 프로그램 사용 안함
        # options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 로그 무시

        # driver = webdriver.Chrome(
        #     service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        #     options=options,
        # )

        # chrome_options = uc.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--window-size=1920,1080")

        # # update user-agent
        # chrome_options.add_argument(
        #     "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
        #     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664 Safari/537.36"
        # )
        # chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-application-cache")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--remote-debugging-port=9222")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-setuid-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})

        # driver = uc.Chrome(headless=True, use_subprocess=False, options=chrome_options)

        # 'undetected_chromedriver'를 가져옵니다.

        # ChromeOptions 객체를 생성합니다.
        chrome_options = uc.ChromeOptions()

        # 브라우저를 GUI 없이 백그라운드에서 실행하도록 합니다.
        chrome_options.add_argument("--headless")

        # 브라우저 창 크기를 설정합니다.
        chrome_options.add_argument("--window-size=1920,1080")

        # 브라우저의 사용자 에이전트를 설정합니다.
        chrome_options.add_argument(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Whale/3.21.192.18 Safari/537.36"
        )

        # 브라우저를 시크릿 모드로 실행합니다.
        chrome_options.add_argument("--incognito")

        # 브라우저 확장 기능을 비활성화합니다.
        chrome_options.add_argument("--disable-extensions")

        # 어플리케이션 캐시를 비활성화합니다.
        chrome_options.add_argument("--disable-application-cache")

        # GPU 가속을 비활성화합니다.
        chrome_options.add_argument("--disable-gpu")

        # 원격 디버깅 포트를 설정합니다.
        chrome_options.add_argument("--remote-debugging-port=9222")

        # 보안 샌드박스 모드를 비활성화합니다.
        chrome_options.add_argument("--no-sandbox")

        # setuid 샌드박스를 비활성화합니다.
        chrome_options.add_argument("--disable-setuid-sandbox")

        chrome_options.add_argument("--disable-popup-blocking")

        # /dev/shm 사용을 비활성화합니다. Docker 환경에서 발생할 수 있는 문제를 방지합니다.
        chrome_options.add_argument("--disable-dev-shm-usage")

        # 브라우저가 자동화 테스트 소프트웨어에 의해 제어되고 있음을 나타내는 JavaScript 속성을 비활성화합니다.
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # 실험적인 옵션을 추가합니다. 이 경우 자격 증명 서비스와 비밀번호 관리자를 비활성화하며, 팝업 알림을 비활성화합니다.
        chrome_options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2,  # 팝업 비활성화
            },
        )

        # driver = uc.Chrome(options=chrome_options)
        with uc.Chrome(options=chrome_options) as driver:
            driver.get(url)

            # wait until someid is clickable
            wait = WebDriverWait(driver, 2)
            wait.until(EC.element_to_be_clickable((By.NAME, "id")))

            # 일반적으로 진행하려고 해면 영수증 캡차가 나옴, pyperclip을 사용해야 함
            tag_id = driver.find_element(By.ID, "username")
            tag_pw = driver.find_element(By.ID, "password")

            tag_id.send_keys(user_id)
            tag_pw.send_keys(user_pw)

            # 로그인 버튼을 클릭합니다
            login_btn = driver.find_element(By.ID, "loginBtn")
            login_btn.click()
            time.sleep(2)

            results = {}

            for keyword in keywords:
                static_url = f"https://blogstand.net/naver/searchKeyword.do?keyword={keyword}&searchType=all&sortOption=sim&dateOption=all&startDate=&endDate=&viewMoreCount="

                driver.get(static_url)
                time.sleep(2)

                results[keyword] = get_blogstadard_api(driver)
                time.sleep(2)

            return results

    except WebDriverException as e:
        print(f"Error with WebDriver: {e}")

    except Exception as e:
        print(f"에러: {e}")

    finally:
        driver.close()


if __name__ == "__main__":
    #     # user1
    #     user_id = "phantom92121@naver.com"
    #     user_pw = "#dltkd11"

    # # user2
    # # user_id = "help@isanghan.co.kr"
    # # user_pw = "#dltkdgks9711#"

    # # user3
    # # user_id = "isanghan12@naver.com"
    # # user_pw = "isanghan12"

    # # keyword = "신사동맛집"

    data = {"user_id": "isanghan12@naver.com", "user_pw": "isanghan12", "keywords": ["신사동카페", "신사동맛집", "신사동술집"]}

    result = get_driver(data)
    print(result)
