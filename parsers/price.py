from utils.config import *
from utils.parse_utils import safe_path, integer, get_element_text


def get_price(meta: dict, offer_id, soup) -> int:
    price = get_price_from_json(meta, offer_id)
    if price is None:
        price = get_price_from_html(soup)
    return price


def get_price_from_json(meta, offer_id):
    products = meta.get('products')

    if isinstance(products, list):
        for p in products:
            try:
                if str(p.get('cianId')) == str(offer_id) and isinstance(p.get('price'), int):
                    return int(p['price'])
            except Exception:
                pass

    for path in CAND_PATHS["price"]:
        val = safe_path(meta, path)
        if isinstance(val, int):
            return int(val)
    return None


def get_price_from_html(soup):
    text = get_element_text(soup, SELECTORS['price'])
    try:
        return integer(text)
    except Exception:
        return None
