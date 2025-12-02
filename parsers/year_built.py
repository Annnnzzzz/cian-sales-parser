from utils.parse_utils import m, get_element_from_json
from utils.config import SEARCH_CONFIGS


def get_year_built(meta, soup, items, factoids):
    year_built = items.get("Год постройки")
    if year_built is None:
        year_built = items.get("Год сдачи")
    if year_built is not None:
        try:
            return int(year_built)
        except Exception:
            year_built = None
    if year_built is None:
        year_built = get_year_built_from_json(meta)
    if year_built is None:
        year_built = get_year_built_from_html(soup, factoids)
    return year_built

def get_year_built_from_json(meta):
    return get_element_from_json(meta, "year_built")


def get_year_built_from_html(soup, factoids):
    for text in factoids:
        if any(word in text.lower() for word in SEARCH_CONFIGS["year_built"]):
            year_build = m(text, "year_built")
            if year_build is not None:
                return year_build
    return None
