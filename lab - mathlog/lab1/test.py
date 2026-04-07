# Вход: a – упорядоченный по возрастанию список,
# x – число
# Выход: индекс наибольшего элемента i:
# a[i] <= x или -1, если такого индекса нет
def upper_bound(a, x):
    n = len(a)
    l = 0
    r = n - 1
    while l <= r:
        m = (l + r) // 2
        if a[m] <= x:
            l = m + 1
        else:
            r = m - 1
    return r
    

a = [1, 2, 3, 4, 5]
x = 3
print(upper_bound(a, x))