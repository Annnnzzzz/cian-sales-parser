HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

REQUEST_TIMEOUT = 15
DELAY_BETWEEN_REQUESTS = {
    'min': 5,
    'max': 15
}
BASE_URL = "https://www.cian.ru/cat.php?deal_type=sale&p=2"

CAND_PATHS = {
    "price": [
        ('page', 'products', 0, 'price'),
        ('offer', 'product', 'price'),
        ('product', 'price'),
    ],
    "rooms": [
        ('offer', 'roomsCount'),
        ('product', 'rooms'),
        ('page', 'extra', 'rooms'),
    ],
    "coordinates": [
        ('offer', 'coordinates', 'lat'),
        ('offer', 'coordinates', 'lng'),
        ('page', 'geo', 'coordinates', 'lat'),
        ('page', 'geo', 'coordinates', 'lng'),
        ('product', 'lat'),
        ('product', 'lng'),
        ('coordinates', 'lat'),
        ('coordinates', 'lng'),
        ('geo', 'lat'),
        ('geo', 'lng'),
    ],
    "area": [
        ('offer', 'area', 'total'),
        ('offer', 'area', 'value'),
        ('product', 'area'),
        ('page', 'extra', 'total_area'),
    ],
    "living_area": [
        ('offer', 'area', 'living'),
        ('offer', 'livingArea'),
        ('page', 'extra', 'living_area'),
    ],
    "kitchen_area": [
        ('offer', 'kitchenArea'),
        ('offer', 'area', 'kitchen'),
        ('page', 'kitchen_area'),
    ],
    "floor": [
        ('offer', 'floor'),
        ('product', 'floor'),
        ('page', 'extra', 'floor'),
    ],
    "floors_total": [
        ('offer', 'floorsTotal'),
        ('offer', 'house', 'floors'),
        ('page', 'extra', 'floors_total'),
    ],
    "year_built": [
        ('offer', 'house', 'year'),
        ('page', 'extra', 'year_built'),
    ]
}

SELECTORS = {
    'address': [
        'div[data-name="AddressContainer"]',
        'div[data-name="OfferAddress"]',
        '[class*="address"]',
        '.offer__address',
    ],
    'price': [
        'span[data-mark="MainPrice"]',
        '[data-testid="price-amount"]',
    ],
    'title': [
        'h1[data-name="OfferTitle"]',
        'h1[class*="title"]',
    ],
    'factoids': 'div[data-name="ObjectFactoidsItem"]',
    'metro': 'li[data-name="UndergroundItem"]',
    'station': '.xa15a2ab7--d9f62d--underground_link',
    'metro_icon': '[data-name="UndergroundIcon"]',
    'metro_time': '.xa15a2ab7--d9f62d--underground_time'
}

PATTERNS = {
    "rooms": [
        r'(\d+)[-\s]*комн',
        r'(\d+)[-\s]*к\.',
        r'(\d+)-комнатная',
        r'(\d+)\s*комнат',
        r'(\d+)\s*(?:комн|комнат|к\.)'
    ],
    "coordinates": [
        r'"coordinates"\s*:\s*{\s*"lat"\s*:\s*([\d.-]+)\s*,\s*"lng"\s*:\s*([\d.-]+)',
        r'"center"\s*:\s*{\s*"lat"\s*:\s*([\d.-]+)\s*,\s*"lng"\s*:\s*([\d.-]+)',
        r'"latitude"\s*:\s*([\d.-]+)\s*,\s*"longitude"\s*:\s*([\d.-]+)',
        r'center=([\d.]+)%2C([\d.]+)',
        r'center=([\d.]+),([\d.]+)',
    ],
    "floor": [
        r'(\d+)\s*/\s*(\d+)',
        r'(\d+)\s*из\s*(\d+)',
        r'этаж\s*(\d+)\s*из\s*(\d+)',
    ],
    "offers": [
        r'href="([^"]*?\/sale\/flat\/\d+[^"]*?)"',
        r'href="https?://www\.cian\.ru/sale/flat/(\d+)/"',  # Строгий
        r'href="[^"]*?//www\.cian\.ru/sale/flat/(\d+)/[^"]*?"',  # Гибкий
        r'/sale/flat/(\d+)/',  # Простой
        r'href="[^"]*?cian\.ru/sale/flat/(\d+)/[^"]*?"',  # Еще более гибкий
        r'href="\s*https?://www\.cian\.ru/sale/flat/(\d+)/\s*"',  # С пробелами
        r'href="[^"]*?//www\.cian\.ru/sale/flat/(\d+)/[^"]*?"',  # Универсальный
        r'/sale/flat/(\d+)/',
        r'href="https?://www\.cian\.ru/sale/flat/(\d+)/"',  # Для https
        r'href="http://www\.cian\.ru/sale/flat/(\d+)/"',
        r'href="https?://www\.cian\.ru/sale/flat/(\d+)/"',
        r'href="(/sale/flat/(\d+)/)"',
        r'"offers"\s*:\s*\[(.*?)\]',
        r'"items"\s*:\s*\[(.*?)\]',
    ],
    "offers_data": [
        r'var\s+i\s*=\s*{',
        r'window\._cianConfig\s*=\s*{',
        r'dataLayer\.push\(\s*{'
    ],

    "area": [r'(\d+(?:[.,]\d+)?)[\s\xa0\u2002\u2003\u2009\u202F\u205F]*м²'],
    "id": r'"id"\s*:\s*(\d{6,12})',
    "sale": r'/sale/flat/\d+/',
    "flat": r'/flat/(\d{6,12})/',
    "year_built": [r'(\d{4})'],
    "factoids": r'([а-я])(\d)',
    "time": [r'(\d+)\s*мин']
}

SEARCH_CONFIGS = {
    'area': {
        'title': [],
        'area': ['общая площадь', 'площадь', 'м²'],
        'living_area': ['жилая', 'жилая площадь'],
        'kitchen_area': ['площадь кухни', 'кухонная площадь'],
    },
    'rooms': ['комн', 'комнат', 'к.'],
    'year_built': ['год', 'постр', 'строен']
}

COORDS_CONFIGS = {
    'lat': ['lat', 'latitude'],
    'lon': ['lng', 'lon', 'longitude']
}

REPL = r'\1 \2'

METRO_WAY = {
    'M8.67 4.471c.966 0 1.75-.778 1.75-1.738S9.636.993 8.67.993c-.967 0-1.75.78-1.75 1.74A1.74 1.74 0 0 0 8.142 '
    '4.39L3.743 5.68 2.605 8.65l1.868.715.783-2.045 1.12-.328L3.449 15h2.13l.094-.259-.017-.006 '
    '2.557-6.937.258-.707L9.662 8H13V6h-2.662L8.275 4.427c.127.03.26.044.395.044Z': 'пешком',
    'm14 7-.84-4.196A1 1 0 0 0 12.18 2H3.82a1 1 0 0 0-.98.804L2 7 1 8v4a1 1 0 0 0 1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 '
    '1-1v-1h6v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0 1-1V8l-1-1Zm-2.64-3H4.64L4 7h8l-.64-3ZM3 10a1 1 0 1 1 2 0 '
    '1 1 0 0 1-2 0Zm9-1a1 1 0 1 0 0 2 1 1 0 0 0 0-2Z': 'на транспорте'
}

CUR_PROXY = None
PROXY_LIST = []
CUR_NUM = -1
