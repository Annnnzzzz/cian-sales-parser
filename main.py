from connection.id_parser import *
from connection.url import *
from connection.offer_pages_parsers import *
from utils.main_utils import save_to_json
from models.proxy import load_proxies
import datetime
from pathlib import Path
from heatmap.map import *
import requests
import pandas as pd
import time
import random

# Полный цикл - загружаем id, обрабатываем полученные странички, строим тепловую карту.
# Обрабатываем до 5 начальных url из списка, из них берем до 1000 страниц
if __name__ == "__main__":
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    json_dir = results_dir / "json_type"
    csv_dir = results_dir / "csv_type"
    heatmap_dir = results_dir / "Heat Maps"

    for dir_path in [json_dir, csv_dir, heatmap_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

    urls = create_urls()
    ids = []
    load_proxies()

    session = requests.Session()
    session.headers.update(HEADERS)
    for i in range  (0, min(len(urls), 5), 1):
        ids+=parse_cian_id(urls[i], session)
        delay = random.uniform(DELAY_BETWEEN_REQUESTS['min'], DELAY_BETWEEN_REQUESTS['max'])
        time.sleep(delay)

    print(f"Собрано {len(ids)} ID")
    apartments = []
    for i in range(0, min(1000, len(ids)), 1):
        try:
            new_apartment = (parse_offer_page(session, ids[i]))
            if new_apartment is not None:
                apartments.append(new_apartment)
            if ((i+1) % 100 == 0):
                print(f"Распарсили {len(apartments)} объявлений")

                if apartments:
                    df = pd.DataFrame(apartments)
                    csv_filename = f'offers_batch_{i + 1}_{timestamp}.csv'
                    csv_path = csv_dir / csv_filename
                    df.to_csv(csv_path, index=False, encoding='utf-8-sig')

                    json_filename = f'apartments_batch_{i + 1}_{timestamp}.json'
                    json_path = json_dir / json_filename
                    save_to_json(apartments, str(json_path))
            delay = random.uniform(DELAY_BETWEEN_REQUESTS['min'], DELAY_BETWEEN_REQUESTS['max'])
            time.sleep(delay)
        except Exception:
            continue

    print(f"Итог: {len(apartments)} объявлений")

    if apartments:
        df = pd.DataFrame(apartments)
        csv_filename = f'offers_final_{timestamp}.csv'
        csv_path = csv_dir / csv_filename
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"Финальный CSV: {csv_path}")

        json_filename = f'apartments_final_{timestamp}.json'
        json_path = json_dir / json_filename
        save_to_json(apartments, str(json_path))
        print(f"Финальный JSON: {json_path}")

        try:
            heatmap_input = Path("results/csv_type/sum_files/merged_data4.csv")
            heatmap_filename = f'apartments_hexbin_map_{timestamp}.html'
            heatmap_path = heatmap_dir / heatmap_filename
            create_hexbin_map(str(heatmap_input), str(heatmap_path), resolution=8)
            print(f"Тепловая карта: {heatmap_path}")
        except Exception as e:
            print(f"Ошибка создания тепловой карты: {e}")
