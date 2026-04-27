class Student:
    def __init__(self, course, napravlenie, group, score, tetradi, dengi):
        # 2. Приватные поля (начинаются с __)
        self.__course = course
        self.__napravlenie = napravlenie
        self.__group = group
        self.__score = score
        self.__tetradi = tetradi
        self.__dengi = dengi

    # 3. Геттеры и сеттеры для приватных полей
    def get_score(self):
        return self.__score

    def set_score(self, value):
        if 0 <= value <= 100:
            self.__score = value
        else:
            print("Ошибка: балл должен быть от 0 до 100")

    def get_obshiy_info(self):
        return (self.__course, self.__napravlenie, self.__group)

    def dengi_plus(self, stipendia):
        self.__dengi += stipendia
        return self.__dengi


# Новый, наследующийся класс
class GraduateStudent(Student):
    # Специфичные поля и методы
    def __init__(self, course, napravlenie, group, score, tetradi, dengi, thesis_topic):
        super().__init__(course, napravlenie, group, score, tetradi, dengi)
        self.thesis_topic = thesis_topic  # Тема работы

    def defend_thesis(self):
        return f"Студент защитил работу на тему: {self.thesis_topic}"


# Демонстрация
# Объект основного класса
student1 = Student("2", "IT", "БИС-22", 80, 5, 500)
print(f"Инфо студента: {student1.get_obshiy_info()}")
student1.set_score(95)  # Используем сеттер
print(f"Обновленный балл: {student1.get_score()}")

# Объект дочернего класса
grad_student = GraduateStudent(
    "4", "IT", "МАГ-1", 100, 10, 25000, "Искусственный интеллект"
)
print(f"Магистр: {grad_student.get_obshiy_info()}")
print(grad_student.defend_thesis())  # Метод дочернего класса
