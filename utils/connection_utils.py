from utils.config import *
from bs4 import BeautifulSoup
import time
import requests
import random


def get_response(session, url):
    global CUR_NUM
    print(CUR_PROXY)
    if CUR_PROXY is None:
        response = session.get(url, timeout=REQUEST_TIMEOUT)
    else:
        proxy = PROXY_LIST[CUR_NUM]
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        response = session.get(url, timeout=REQUEST_TIMEOUT, proxies=proxies)
    if response.status_code == 429 or response.status_code == 403:
        print("Меняем прокси", response.status_code)
        for i in range(10):
            CUR_NUM = (CUR_NUM + 1) % len(PROXY_LIST)
            proxy = PROXY_LIST[CUR_NUM]
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            delay = DELAY_BETWEEN_REQUESTS['max']
            time.sleep(max(delay,
                       2 ** i + random.uniform(DELAY_BETWEEN_REQUESTS['min'], DELAY_BETWEEN_REQUESTS['max'])))
            new_session = requests.Session()

            new_session.headers.update(session.headers)

            response = new_session.get(url, timeout=REQUEST_TIMEOUT, proxies=proxies)
            print(f"Новый прокси {i + 1}: {response.status_code}")
            if response.status_code == 200:
                response_text = response.text
                soup = BeautifulSoup(response_text, 'html.parser')
                return response_text, soup

    if response.status_code != 200:
        raise Exception
    response_text = response.text
    soup = BeautifulSoup(response_text, 'html.parser')
    return response.text, soup
