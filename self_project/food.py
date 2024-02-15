from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import json

slack_webhook_url = "https://hooks.slack.com/services/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"
url='https://www.instagram.com/casamia__food/'

def send_slack_webhook(str_text):
    """
    입력된 텍스트를 Slack 웹훅으로 전송하는 함수
    Args: str_text (str): 전송할 텍스트
    Returns: str: 전송 결과 ("OK" 또는 "error")
    """
    headers = {
        "Content-type": "application/json"
    }
    data = {
        "text": str_text
    }
    res = requests.post(slack_webhook_url, headers=headers, data=json.dumps(data))
    if res.status_code == 200:
        return "OK"
    else:
        return "error"
    
def select_first(driver):
    first = driver.find_elements(By.CSS_SELECTOR, "div._aagw")[0]
    first.click()
    time.sleep(1)

def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    try:
        content = soup.select('div._a9zs')[0].text
    except IndexError:
        content = ''

    tags = re.findall(r'#[^\s#,\\]+', content)
    date = soup.select('time._aaqe')[0]['datetime'][:10]
    data = [content, date, tags]
    return data

options = Options()
# 필요한 옵션을 여기에 추가하세요
driver = webdriver.Chrome(options=options)

driver.get(url)
time.sleep(1)

email = '01080338529'
input_id = driver.find_element(By.CSS_SELECTOR, "#loginForm > div > div:nth-child(1) > div > label > input")
input_id.clear()
input_id.send_keys(email)

password = 'kim@80338529'
input_pw = driver.find_element(By.CSS_SELECTOR, '#loginForm > div > div:nth-child(2) > div > label > input')
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()

time.sleep(5)

# 로그인 정보 저장 여부 ("나중에 하기 버튼 클릭")
try:
    btn_later1 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div')
    btn_later1.click()
except Exception as e:
    print(f"Exception while clicking '나중에 하기' button 1: {e}")

time.sleep(5)

# 알림 설정 ("나중에 하기 버튼 클릭")
try:
    btn_later2 = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
    btn_later2.click()
except Exception as e:
    print(f"Exception while clicking '나중에 하기' button 2: {e}")

select_first(driver)

result = []

try:
    data = get_content(driver)
    result.append(data)
except IndexError:
    print("안됌포기하셈")
    time.sleep(2)

print("구내식당 : ",end='')
list=result[0]
menu=list[2]
print(menu[:8])#보통 메뉴 개수가 6~8개 정도

#메세지 전송
message = "까사미아 구내식당 : {}\n 참고:{}".format(menu[:8],url)
print(send_slack_webhook(message))
