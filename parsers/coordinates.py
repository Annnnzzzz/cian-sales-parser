from utils.parse_utils import safe_path, m
from utils.config import CAND_PATHS, COORDS_CONFIGS


def get_coordinates(meta: dict, soup):
    lat, lon = get_coordinates_from_json(meta)
    if lat is None or lon is None:
        lat, lon = get_coordinates_from_html(soup)
    if lat is not None and lon is not None:
        return round(lat, 6), round(lon, 6)
    return None, None


def find_json_coordinates(meta, key):
    try:
        for path in CAND_PATHS["coordinates"]:
            try:
                if path[-1] in COORDS_CONFIGS[key]:
                    val = safe_path(meta, path)
                    if val is not None:
                        return float(val)
            except Exception:
                continue
    except Exception:
        pass
    return None


def get_coordinates_from_json(meta):
    lat = find_json_coordinates(meta, "lat")
    lon = find_json_coordinates(meta, "lon")
    if lat is not None and lon is not None:
        if 55.0 <= lat <= 56.5 and 36.0 <= lon <= 38.5:
            return lat, lon

    return None, None


def get_coordinates_from_html(soup):
    script_tags = soup.find_all('script')
    for script in script_tags:
        if script.string:
            lat, lon = m(script.string, "coordinates")
            if lat is not None and lon is not None:
                return lat, lon

    meta_el = soup.find('meta', {'property': 'og:image'})
    if meta_el and meta_el.get('content'):
        content = meta_el['content']
        lat, lon = m(content, "coordinates")
        if lat is not None and lon is not None:
            return lat, lon

    return None, None
