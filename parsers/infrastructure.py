from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json


def main_infr(url):
    parser = CianInfrastructureParser(headless=False)  # headless=False для отладки

    try:

        # Загружаем страницу
        if parser.load_page(url):
            print("Страница успешно загружена")

            # Парсим всю инфраструктуру
            infrastructure_data = parser.parse_all_infrastructure()

            # Сохраняем результаты
            with open('cian_infrastructure.json', 'w', encoding='utf-8') as f:
                json.dump(infrastructure_data, f, ensure_ascii=False, indent=2)

            # Выводим сводку
            print("\n=== РЕЗУЛЬТАТЫ ПАРСИНГА ===")
            for category, data in infrastructure_data.items():
                print(f"{data['name']}: {data['objects_count']} объектов")

        else:
            print("Не удалось загрузить страницу")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        parser.close()

class CianInfrastructureParser:
    def __init__(self, headless=True):
        self.setup_driver(headless)
        self.wait = WebDriverWait(self.driver, 15)

    def setup_driver(self, headless):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def load_page(self, url):
        """Загрузка страницы и ожидание карты"""
        self.driver.get(url)

        # Ждем загрузки карты инфраструктуры
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-name="InfrastructureWrapper"]'))
            )
            time.sleep(3)  # Дополнительное время для полной загрузки
            return True
        except TimeoutException:
            print("Карта инфраструктуры не загрузилась")
            return False

    def get_available_categories(self):
        """Получить список доступных категорий инфраструктуры"""
        categories = []

        try:
            category_items = self.driver.find_elements(
                By.CSS_SELECTOR,
                '[data-name="InfrastructureTypeItem"]'
            )

            for item in category_items:
                try:
                    category_data = {
                        'name': item.get_attribute('aria-label'),
                        'value': item.find_element(By.TAG_NAME, 'input').get_attribute('value'),
                        'russian_name': item.find_element(By.TAG_NAME, 'span').text,
                        'checked': item.find_element(By.TAG_NAME, 'input').is_selected(),
                        'element': item
                    }
                    categories.append(category_data)
                except Exception as e:
                    continue

        except NoSuchElementException:
            print("Категории не найдены")

        return categories

    def select_category(self, category_value):
        """Выбрать категорию инфраструктуры"""
        try:
            # Находим checkbox по value
            checkbox = self.driver.find_element(
                By.CSS_SELECTOR,
                f'input[value="{category_value}"]'
            )

            # Находим родительский label для клика
            label = checkbox.find_element(By.XPATH, "./..")

            # Кликаем только если категория не выбрана
            if not checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", label)
                time.sleep(2)  # Ждем загрузки данных
                return True
            else:
                print(f"Категория {category_value} уже выбрана")
                return True

        except NoSuchElementException:
            print(f"Категория {category_value} не найдена")
            return False

    def parse_map_objects(self):
        """Парсинг объектов на карте"""
        objects = []

        try:
            # Ждем появления меток на карте
            time.sleep(3)

            # Ищем все метки на карте
            map_pins = self.driver.find_elements(
                By.CSS_SELECTOR,
                '[data-testid^="MapPin-"]'
            )

            for pin in map_pins:
                try:
                    pin_data = {
                        'type': pin.get_attribute('data-testid').replace('MapPin-', ''),
                        'location': self.get_pin_position(pin),
                        'element': pin
                    }
                    objects.append(pin_data)
                except Exception as e:
                    continue

        except Exception as e:
            print(f"Ошибка при парсинге объектов: {e}")

        return objects

    def get_pin_position(self, pin_element):
        """Получить позицию метки на карте"""
        try:
            # Получаем стиль родительского элемента с координатами
            parent = pin_element.find_element(By.XPATH, "./ancestor::ymaps[contains(@class, 'placemark-overlay')]")
            style = parent.get_attribute('style')

            # Парсим координаты из стиля
            import re
            left_match = re.search(r'left:\s*(\d+)px', style)
            top_match = re.search(r'top:\s*(\d+)px', style)

            return {
                'left': int(left_match.group(1)) if left_match else None,
                'top': int(top_match.group(1)) if top_match else None
            }
        except:
            return {'left': None, 'top': None}

    def get_object_details(self, pin_element):
        """Получить детальную информацию об объекте (при клике)"""
        try:
            # Кликаем на метку
            self.driver.execute_script("arguments[0].click();", pin_element)
            time.sleep(1)

            # Ищем всплывающее окно с информацией
            popup = self.driver.find_elements(By.CSS_SELECTOR, '.map-popup, .balloon')
            if popup:
                popup_text = popup[0].text
                # Закрываем popup
                close_btn = self.driver.find_elements(By.CSS_SELECTOR, '.popup-close, .balloon-close')
                if close_btn:
                    close_btn[0].click()

                return popup_text

        except Exception as e:
            print(f"Ошибка при получении деталей: {e}")

        return None

    def parse_all_infrastructure(self):
        """Парсинг всей инфраструктуры по всем категориям"""
        all_data = {}

        # Получаем доступные категории
        categories = self.get_available_categories()
        print(f"Найдено категорий: {len(categories)}")

        for category in categories:
            print(f"Обрабатываю категорию: {category['russian_name']}")

            # Выбираем категорию
            if self.select_category(category['value']):
                # Парсим объекты
                objects = self.parse_map_objects()
                all_data[category['value']] = {
                    'name': category['russian_name'],
                    'objects_count': len(objects),
                    'objects': objects
                }

                print(f"  - Найдено объектов: {len(objects)}")

                # Небольшая пауза между категориями
                time.sleep(1)

        return all_data

    def close(self):
        """Закрыть браузер"""
        self.driver.quit()