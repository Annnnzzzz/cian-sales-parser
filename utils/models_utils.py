from utils.config import *
import json
import re


def read_balanced_braces(s, start_idx):
    """Работает с вложенными объектами по принципу работу с ПСП, возвращает кортеж из строки для парсинга и позицию строки после последней скобки,
    второе сейчас фактически не используется, но может быть использовано для отладки или продолжения поиска"""
    if start_idx >= len(s) or s[start_idx] != '{':
        return None, None
    i = start_idx
    depth = 0
    in_str = False
    esc = False
    while i < len(s):
        ch = s[i]
        if in_str:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return s[start_idx:i + 1], i + 1,
        i += 1
    return None, None


def extract_json(html):
    """Ищет в HTML шаблоны, передает его для дальнейшего парсинга,
     в случае успеха преобразует полученные данные в словарь"""
    d = {}
    for pattern in PATTERNS["offers_data"]:
        try:
            mm = re.search(pattern, html)
            start = mm.end() - 1
            obj, end = read_balanced_braces(html, start)
            if obj:
                data = json.loads(obj)
                d.update(data)

        except Exception:
            continue
    return d


def get_factoids(soup):
    factoids = []
    facts = soup.select(SELECTORS["factoids"])
    for f in facts:
        factoids.append(re.sub(PATTERNS["factoids"], REPL, f.get_text(strip=True), flags=re.IGNORECASE))
    return factoids


def offer_items(soup):
    items = soup.find_all('div', {'data-name': 'OfferSummaryInfoItem'})
    result = {}

    for item in items:
        paragraphs = item.find_all('p')
        if len(paragraphs) >= 2:
            label = paragraphs[0].get_text(strip=True)
            value = paragraphs[1].get_text(strip=True)
            result[label] = value
    return result
