from utils.config import *
import re
def safe_first(*dicts_and_paths):
    dicts = dicts_and_paths[0]
    paths = dicts_and_paths[1]
    for path in paths:
        v = safe_path(dicts, path)
        if v is not None:
            return v
    return None


def get_element_from_json(meta, types):
    return integer(safe_first(meta, CAND_PATHS[types]))

def safe_path(d, path):
    """Безопасное обращение к элементам словаря"""
    cur = d
    for k in path:
        if isinstance(k, int):
            if isinstance(cur, list) and 0 <= k < len(cur):
                cur = cur[k]
            else:
                return None
        else:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                return None
    return cur

def integer(v):
    try:
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return int(v)
        digits = re.sub(r'\D+', '', str(v))
        return int(digits) if digits else None
    except Exception:
        return None

def m(text, types):
    for pattern in PATTERNS[types]:
        mes = re.search(pattern, text)
        if mes:
            try:
                match types:
                    case "area":
                        return float(mes.group(1).replace(',', '.'))
                    case "flat" | "rooms" | 'year_built' | 'time':
                        return int(mes.group(1))
                    case "floor":
                        floor_current = int(mes.group(1))
                        floor_total = int(mes.group(2))
                        return floor_current, floor_total
                    case "coordinates":
                        lat = float(mes.group(1))
                        lon = float(mes.group(2))
                        if 55.0 <= lat <= 56.5 and 36.0 <= lon <= 38.5:
                            return lat, lon
            except ValueError:
                continue
    match types:
        case "area", "rooms", "year_built":
            return None
        case "floor" | "coordinates":
            return None, None


def get_element_text(soup, selectors):
    for selector in selectors:
        el = soup.select_one(selector)
        if el:
            t = el.get_text(strip=True)
            if t:
                return t
    return None
