from utils.parse_utils import safe_path, m
from utils.config import *


def get_rooms(meta, soup, title, factoids):
    rooms = get_rooms_from_json(meta)
    if rooms is None:
        rooms = get_rooms_from_html(soup, title, factoids)
    if rooms is None:
        if "Студия" in title:
            rooms = 0
    return rooms


def get_rooms_from_json(meta):
    try:
        for path in CAND_PATHS["rooms"]:
            val = safe_path(meta, path)
            if val is not None:
                if isinstance(val, int):
                    return int(val)
    except Exception:
        pass

    return None


def get_rooms_from_html(soup, title, factoids):
    r = m(title, "rooms")
    if r is not None:
        return r

    for text in factoids:
        if any(word in text.lower() for word in SEARCH_CONFIGS['rooms']):
            return m(text, "rooms")
    return None
