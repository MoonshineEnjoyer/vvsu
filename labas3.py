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
