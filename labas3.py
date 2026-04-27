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
