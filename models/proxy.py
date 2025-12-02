import time
import requests
from utils.config import HEADERS, BASE_URL, PROXY_LIST


class Proxy:
    def __init__(self, proxy):
        self.proxies = {
            'http': proxy,
            'https': proxy
        }
        self.check_proxy()

    def check_proxy(self, timeout=2):
        self.speed = None
        self.check = False
        try:
            start_time = time.time()
            response = requests.get(
                BASE_URL,
                proxies=self.proxies,
                timeout=timeout,
                headers=HEADERS
            )
            response_time = time.time() - start_time
            if response.status_code == 200:
                self.speed = response_time
                self.check = True
        except Exception as e:
            pass

    def __lt__(self, other):
        return self.speed < other.speed
def load_proxies():
    global PROXY_LIST
    print("try to load proxy")
    try:
        with open("/results/other/proxies.txt", 'r', encoding='utf-8') as file:
            print('opened')
            for line in file:
                try:
                    p = line.strip()
                    if p is not None:
                        PROXY_LIST.append(p)
                except Exception:
                    continue
    except Exception:
        pass


def ready_proxy():
    print("loading")
    proxies = load_proxies()
    proxies_list = []
    for p in proxies:
        print("check")
        ready_p = Proxy(p)
        if ready_p.check is True:
            proxies_list.append(ready_p)
    return sorted(proxies_list)
