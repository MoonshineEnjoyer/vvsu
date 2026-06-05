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


















import math

# Шаблоны функций аффинных преобразований
def translate(points, tx, ty):
    return [(x + tx, y + ty) for x, y in points]

def rotate(points, angle_deg):
    a = math.radians(angle_deg)
    cos_a, sin_a = math.cos(a), math.sin(a)
    return [(x * cos_a - y * sin_a, x * sin_a + y * cos_a) for x, y in points]

def scale(points, sx, sy):
    return [(x * sx, y * sy) for x, y in points]

# Исходный квадрат
square = [(0, 0), (2, 0), (2, 2), (0, 2)]

# Масштабируем
scaled = scale(square, 1.5, 1.5)

# Поворачиваем
rotated = rotate(scaled, 45)

# Переносим
final_result = translate(rotated, 5, 3)

# Округляем (чтоб наглядно)
def round_pts(pts):
    return [(round(x, 4), round(y, 4)) for x, y in pts]

print("1. Исходный квадрат:", square)
print("2. Масштабирование на 1.5:", round_pts(scaled))
print("3. Поворачиваем на 45 градусов:", round_pts(rotated))
print("4. Конечные точки после переносса с округлением:", round_pts(final_result))

square2 = [(0, 0), (4, 0), (4, 4), (0, 4)]
scaled2 = scale(square2, 1.5, 1.5)
rotated2 = rotate(scaled2, 45)
final_result2 = translate(rotated2, 5, 3)
print("\n1.1 Второй исходный квадрат:", square2)
print("2.2 Масштабирование на 1.5:", round_pts(scaled2))
print("3.3 Поворачиваем на 45 градусов:", round_pts(rotated2))
print("4.4 Конечные точки после переносса с округлением:", round_pts(final_result2))

















import random

def cross2(o, a, b):
    val = (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    # Если val == 0, возвращаем True (1) или False (-1) в зависимости от того, дальше ли точка a
    return val if val != 0 else (1 if (abs(a[0] - o[0]) + abs(a[1] - o[1])) > (abs(b[0] - o[0]) + abs(b[1] - o[1])) else -1)

# Алгоритм Джарвиса
def jarvis_march(points):
    n = len(points)
    if n < 3: return points[:]
    # Самая левая точка
    start = min(range(n), key=lambda i: (points[i][0], points[i][1]))
    hull = []
    p = start
    while True:
        hull.append(points[p])
        q = (p + 1) % n
        if q == p:
            q = (p + 2) % n
        for i in range(n):
            # Если i "левее" - обновляем q
            if cross2(points[p], points[i], points[q]) > 0:
                q = i
        p = q
        if p == start:
            break
    return hull

pts_1 = [(0, 0), (6, 0), (3, 6), (2, 1), (3, 1), (4, 1), (2, 2), (3, 2), (4, 2), (3, 3)]
print("--- Треугольник без коллинеарности на краях ---")
print("Вход (10 точек):", pts_1)
print("Вывод оболочки:", jarvis_march(pts_1))

pts_2 = [(0, 2), (2, 4), (4, 2), (2, 0), (1, 1), (2, 2), (3, 3), (1, 3), (2, 3), (2, 1)]
print("--- Вытянутый ромб ---")
print("Вход (10 точек):", pts_2)
print("Вывод оболочки:", jarvis_march(pts_2))









import math
import matplotlib.pyplot as plt

def cross2(o, a, b):
    val = (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    # Если val == 0, возвращаем True (1) или False (-1) в зависимости от того, дальше ли точка a
    return val if val != 0 else (1 if (abs(a[0] - o[0]) + abs(a[1] - o[1])) > (abs(b[0] - o[0]) + abs(b[1] - o[1])) else -1)

# Грэхем
def graham_scan(points):
    if len(points) < 3: return points[:]
    # Нижняя (затем левая) точка
    start = min(points, key=lambda p: (p[1], p[0]))
    def angle_key(p):
        if p == start:
            return (-math.inf, 0) # Гарантируем, что start будет самым первым
        return (math.atan2(p[1] - start[1], p[0] - start[0]), 
                (p[0] - start[0])**2 + (p[1] - start[1])**2)              
    sorted_pts = sorted(points, key=angle_key)
    stack = []
    for p in sorted_pts:
        while len(stack) >= 2 and cross2(stack[-2], stack[-1], p) <= 0:
            stack.pop() # Убираем правый поворот и коллинеарные внутренние точки
        stack.append(p)
    return stack

def jarvis_march(points):
    n = len(points)
    if n < 3: return points[:]
    # Самая левая точка
    start = min(range(n), key=lambda i: (points[i][0], points[i][1]))
    hull = []
    p = start
    while True:
        hull.append(points[p])
        q = (p + 1) % n
        if q == p:
            q = (p + 2) % n
        for i in range(n):
            # Если i "левее" - обновляем q
            if cross2(points[p], points[i], points[q]) > 0:
                q = i
        p = q
        if p == start:
            break
    return hull

# набор из 10 точек для сравнения
pts = [(0, 0), (2, 0), (4, 0), (4, 2), (4, 4), (2, 4), (0, 4), (0, 2), (1, 1), (2, 2)]

# Расчет оболочек обеими функциями
hull_jarvis = jarvis_march(pts)
hull_graham = graham_scan(pts)

print("Оболочка Джарвиса:", hull_jarvis)
print("Оболочка Грэхема :", hull_graham)

# --- Визуализация через matplotlib ---
plt.figure(figsize=(6, 6))

# Отрисовка всех исходных точек
xs, ys = zip(*pts)
plt.scatter(xs, ys, color='blue', label='Исходные точки', zorder=3)

# Замыкаем контур оболочки для отрисовки линии
hull_plot = hull_graham + [hull_graham[0]]
hx, hy = zip(*hull_plot)
plt.plot(hx, hy, color='red', linestyle='-', linewidth=2, label='Выпуклая оболочка', zorder=2)

# Выделение вершин оболочки маркером
plt.scatter(hx, hy, color='red', marker='o', s=80, facecolors='none', edgecolors='red', label='Вершины оболочки', zorder=4)

plt.title("Визуализация выпуклой оболочки (Алгоритм Грэхема)")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.show()
