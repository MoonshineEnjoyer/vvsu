def create_adj_matrix(n, edges):
    matrix = [[0] * n for _ in range(n)]
    for i, j in edges:
        matrix[i][j] = 1
    return matrix
edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 5)]
m = create_adj_matrix(6, edges)
print('Матрица смежности')
for row in m:
    print(row)

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}
print(graph)
def degree(graph, vertex):
    return len(graph.get(vertex, []))
print('степень вершины для B')
print(degree(graph, 'B'))
print('степень вершины для D')
print(degree(graph, 'D'))
sum_of_degrees = sum(degree(graph, v) for v in graph)
twice_edges = 2 * len(edges)
print(f'Сумма степеней вершин: {sum_of_degrees}')
print(f'Удвоенное число рёбер: {twice_edges}')
print(f'Проверка теоремы Эйлера (сумма степеней = 2 * число рёбер): {sum_of_degrees == twice_edges}')















from collections import deque
graph = {
    'a': ['b', 'c'],
    'b': ['a', 'd', 'e'],
    'c': ['a', 'f'],
    'd': ['b'],
    'e': ['b', 'f'],
    'f': ['c', 'e']
}
def bfs(graph, start): # порядок обхода
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

def bfs_distances(graph, start): # расчёт расстояния от стартовой точки
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

def bfs_shortest_path(graph, start, end): # для вывода точного маршрута
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

print("Порядок обхода от 'a':", bfs(graph, 'a'))
print("Расстояния от 'a':", bfs_distances(graph, 'a'))
path_A_F = bfs_shortest_path(graph, 'a', 'f')
path_D_F = bfs_shortest_path(graph, 'd', 'f')
print(f"Кратчайший путь из A в F: {path_A_F}")
print(f"Кратчайший путь из D в F: {path_D_F}")
