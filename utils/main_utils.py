import time
import json
def save_to_json(offers, filename="apartments.json"):
    output_data = {
        'metadata': {
            'parsed_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_offers': len(offers),
            'source': 'cian.ru'
        },
        'offers': offers
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2, sort_keys=True)