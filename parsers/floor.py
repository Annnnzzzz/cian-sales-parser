from utils.parse_utils import m, get_element_from_json


def get_floor(meta: dict, soup, factoids):
    floor, floors_total = get_floor_from_json(meta)
    if floor is None or floors_total is None:
        floor, floors_total = get_floor_from_html(soup, factoids)
    return floor, floors_total


def get_floor_from_json(meta):
    return get_element_from_json(meta, "floor"), get_element_from_json(meta, "floors_total"),


def get_floor_from_html(soup, factoids):
    for text in factoids:
        floor, floors_total = m(text, "floor")
        if floor is not None and floors_total is not None:
            return floor, floors_total
    return None, None
