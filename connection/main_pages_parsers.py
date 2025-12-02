import requests
import time
import re
from .offer_pages_parsers import parse_offer_page
from urllib.parse import urljoin
from utils.connection_utils import get_response
from utils.config import *


def parse_cian_offers(main_url):
    """Парсинг объявлений на главной странице, передает id квартир в parse_offer_page и возвращает список с информацией о квартирах"""
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        response_text, soup = get_response(session, main_url)
        offer_ids = get_offer_ids(response_text, soup)
        offers = []
        print("offers", offer_ids)

        for offer_id in offer_ids:
            try:
                offer = parse_offer_page(session, offer_id)
                if offer:
                    offers.append(offer)
            except Exception:
                continue
            time.sleep(DELAY_BETWEEN_REQUESTS)
        return offers, get_next_page_url(soup)

    except Exception:
        return [], None


def get_next_page_url(soup):
    """Поиск ссылки на следующую страницу"""
    next_span = soup.find('span', text='Дальше')
    if next_span:
        next_link = next_span.find_parent('a')
        if next_link:
            return urljoin(BASE_URL, next_link.get('href'))

    return None


def get_offer_ids(html_content, soup):
    """Получение id объявлений, возвращает список id на странице"""
    offer_ids = []
    print(html_content)
    for pattern in PATTERNS["offers"]:
        print("patt")
        matches = re.findall(pattern, html_content, re.DOTALL)
        print("matches", matches)
        for match in matches:
            print("match", match)
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
        if is_valid_id(oid):
            valid_ids.append(oid)
    return valid_ids


def is_valid_id(oid):
    if len(oid) >= 6 and not oid.startswith(('0', '00')):
        try:
            if int(oid) > 100000:
                return True
        except:
            pass
    return False
