import requests
from urllib.parse import urljoin
from utils.connection_utils import get_response
from utils.config import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import chromedriver_autoinstaller


def parse_cian_id(main_url, session):
    """Парсинг объявлений на главной странице, передает id квартир в parse_offer_page и возвращает список с информацией о квартирах"""
    offers_ids = []
    while main_url is not None:
        try:
            response_text, soup = get_response(session, main_url)

            offers_ids+=get_offer_ids_id(response_text, soup)
            time.sleep(DELAY_BETWEEN_REQUESTS)

            new_url = get_next_page_url_id(soup, session, main_url)

            if new_url is None:
                try:
                    new_ids = load_next(session, main_url)

                    if new_ids is not None:
                        offers_ids+=new_ids
                except:
                    break
            main_url=new_url

        except Exception:
            break
    return offers_ids


def get_next_page_url_id(soup, session, current_url):
    """Поиск ссылки на следующую страницу"""
    next_span = soup.find('span', text='Дальше')
    if next_span:
        next_link = next_span.find_parent('a')
        if next_link:
            return urljoin(BASE_URL, next_link.get('href'))
    return None


def get_offer_ids_id(html_content, soup):
    """Получение id объявлений, возвращает список id на странице"""
    offer_ids = []

    for pattern in PATTERNS["offers"]:
        matches = re.findall(pattern, html_content, re.DOTALL)
        for match in matches:
            id_matches = re.findall(PATTERNS["id"], match)
            offer_ids.extend(id_matches)

    links = soup.find_all('a', href=re.compile(PATTERNS["sale"]))
    for link in links:
        href = link.get('href', '')
        mes = re.search(PATTERNS["flat"], href)
        if mes:
            offer_ids.append(mes.group(1))

    valid_ids = []
    for oid in set(offer_ids):
        if is_valid_id_id(oid):
            valid_ids.append(oid)
    return valid_ids


def is_valid_id_id(oid):
    if len(oid) >= 6 and not oid.startswith(('0', '00')):
        try:
            if int(oid) > 100000:
                return True
        except:
            pass
    return False


def load_next(session, main_url):
    """Подгружаем данные при помощи кнопки показать еще и selenium"""
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(main_url)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        button = find_button(driver)
        while button is not None:
            try:
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(1)

                driver.execute_script("arguments[0].click();", button)
                time.sleep(4)

                button = find_button(driver)

            except Exception as e:
                break
        final_html = driver.page_source
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(final_html, 'html.parser')
        all_offer_ids = get_offer_ids_id(final_html, soup)
        return all_offer_ids

    except Exception as e:
        print(f"Ошибка: {e}")
        return []
    finally:
        driver.quit()


def find_button(driver):
    try:
        return driver.find_element(By.XPATH, "//a[text()='Показать ещё']")
    except:
        try:
            return driver.find_element(By.XPATH, "//a[contains(text(), 'Показать')]")
        except:
            try:
                return driver.find_element(By.XPATH, "//*[contains(text(), 'Показать ещё')]")
            except:
                return None
