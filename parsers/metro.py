from utils.config import *
from utils.parse_utils import m


def get_metro(soup):
    return get_metro_from_html(soup)


def get_metro_from_html(soup):
    metro_items = soup.select(SELECTORS["metro"])
    if not metro_items:
        return None

    metro_list = []

    for metro_item in metro_items:
        try:
            metro_name_el = metro_item.select_one(SELECTORS["station"])
            metro_name = metro_name_el.get_text(strip=True) if metro_name_el else None

            metro_icon_el = metro_item.select_one(SELECTORS['metro_icon'])
            metro_icon_color = None
            if metro_icon_el and metro_icon_el.get('style'):
                metro_icon_color = metro_icon_el['style'].replace('color:', '').strip()

            time_el = metro_item.select_one(SELECTORS['metro_time'])
            metro_time_text = time_el.get_text(strip=True) if time_el else None

            metro_time_minutes = m(metro_time_text, 'time') if metro_time_text else None

            metro_way = None
            if time_el:
                time_icon_el = time_el.select_one('svg path')
                if time_icon_el:
                    metro_way = METRO_WAY.get(time_icon_el.get('d'))

            metro_list.append({
                'metro_name': metro_name,
                'metro_icon_color': metro_icon_color,
                'metro_time_text': metro_time_text,
                'metro_time_minutes': metro_time_minutes,
                'metro_way': metro_way
            })
        except Exception:
            continue

    return metro_list
