from utils.parse_utils import get_element_from_json
from utils.config import SEARCH_CONFIGS
from utils.parse_utils import m


def get_area(meta, items, title, factoids):
    area = items.get('Общая площадь')
    living_area = items.get('Жилая площадь')
    kitchen_area = items.get('Площадь кухни')
    if area is None or living_area is None or kitchen_area is not None:
        area1, living_area1, kitchen_area1 = get_params_from_json(meta)
        if area is None:
            area = area1
        if living_area is None:
            living_area = living_area1
        if kitchen_area is None:
            kitchen_area = kitchen_area1
    if area is None or living_area is None:
        area2, living_area2, kitchen_area2 = get_area_from_html(title, factoids)
        if area is None:
            area = area2
        if living_area is None:
            living_area = living_area2
        if kitchen_area is None:
            kitchen_area = kitchen_area2
    return area, living_area, kitchen_area


def get_area_from_html(title, factoids):
    living_area = None
    kitchen_area = None
    area = get_areas(title, "title")
    for text in factoids:
        if living_area is None:
            living_area = get_areas(text, "living")
        if kitchen_area is None:
            kitchen_area = get_areas(text, "kitchen")
        if area is None:
            area = get_areas(text, "description")
        if area is None:
            area = get_areas(text, "general")
        if area is not None and living_area is not None and kitchen_area is not None:
            return area, living_area, kitchen_area
    return area, living_area, kitchen_area


def get_params_from_json(meta):
    return (get_element_from_json(meta, "area"), get_element_from_json(meta, "living_area"),
            get_element_from_json(meta, "kitchen_area"),)


def get_areas(text, search_type):
    try:
        if any(phrase in text.lower() for phrase in SEARCH_CONFIGS["area"][search_type]):
            return m(text, "area")
    except Exception:
        pass
    return None
