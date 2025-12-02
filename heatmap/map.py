import pandas as pd
import numpy as np
import h3
import folium
from folium.plugins import HeatMap
import json
import re
import ast


def extract_numeric_value(value_str):
    """Форматируем площадь"""
    if pd.isna(value_str):
        return None
    cleaned = re.sub(r'[^\d,\.]', '', str(value_str))
    cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except:
        return None


def calculate_price_per_sqm(row):
    """Вычисляет цену за квадратный метр"""
    try:
        price = float(row['price'])
        area = extract_numeric_value(row['area'])

        if area and area > 0:
            return price / area
        return None
    except:
        return None


def create_hexbin_map(csv_file_path, output_file='hexbin_map.html', resolution=8):
    """
    Создает тепловую карту с гексагонами стоимости квадратного метра
    resolution: разрешение H3 гексагонов (6-10, чем больше - тем мельче гексагоны)
    """
    print(csv_file_path)
    df = pd.read_csv(csv_file_path)

    processed_data = []

    for _, row in df.iterrows():
        try:
            price_per_sqm = calculate_price_per_sqm(row)

            if price_per_sqm and not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
                lat, lon = float(row['latitude']), float(row['longitude'])


                hex_id = h3.latlng_to_cell(lat, lon, resolution)

                processed_data.append({
                    'id': row['id'],
                    'latitude': lat,
                    'longitude': lon,
                    'price_per_sqm': price_per_sqm,
                    'price': float(row['price']),
                    'area': extract_numeric_value(row['area']),
                    'rooms': row['rooms'],
                    'hex_id': hex_id,
                    'address': row['address']
                })
        except Exception as e:
            print(f"Ошибка обработки строки {row['id']}: {e}")
            continue


    processed_df = pd.DataFrame(processed_data)

    if processed_df.empty:
        print("Нет данных для построения карты")
        return


    hex_stats = processed_df.groupby('hex_id').agg({
        'price_per_sqm': 'mean',
        'latitude': 'first',
        'longitude': 'first',
        'id': 'count'
    }).rename(columns={'id': 'apartment_count'}).reset_index()


    center_lat = processed_df['latitude'].mean()
    center_lon = processed_df['longitude'].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles='CartoDB positron'
    )


    for _, hex_row in hex_stats.iterrows():
        hex_id = hex_row['hex_id']
        price_per_sqm = hex_row['price_per_sqm']
        apartment_count = hex_row['apartment_count']


        hex_boundary = h3.cell_to_boundary(hex_id)
        coordinates = [[lat, lng] for lat, lng in hex_boundary]


        max_price = hex_stats['price_per_sqm'].max()
        min_price = hex_stats['price_per_sqm'].min()

        if max_price > min_price:
            normalized_price = (price_per_sqm - min_price) / (max_price - min_price)
        else:
            normalized_price = 0.5


        colors = [
            "#2E8B57",  # морской зеленый
            "#3CB371",  # средний весенний зеленый
            "#90EE90",  # светло-зеленый
            "#98FB98",  # бледно-зеленый
            "#ADFF2F",  # зелено-желтый
            "#BFFF00",  # лаймовый
            "#DFFF00",  # желто-лаймовый
            "#FFFF00",  # желтый
            "#FFFA00",  # ярко-желтый
            "#FFF200",  # лимонно-желтый
            "#FFE800",  # солнечный желтый
            "#FFDD00",  # золотой желтый
            "#FFD200",  # шафрановый
            "#FFC800",  # желто-оранжевый
            "#FFBD00",  # оранжево-желтый
            "#FFB300",  # оранжевый
            "#FFA500",  # стандартный оранжевый
            "#FF9500",  # темно-оранжевый
            "#FF8500",  # красно-оранжевый
            "#FF7500",  # оранжево-красный
            "#FF6500"  # красновато-оранжевый
        ]

        color_idx = int(normalized_price * (len(colors) - 1))
        color_idx = max(0, min(len(colors) - 1, color_idx))
        color = colors[color_idx]


        folium.Polygon(
            locations=coordinates,
            popup=folium.Popup(
                f"""
                <b>Средняя цена за м²:</b> {price_per_sqm:,.0f} руб.<br>
                <b>Количество квартир:</b> {apartment_count}<br>
                <b>H3 индекс:</b> {hex_id}
                """,
                max_width=300
            ),
            tooltip=f"Цена за м²: {price_per_sqm:,.0f} руб. ({apartment_count} кв.)",
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            color='black',
            weight=1,
            opacity=0.8
        ).add_to(m)

    median_price_per_sqm = processed_df['price_per_sqm'].median()


    min_price_val = hex_stats['price_per_sqm'].min()
    max_price_val = hex_stats['price_per_sqm'].max()

    legend_html = f'''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 350px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px; border-radius: 5px;">
    <p style="margin: 0 0 8px 0; font-weight: bold; font-size: 16px;"> Средняя стоимость м²</p>

    <!-- Цветовая шкала -->
     <div style="background: linear-gradient(to right, #008300, #00A700, #14C514, #33d633, #89ff89, #80ff00, #ffff00, #ffaa00, #ff8000, #ff5500, #ff2a00, #ff0000, #e60000, #cc0000, #b30000, #990000); 
        width: 100%; height: 15px; border: 1px solid #ccc; margin-bottom: 5px;"></div>

    <!-- Границы стоимости -->
    <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 8px;">
        <span>{min_price_val:,.0f}₽</span>
        <span style="color: green; font-weight: bold;">{median_price_per_sqm:,.0f}₽ (медиана)</span>
        <span>{max_price_val:,.0f}₽</span>
    </div>

    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))


    m.save(output_file)
    print(f"Карта сохранена как {output_file}")
    print(f"Обработано {len(processed_df)} квартир")
    print(f"Создано {len(hex_stats)} гексагонов")
    print(f"Диапазон цен за м²: {hex_stats['price_per_sqm'].min():,.0f} - {hex_stats['price_per_sqm'].max():,.0f} руб.")


def create_hexbin_map_from_json(json_file_path, output_file='hexbin_map.html', resolution=8):
    """
    Создает карту из JSON файла
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)


    offers = data['offers']
    df_data = {
        'id': [offers['id']],
        'latitude': [offers['latitude']],
        'longitude': [offers['longitude']],
        'price': [offers['price']],
        'area': [offers['area']],
        'rooms': [offers['rooms']],
        'address': [offers['address']]
    }

    df = pd.DataFrame(df_data)
    create_hexbin_map_from_dataframe(df, output_file, resolution)


def create_hexbin_map_from_dataframe(df, output_file='hexbin_map.html', resolution=8):
    """
    Создает карту напрямую из DataFrame
    """

    temp_csv = 'temp_data.csv'
    df.to_csv(temp_csv, index=False, encoding='utf-8')
    create_hexbin_map(temp_csv, output_file, resolution)

    # Удаляем временный файл
    import os
    os.remove(temp_csv)