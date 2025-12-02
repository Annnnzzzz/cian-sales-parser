from utils.models_utils import *
from utils.parse_utils import *
from parsers import *
import datetime, time


class Flat:
    def __init__(self, offer_id, url, response_text, soup):
        self.id = offer_id
        self.url = url

        html = response_text
        meta = extract_json(html)
        items = offer_items(soup)
        self.type_of_flat = items.get("Тип жилья")
        factoids = get_factoids(soup)
        self.title = get_element_text(soup, SELECTORS["title"])
        self.price = get_price(meta, offer_id, soup)
        self.rooms = get_rooms(meta, soup, self.title, factoids)
        self.address = get_address(meta, soup)
        self.latitude, self.longitude = get_coordinates(meta, soup)
        self.area, self.living_area, self.kitchen_area = get_area(meta, items, self.title, factoids)
        self.ceiling_height = items.get("Высота потолков")
        self.floor, self.floors_total = get_floor(meta, soup, factoids)
        self.year_build = get_year_built(meta, soup, items, factoids)
        self.repair = items.get("Ремонт")
        if self.year_build is not None and self.year_build >= datetime.date.today().year:
            if self.repair is None:
                self.repair = items.get("Отделка")
        self.type_of_building = items.get("Тип дома")
        self.parking = items.get("Парковка")
        self.metro = get_metro(soup)
        self.parsed_at = time.strftime('%Y-%m-%d %H:%M:%S')

    def get_data(self):
        data = self.__dict__
        data.pop('meta', None)
        data.pop('soup', None)
        return data

