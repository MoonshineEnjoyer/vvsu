import abc


# Абстрактный класс
class Character(abc.ABC):
    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def attack(self):
        pass


# Наследование
class Warrior(Character):
    def attack(self):
        return f" {self.name} наносит сокрушительный удар мечом!"


class Mage(Character):
    def attack(self):
        return f" {self.name} выпускает магический огненный шар!"


# Функция, которая работает с разными типами объектов, т.е. полиморфизм
def make_hero_action(hero):
    print(hero.attack())


# Демонстрация
if __name__ == "__main__":
    heroes = [Warrior("Воин"), Mage("Маг"), Warrior("Рыцарь")]

    print("--- Симуляция боя ---")

    # Обработка списка объектов
    for h in heroes:
        make_hero_action(h)













!pip install google-colab-selenium

import time
import google_colab_selenium as gs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация браузера
driver = gs.Chrome()

try:
    print("Открытие тренировочного сайта Swag Labs...")
    driver.get("https://www.saucedemo.com")
    
    wait = WebDriverWait(driver, 10)
    
    # Шаг 3: Поиск полей и ввод данных (используем ID)
    print("Ввод тестовых данных...")
    username_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    password_field = driver.find_element(By.ID, "password")
    
    username_field.send_keys("standard_user")
    password_field.send_keys("secret_sauce")
    
    # Шаг 4: Клик по кнопке Login (используем ID кнопки)
    print("Нажатие на кнопку входа...")
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    
    # Шаг 5: Считывание информации из закрытой зоны
    print("Ожидание загрузки каталога товаров...")
    # Ждем появления названия первого товара в магазине (класс 'inventory_item_name')
    product_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name")))
    product_name = product_element.text.strip()
    
    full_output = f"Вход выполнен успешно! Первое доступное секретное имя товара в каталоге: {product_name}"
    
    print("\n--- ИЗВЛЕЧЕННЫЕ ДАННЫЕ ---")
    print(full_output)
    print("-------------------------\n")
    
    # Шаг 6: Запись результата в файл
    with open("secure_data.txt", "w", encoding="utf-8") as file:
        file.write(full_output)
    print("Данные успешно сохранены в файл 'secure_data.txt'!")

finally:
    print("Закрытие браузера.")
    driver.quit()




















import sys
import subprocess

# Автоматическая проверка и установка BeautifulSoup4 и requests
for lib in ['requests', 'beautifulsoup4']:
    try:
        __import__(lib if lib != 'beautifulsoup4' else 'bs4')
    except ImportError:
        print(f"Библиотека {lib} не найдена. Устанавливаем...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

# 1. URL сайта и заголовки для имитации браузера
URL = 'https://lenta.ru/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

# Словарь для красивого вывода месяцев на русском языке
MONTHS_RU = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

print(f"Отправка GET-запроса к {URL}...")
response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    print("Страница Lenta.ru успешно загружена! Начинаем парсинг...\n")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Находим карточки новостей
    news_blocks = soup.select('a[class*="card-mini"], div[class*="card-mini"]')
    if not news_blocks:
        news_blocks = soup.select('.parts-page-fraction a')
    
    count = 0
    dt_now = datetime.now()
    
    # Сет для отслеживания уникальных ссылок (чтобы избежать повторов)
    seen_urls = set()
    
    # 5. Обход найденных блоков
    for block in news_blocks:
        if count >= 5:
            break
            
        # --- Извлечение ссылки и фильтрация ---
        if block.name == 'a':
            href = block.get('href', '-')
        else:
            link_inside = block.select_one('a')
            href = link_inside.get('href', '-') if link_inside else '-'
            
        # Если ссылки нет, она пустая или это просто заглушка "#" — пропускаем блок
        if href == '-' or not href or href.strip() == '#':
            continue
            
        # Строим полный URL статьи
        full_url = urljoin(URL, href)
        
        # Если мы эту ссылку уже парсили в этом запуске — пропускаем, чтобы не было дублей
        if full_url in seen_urls:
            continue
            
        # Ищем заголовок новости
        title_element = block.select_one('[class*="title"], [class*="text"]')
        
        # Находим и удаляем элемент времени внутри текстового блока, чтобы он не сливался с заголовком
        if title_element:
            bad_time = title_element.select_one('time, [class*="date"], [class*="time"]')
            if bad_time:
                bad_time.extract() # Удаляет тег времени из title_element
            title = title_element.get_text(strip=True)
        elif block.name == 'a':
            # Если ищем по тегу 'a', тоже удаляем внутреннее время
            bad_time = block.select_one('time, [class*="date"], [class*="time"]')
            if bad_time:
                bad_time.extract()
            title = block.get_text(strip=True)
        else:
            continue

        
        # Ищем дату/время публикации и форматируем
        date_element = block.select_one('time, [class*="date"], [class*="time"]')
        date_formatted = "Дата не указана"
        
        if date_element and date_element.has_attr('datetime'):
            try:
                raw_datetime = date_element['datetime']
                dt = datetime.fromisoformat(raw_datetime.split('+')[0])
                date_formatted = f"{dt.day} {MONTHS_RU[dt.month]} {dt.year}, {dt.strftime('%H:%M')}"
            except Exception:
                time_text = date_element.get_text(strip=True)
                date_formatted = f"{dt_now.day} {MONTHS_RU[dt_now.month]} {dt_now.year}, {time_text}"
        elif date_element:
            time_text = date_element.get_text(strip=True)
            date_formatted = f"{dt_now.day} {MONTHS_RU[dt_now.month]} {dt_now.year}, {time_text}"
        else:
            date_formatted = f"{dt_now.day} {MONTHS_RU[dt_now.month]} {dt_now.year}, {dt_now.strftime('%H:%M')}"

        # Добавляем ссылку в разряд «увиденных»
        seen_urls.add(full_url)
        
        # 6. Вывод в строго заданном формате
        print(f"📰 {title}")
        print(f"⏱ {date_formatted}")
        print(f"🔗 {full_url}")
        print("-" * 50)
        
        count += 1

    if count == 0:
        print("⚠ Не удалось найти уникальные блоки новостей со ссылками.")
else:
    print(f"Ошибка загрузки страницы. Статус-код: {response.status_code}")
