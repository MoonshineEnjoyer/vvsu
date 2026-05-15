# 1 Задание, линейный поиск
arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
print("Линейный поиск, результат")
print(linear_search(arr, 23))
print(linear_search(arr, 50))
# 1 Задание, бинарный поиск (итеративный)
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
print("Бинарный поиск, результат")
print(binary_search(arr, 23))
print(binary_search(arr, 50))

# 2 pflfybt
class HashTable:
    def __init__(self, size=11):
        self.size = size
        self.table = [[] for _ in range(size)]
    def _hash(self, key):
        return hash(key) % self.size
    def insert(self, key, value):
        idx = self._hash(key)
        for pair in self.table[idx]:
            if pair[0] == key:
                pair[1] = value; return
        self.table[idx].append([key, value])
    def search(self, key):
        idx = self._hash(key)
        for pair in self.table[idx]:
            if pair[0] == key: return pair[1]
        return None
    def delete(self, key):
        idx = self._hash(key)
        for i, pair in enumerate(self.table[idx]):
            if pair[0] == key:
                del self.table[idx][i]
                return True
        return False
    def display(self):
        for i, bucket in enumerate(self.table):
            print(f"{i}: {bucket}")
htable = HashTable()
example = {"Малых": 5, "Свиридов": 5, "Михайленко": 5, "Прокопенко": 5, "Дмитров": 5}
for name, grade in example.items():
    htable.insert(name, grade)
htable.display()
print("Поиск оценки Свиридов:", htable.search("Свиридов"))
print("Поиск оценки Белов:", htable.search("Белов"))
print("Удаление записи Михайленко:", htable.delete("Михайленко")) # tyt proeb
htable.display()




class HashTable:
    def __init__(self, size=11):
        self.size = size
        self.table = [[] for _ in range(size)]
    def _hash(self, key):
        return hash(key) % self.size
    def insert(self, key, value):
        idx = self._hash(key)
        for pair in self.table[idx]:
            if pair[0] == key:
                pair[1] = value; return # обновление
        self.table[idx].append([key, value]) # добавление
    def search(self, key):
        idx = self._hash(key)
        for pair in self.table[idx]:
            if pair[0] == key: return pair[1]
        return None
    def delete(self, key):
        idx = self._hash(key)
        for i, pair in enumerate(self.table[idx]):
            if pair[0] == key:
                del self.table[idx][i]
                return True
        return False
    def display(self):
        for i, bucket in enumerate(self.table):
            print(f"{i}: {bucket}")
table = HashTable()
table.insert(0, "Малых: 5")
table.insert(1, "Михайленко: 4")
table.insert(6, "Гончаренко: 3")
table.insert(3, "Свиридов: 5")
table.insert(4, "Смирнов: 4")
table.display()

print("\nПоиск существующей записи")
print(table.search(3))
print("Поиск несуществующей записи")
print(table.search(48))

table.delete(1)
table.display()








# Определение вершин и ребер
vertices = ['a', 'b', 'c', 'd', 'e', 'f']
edges = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('b', 'e'), ('c', 'f'), ('e', 'f')]

# Создание маппинга «имя: индекс»
v_to_idx = {vertex: i for i, vertex in enumerate(vertices)}

# Инициализация пустой матрицы 6х6
matrix = [[0] * 6 for _ in range(6)]

# Заполнение матрицы для неориентированного графа
for u, v in edges:
    i, j = v_to_idx[u], v_to_idx[v]
    matrix[i][j] = 1
    matrix[j][i] = 1

# Красивый вывод
for row in matrix:
    print(row)
