import sys
import array
import ctypes
import time
sys.setrecursionlimit(200000)

# 1 задание; пункт 1
num = 10
text = "Привет"
my_list = [1, 2, 3]
print("Число:", num, type(num), id(num), sys.getsizeof(num))
print("Строка:", text, type(text), id(text), sys.getsizeof(text))
print("Список:", my_list, type(my_list), id(my_list), sys.getsizeof(my_list))

# 1 задание; пункт 2
a = [10, 20]
b = a
print("a и b - это один объект", a is b)

# 1 задание, неизменяемое число; пункт 3
x = 5
y = x
x = 10
print("результат после x = 10: x =", x, "y =", y)  

# 1 задание, изменяемый список; пункт 3
list1 = [1]
list2 = list1
list1.append(2)
print("результат после append: list1 =", list1, "list2 =", list2)

# 2 задание, подсчёт памяти; пункт 1
def memory(obj, seen=None):
    if seen is None:
        seen = set()
    if id(obj) in seen:
        return 0
    seen.add(id(obj))
    size = sys.getsizeof(obj)
    if isinstance(obj, (list, tuple, dict, set)):
        items = obj.values() if isinstance(obj, dict) else obj
        for item in items:
            size += memory(item, seen)
    return size
test = [1, [2, 3], "пайтон"]
print("размер объекта:", memory(test), "байт")

# 2 задание, создание арреем массива из 10 чисел и вычисление теоретического адреса для каждого элемента со сравнением с реальным; пункт 2
nums = array.array('i', range(10))
base, length = nums.buffer_info()
item_size = nums.itemsize
print("Базовый адрес массива:", base)
for i in range(len(nums)):
    theor = base + i * item_size
    real = ctypes.addressof(ctypes.c_int.from_buffer(nums, i * item_size))
    print("число: ", i, ". Теоретический адрес = ", theor, ". Реальный адрес = ", real, sep="")

# 3 задание, брутфорс
def find_max_brute_force(arr):
    n = len(arr)
    for i in range(n):
        is_max = True
        for j in range(n):
            if arr[j] > arr[i]:
                is_max = False
                break
        if is_max:
            return arr[i]
test3_1 = [10, 5, 2, 7, 1354, 3]
test3_1_max = find_max_brute_force(test3_1)
print(test3_1_max)

# 3 задание, Greedy
def find_max_greedy(arr):
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val
test3_2 = [102, 75, 24, 7, 134, 31]
test3_2_max = find_max_brute_force(test3_2)
print(test3_2_max)

# 3 задание, Divide & Conquer
def find_max_divide_conquer(arr, low, high):
    if low == high:
        return arr[low]
    mid = (low + high) // 2
    left_max = find_max_divide_conquer(arr, low, mid)
    right_max = find_max_divide_conquer(arr, mid + 1, high)
    return left_max if left_max > right_max else right_max
test3_3 = [140, 54, 22, 77, 154, 311]
test3_3_max = find_max_brute_force(test3_3)
print(test3_3_max)

# 3 задание, DP
def find_max_dp(arr):
    n = len(arr)
    dp = [0] * n
    dp[0] = arr[0]
    for i in range(1, n):
        dp[i] = max(dp[i-1], arr[i])
    return dp[n-1]
test3_4 = [140, 542, 222, 771, 1314, 3141]
test3_4_max = find_max_brute_force(test3_4)
print(test3_4_max)

# 3 задание, проверка
n = 100000
arr = [i for i in range(n)]

# Greedy
start = time.perf_counter()
find_max_greedy(arr)
print("Greedy", ". Сложность: O(n)", ". Время: ", time.perf_counter() - start, " сек", sep="")

# Divide & Conquer
start = time.perf_counter()
find_max_divide_conquer(arr, 0, n - 1)
print("Divide & Conquer", ". Сложность: O(n)", ". Время: ", time.perf_counter() - start, " сек", sep="")

# DP
start = time.perf_counter()
find_max_dp(arr)
print("DP", ". Сложность: O(n)", ". Время: ", time.perf_counter() - start, " сек", sep="")

# Brute Force
start = time.perf_counter()
find_max_brute_force(arr)
print("Brute Force", ". Сложность: O(n^2)", ". Время: ", time.perf_counter() - start, " сек", sep="")