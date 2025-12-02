from models.flat import Flat
from utils.connection_utils import get_response
def parse_offer_page(session, offer_id):
    """Парсинг самих объявлений, принимает id и составляет url на конкретное объявление"""
    url = f"https://www.cian.ru/sale/flat/{offer_id}/"
    try:
        response_text, soup = get_response(session, url)
        return Flat(offer_id, url, response_text, soup).get_data()
    except Exception:
        return None