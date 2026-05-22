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








from collections import deque

# Исходный граф из задания 1
graph = {
    'a': ['b', 'c'],
    'b': ['a', 'd', 'e'],
    'c': ['a', 'f'],
    'd': ['b'],
    'e': ['b', 'f'],
    'f': ['c', 'e']
}

# 1. Порядок обхода BFS
def bfs(graph, start):
    visited = []
    queue = deque([start])
    visited_set = {start}
    
    while queue:
        vertex = queue.popleft()
        visited.append(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                queue.append(neighbor)
    return visited

# 2. Словарь расстояний от start до всех вершин
def bfs_distances(graph, start):
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0
    queue = deque([start])
    
    while queue:
        vertex = queue.popleft()
        for neighbor in graph.get(vertex, []):
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[vertex] + 1
                queue.append(neighbor)
    return distances

# 3. Поиск кратчайшего пути
def bfs_shortest_path(graph, start, end):
    if start == end:
        return [start]
    queue = deque([[start]])
    visited = {start}
    
    while queue:
        path = queue.popleft()
        vertex = path[-1]
        
        if vertex == end:
            return path
            
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None

# --- Тестирование и поиск путей ---
print("Порядок обхода от 'a':", bfs(graph, 'a'))
print("Расстояния от 'a':", bfs_distances(graph, 'a'))

path_A_F = bfs_shortest_path(graph, 'a', 'f')
path_D_F = bfs_shortest_path(graph, 'd', 'f')

print(f"Кратчайший путь из A в F: {path_A_F}")
print(f"Кратчайший путь из D в F: {path_D_F}")







import heapq

# 2. Представление графа в виде списка смежности с весами
# Структура: {вершина_источник: [(сосед, вес), ...]}
graph = {
    0: [(1, 4), (2, 2)],
    1: [(2, 1), (3, 5)],
    2: [(1, 1), (3, 8), (4, 10)],
    3: [(4, 2)],
    4: []
}

def dijkstra(graph, start, target):
    # Инициализация расстояний бесконечностью, для стартовой вершины — 0
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    
    # Словарь для восстановления пути: {дочерняя_вершина: родительская_вершина}
    predecessors = {vertex: None for vertex in graph}
    
    # Очередь с приоритетами (минимальная куча), хранит пары (расстояние, вершина)
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # Если нашли расстояние больше, чем уже записано, пропускаем
        if current_distance > distances[current_vertex]:
            continue
            
        # Обход всех соседей текущей вершины
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight
            
            # Если найден более короткий путь к соседу
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
                
    # 4. Восстановление кратчайшего пути от start до target
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    
    # Если путь не существует (расстояние осталось бесконечным)
    if distances[target] == float('infinity'):
        return distances, []
        
    return distances, path

# Запуск алгоритма
start_vertex = 0
target_vertex = 4
distances, shortest_path = dijkstra(graph, start_vertex, target_vertex)

# Вывод результатов
print("3. Кратчайшие расстояния от вершины 0:")
for vertex, dist in distances.items():
    print(f"До вершины {vertex}: {dist}")

print(f"\n4. Кратчайший путь от {start_vertex} до {target_vertex}:")
print(" -> ".join(map(str, shortest_path)))








import heapq

# 2. Представление графа как список смежности с весами (Лекция, стр. 22)
weighted_graph = {
    0: [(1, 4), (2, 2)],
    1: [(2, 1), (3, 5)],
    2: [(1, 1), (3, 8), (4, 10)],
    3: [(4, 2)],
    4: []
}

def dijkstra(graph, start):
    # Инициализация расстояний бесконечностью (Лекция, стр. 22 использует INF)
    INF = float('inf')
    distances = {vertex: INF for vertex in graph}
    distances[start] = 0
    
    # Структура для восстановления пути
    parent = {vertex: None for vertex in graph}
    
    # Приоритетная очередь на базе min-heap (Принцип из Лекции, стр. 20, 23)
    # Хранит кортежи: (текущее_расстояние, вершина)
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # Если нашли путь длиннее, чем уже сохранен — пропускаем
        if current_distance > distances[current_vertex]:
            continue
            
        # Обход соседей вершины (Лекция, стр. 22)
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight
            
            # Релаксация ребра
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parent[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
                
    return distances, parent

def get_path(parent, start, end):
    # 4. Функция восстановления кратчайшего пути
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path if path[0] == start else []

# Запуск алгоритма от вершины 0
start_vertex = 0
end_vertex = 4
distances, parent = dijkstra(weighted_graph, start_vertex)
shortest_path = get_path(parent, start_vertex, end_vertex)

# Вывод результатов в консоль
print("3. Кратчайшие расстояния от вершины 0:")
for vertex, dist in distances.items():
    print(f"   До вершины {vertex}: {dist}")

print(f"\n4. Восстановленный кратчайший путь от {start_vertex} до {end_vertex}:")
print(f"   Путь: {shortest_path}")
print(f"   Суммарный вес (длина пути): {distances[end_vertex]}")









# 2. Представление графа как список смежности с весами (из условий Задания 1)
graph = {
    0: [(1, 4), (2, 2)],
    1: [(2, 1), (3, 5)],
    2: [(1, 1), (3, 8), (4, 10)],
    3: [(4, 2)],
    4: []
}

# 3. Реализация алгоритма Дейкстры через итеративный обход соседей
def dijkstra_traversal(graph, start, end):
    # Инициализация структуры посещенных вершин, как в DFS/BFS на лекции
    visited = set()
    
    # Инициализация массива/словаря расстояний значениями бесконечности
    INF = float('inf')
    distances = {vertex: INF for vertex in graph}
    distances[start] = 0
    
    # Словарь предков для восстановления пути (Шаг 4)
    predecessors = {vertex: None for vertex in graph}
    
    # Обходим граф, пока не посетим все доступные вершины
    while len(visited) < len(graph):
        # Находим среди НЕПОСЕЩЕННЫХ вершину с минимальным текущим расстоянием
        current_vertex = None
        min_dist = INF
        
        for vertex in graph:
            if vertex not in visited and distances[vertex] < min_dist:
                min_dist = distances[vertex]
                current_vertex = vertex
                
        # Если не осталось доступных вершин, завершаем обход
        if current_vertex == -1 or current_vertex is None:
            break
            
        # Фиксируем вершину (добавляем в visited, как в коде BFS/DFS с презентации)
        visited.add(current_vertex)
        
        # Обход соседей текущей вершины (как во всех алгоритмах обхода лекции)
        for neighbor, weight in graph[current_vertex]:
            if neighbor not in visited:
                new_distance = distances[current_vertex] + weight
                
                # Релаксация: если нашли путь короче, обновляем данные
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_vertex
                    
    # 4. Восстановление кратчайшего пути от start до end
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = predecessors[curr]
    path.reverse()
    
    return distances, path

# Запуск скрипта для проверки
start_vertex = 0
end_vertex = 4
distances, shortest_path = dijkstra_traversal(graph, start_vertex, end_vertex)

# Вывод результатов в консоль
print("3. Кратчайшие расстояния от вершины 0:")
for vertex, dist in distances.items():
    print(f"До вершины {vertex}: {dist}")

print(f"\n4. Кратчайший путь от {start_vertex} до {end_vertex}:")
print(" -> ".join(map(str, shortest_path)))














from collections import deque, defaultdict

# Данные проекта из таблицы Задания 2: ребра (откуда, куда, длительность)
edges = [
    (0, 1, 3),
    (0, 2, 2),
    (1, 3, 4),
    (2, 3, 5),
    (1, 4, 6),
    (3, 4, 2),
    (3, 5, 3),
    (4, 5, 1)
]
n = 6  # Проект из 6 узлов (от 0 до 5)

# 1. Реализация топологической сортировки (левая часть слайда 35)
def topological_sort(graph, n):
    in_degree = [0] * n
    for u in range(n):
        for v, w in graph[u]:
            in_degree[v] += 1
            
    # Используем очередь deque, как в лекции
    queue = deque([v for v in range(n) if in_degree[v] == 0])
    order = []
    
    while queue:
        v = queue.popleft()
        order.append(v)
        for neighbor, w in graph[v]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order

# 2-3. Реализация нахождения критического пути (правая часть слайда 35)
def critical_path(n, edges):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        
    # Шаг 1: Топологическая сортировка
    order = topological_sort(graph, n)
    
    # Шаг 2: Прямой проход (вычисление раннего времени раннего начала)
    early = [0] * n
    for u in order:
        for v, w in graph[u]:
            early[v] = max(early[v], early[u] + w)
            
    # Шаг 3: Обратный проход (вычисление позднего времени)
    late = [early[order[-1]]] * n
    for u in reversed(order):
        for v, w in graph[u]:
            late[u] = min(late[u], late[v] - w)
            
    # Шаг 4: Определение критических узлов (где раннее время равно позднейшему)
    # Исправляем опечатку из слайда, чтобы функция возвращала сами номера узлов
    crit_nodes = [i for i in range(n) if early[i] == late[i]]
    
    return early[order[-1]], crit_nodes, order

# Запуск алгоритма
t_cr, nodes, top_order = critical_path(n, edges)

# Вывод ответов по пунктам задания
print(f"1. Результат топологической сортировки: {top_order}")
print(f"3. Критическое время (Ткр) = {t_cr}")
print(f"3. Критические узлы: {nodes}")









from collections import deque, defaultdict

# Данные проекта из таблицы Задания 2: ребра (откуда, куда, длительность)
edges = [
    (0, 1, 3),
    (0, 2, 2),
    (1, 3, 4),
    (2, 3, 5),
    (1, 4, 6),
    (3, 4, 2),
    (3, 5, 3),
    (4, 5, 1)
]
n = 6  # Проект из 6 узлов (от 0 до 5)

# 1. Топологическая сортировка (по лекции)
def topological_sort(graph, n):
    in_degree = [0] * n
    for u in range(n):
        for v, w in graph[u]:
            in_degree[v] += 1
            
    queue = deque([v for v in range(n) if in_degree[v] == 0])
    order = []
    
    while queue:
        v = queue.popleft()
        order.append(v)
        for neighbor, w in graph[v]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order

# 2. Основная функция расчёта параметров CPM
def critical_path_analysis(n, edges):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        
    order = topological_sort(graph, n)
    
    # Прямой проход: расчет ранних сроков (как в лекции)
    early = [0] * n
    for u in order:
        for v, w in graph[u]:
            early[v] = max(early[v], early[u] + w)
            
    # Обратный проход: исправленный расчет поздних сроков для ветвлений
    late = [early[order[-1]]] * n
    for u in reversed(order):
        for v, w in graph[u]:
            if late[v] - w < late[u]:
                late[u] = late[v] - w
                
    # Определение всех критических узлов
    crit_nodes = [i for i in range(n) if early[i] == late[i]]
    
    # 3. Функция восстановления критических путей (обход в глубину от истока к стоку)
    critical_paths = []
    
    def find_paths(current_node, current_path):
        if current_node == n - 1:  # Дошли до конечного узла (5)
            critical_paths.append(list(current_path))
            return
        for neighbor, weight in graph[current_node]:
            # Ребро лежит на критическом пути, если узел-сосед критический
            # и раннее время начала совпадает с шагом выполнения работы
            if neighbor in crit_nodes and early[current_node] + weight == early[neighbor]:
                current_path.append(neighbor)
                find_paths(neighbor, current_path)
                current_path.pop()

    # Запускаем поиск путей из начальной вершины 0
    if 0 in crit_nodes:
        find_paths(0, [0])
        
    return early[order[-1]], crit_nodes, top_order, critical_paths

# Запуск алгоритма
t_cr, nodes, top_order, all_paths = critical_path_analysis(n, edges)

# Вывод результатов работы программы
print(f"1. Топологический порядок вершин: {top_order}")
print(f"2. Критическое время выполнения проекта (Ткр): {t_cr}")
print(f"3. Все критические узлы: {nodes}")
print("\n4. Вычисленные критические пути проекта:")
for idx, path in enumerate(all_paths, 1):
    print(f"   Путь {idx}: " + " -> ".join(map(str, path)))
