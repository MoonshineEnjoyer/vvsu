import time

# 1-2. ПАРСИНГ СТРОКИ ЛОГОВ В СЛОВАРИ
def parse_logs_to_dicts(raw_logs_str, delimiter=';'):
    parsed_logs = []
    messages = raw_logs_str.split(delimiter)

    for msg in messages:
        msg = msg.strip() # Избавляемся от лишних пробелов при разделении строки
        if not msg:
            continue # Если строка пустая (в самом конце лог-файла, например), цикл переходит к следующему логу, не выполняя для этой строки никакой код ниже

        parts = msg.split() # Делим полученную разделенную строку на части
        if len(parts) < 6: # Проверяем, есть ли в логе минимум дата, время, уровень, пользователь, действие, статус
            continue

        # Извлекаем значения, убирая префиксы "user=", "action=", "status="
        user_name = parts[3].replace("user=", "")
        action_name = parts[4].replace("action=", "")
        status_name = parts[5].replace("status=", "")

        log_dict = {
            'timestamp': parts[0] + " " + parts[1],
            'level': parts[2],
            'user': user_name,
            'action': action_name,
            'status': status_name
        }
        parsed_logs.append(log_dict)

    return parsed_logs


# 3. ФУНКЦИИ ОБРАБОТКИ
def filter_by_user(logs, user_substring): # Фильтрация по списку словарей (поиск в user, без учёта регистра)
    result = []
    sub = user_substring.lower() # Избавляемся от надобности следования регистру
    for log in logs:
        if sub in log['user'].lower():
            result.append(log)
    return result


def stats_by_status(logs): # Словарь статус -> количество
    counts = {}
    for log in logs: # Обходим логи
        status = log['status']
        counts[status] = counts.get(status, 0) + 1 # Прибавляем, если нашли такой же статус
    return counts


def most_problem_users(logs): # Список пользователей с максимальной долей сообщений, где статус != ok
    total_counts = {}
    error_counts = {}

    for log in logs:
        user = log['user']
        total_counts[user] = total_counts.get(user, 0) + 1 # Увеличиваем счётчик запросов для этого юзера на 1. 0, если юзер новый
        if log['status'] != 'ok':
            error_counts[user] = error_counts.get(user, 0) + 1 # Увеличиваем таким же образом счётчик ошибок на 1.

    max_rate = 0.0 # Переменная для хранения максимальной доли ошибок
    user_rates = {}
    for user, total in total_counts.items(): # Перебираем всех найденных юзеров и их общее кол-во запросов из словаря total_counts
        rate = error_counts.get(user, 0) / total # Ищем долю: кол-во ошибок на их кол-во
        user_rates[user] = rate
        if rate > max_rate:
            max_rate = rate

    if max_rate == 0.0:
        return []

    problem_users = []
    for user, rate in user_rates.items():
        if rate == max_rate: # Если у нас несколько юзеров с одинаковой долей
            problem_users.append(user)
    return problem_users


def filter_by_user_raw(raw_logs_str, user_substring, delimiter=';'): # «сырое» фильтрование по пользователю по всей строке лога, без предварительного разбиения.
    result = [] # Создает пустой список, куда мы будем сохранять найденные строки логов.
    messages = raw_logs_str.split(delimiter) # Разрезаем одну огромную строку по ";"
    sub = user_substring.lower() # Исключаем регистр

    for msg in messages:
        if sub in msg.lower():
            result.append(msg.strip()) # Подстрока найдена - разрезаем от лишних пробелов стрипом и добавляем в список

    return result

# АВТОМАТИЧЕСКАЯ ГЕНЕРАЦИЯ НАБОРОВ А, B, C (минимум 1000 сообщений)
logs_A, logs_B, logs_C = [], [], []

for i in range(1000):
    # Набор A: 5 пользователей, User_1 частый (70%), статус 'ok' в 90% случаев; User_2 - User-5 - 30% случаев
    user_A = "User_1" if i % 10 < 7 else f"User_{2 + i % 4}"
    status_A = "ok" if i % 10 != 0 else "error_500"
    logs_A.append(f"2026-03-21 10:00:00 INFO user={user_A} action=click status={status_A}")

    # Набор B: статусы распределены равномерно между 4 значениями, по 250 сообещний.
    user_B = f"User_{i % 8}"
    statuses_B = ["ok", "error_404", "timeout", "access_denied"]
    status_B = statuses_B[i % 4]
    logs_B.append(f"2026-03-21 10:00:00 INFO user={user_B} action=view status={status_B}")

    # Набор C: User_99 делает 50% запросов, статусы смешаны случайно (33/66)
    user_C = "User_99" if i % 2 == 0 else f"User_{i % 5}"
    status_C = "ok" if i % 3 == 0 else "error_404"
    logs_C.append(f"2026-03-21 10:00:00 INFO user={user_C} action=login status={status_C}")

raw_A = ";".join(logs_A)
raw_B = ";".join(logs_B)
raw_C = ";".join(logs_C)


# ПРОВЕДЕНИЕ ЗАМЕРОВ И ВЫВОД ТАБЛИЦЫ
print(f"{'Набор':<6} | {'Операция':<35} | {'Время (сек)':<15}")
print("-" * 65)

for name, raw_data, freq_user, rare_user in [('A', raw_A, 'User_1', 'User_2'),
                                             ('B', raw_B, 'User_0', 'User_7'),
                                             ('C', raw_C, 'User_99', 'User_1')]: # Цикл, выполнится ровно 3 раза
    # Время парсинга
    t0 = time.perf_counter() # Засекаем время с точностью до микросекунд
    parsed = parse_logs_to_dicts(raw_data) # Запускаем функцию среза одной огромной строки логов
    t_parse = time.perf_counter() - t0 # Останавливаем время, высчитываем
    print(f"Набор {name} | Структурирование (парсинг) {'':<10} | {t_parse:.6f}")

    # Сравнение фильтрации частого пользователя
    t0 = time.perf_counter()
    filter_by_user(parsed, freq_user) # Обычная, после предварительной очистки
    t_filt = time.perf_counter() - t0

    t0 = time.perf_counter()
    filter_by_user_raw(raw_data, freq_user) # Сырая
    t_raw = time.perf_counter() - t0
    print(f"Набор {name} | filter_by_user ({freq_user:<7} - частый)  | {t_filt:.6f}")
    print(f"Набор {name} | filter_by_user_raw ({freq_user:<7} - частый)  | {t_raw:.6f}")

    # Сравнение фильтрации редкого пользователя
    t0 = time.perf_counter()
    filter_by_user(parsed, rare_user)
    t_filt_rare = time.perf_counter() - t0

    t0 = time.perf_counter()
    filter_by_user_raw(raw_data, rare_user)
    t_raw_rare = time.perf_counter() - t0
    print(f"Набор {name} | filter_by_user ({rare_user:<7} - редкий)   | {t_filt_rare:.6f}")
    print(f"Набор {name} | filter_by_user_raw ({rare_user:<7} - редкий)   | {t_raw_rare:.6f}")
    print("-" * 65)


"""
1. Оценка асимптотической сложности (N — число логов, L — длина одного лога):
   - Разбор строки в список словарей: O(N * L). Делаем один проход по всем
     сообщениям N, внутри каждого вызываем методы строк (.split), которые
     зависят от длины самого лога L.
   - filter_by_user: O(N). Проходим ровно один раз по уже готовому списку из N
     элементов и проверяем конкретное поле словаря.
   - filter_by_user_raw: O(N * L). Один проход по N сообщениям, но внутри
     каждого выполняется полнотекстовый поиск подстроки по всей длине строки L.
   - stats_by_status и most_problem_users: O(N). Один проход циклом по списку
     из N словарей.

2. Сопоставление конкретных результатов (наборы А/B/C) с теорией:
   - Субъективное восприятие скорости: При поиске частого пользователя (например,
     User_1 в наборе А, который занимает 70% всех логов) фильтрация субъективно
     кажется медленнее, хотя теоретическая сложность одинакова — O(N). Алгоритм в
     обоих случаях делает одинаковое число проверок. Разница в ощущениях возникает
     из-за того, что Python тратит дополнительное время на выделение памяти,
     копирование и вывод огромного результирующего списка элементов на экран.
   - Когда окупается структура: Подготовка структуры «список словарей» требует
     затрат памяти и времени (t_parse). При количестве запросов n = 1 выгоднее
     использовать прямой поиск по сырой строке (filter_by_user_raw). Однако при
     многократных запросах (n >= 2), структура полностью окупается, так как
     тяжелый парсинг выполняется всего один раз, а последующие точечные выборки
     по ключам словаря работают в разы быстрее, чем постоянная нарезка сырого текста.

3. Фрагмент лога для анализа и демонстрации:
   -----------------------------------------------------------------------------
   2026-03-21 10:00:00 INFO user=User_1 action=click status=ok;
   2026-03-21 10:00:00 INFO user=User_2 action=click status=error_500;
   2026-03-21 10:00:00 INFO user=User_1 action=click status=ok
   -----------------------------------------------------------------------------
   Анализ фрагмента:
   При вызове filter_by_user_raw("User_2") алгоритм вынужден сканировать абсолютно
   весь текст строк, включая даты, уровни логов (INFO) и действия (click).
   При вызове filter_by_user("User_2") алгоритм работает изолированно, обращаясь
   напрямую к ключу словаря ['user'], что исключает чтение лишнего текстового шума.
"""









































"""
1. Преимущества списка словарей перед сырой строкой:
   - Точность: Исключает ошибки, когда имя пользователя случайно совпадает
     со статусом или действием (поиск идет строго по ключу ['user']).
   - Удобство: К данным легко обращаться по именам полей (log['status']),
     вместо постоянной ручной нарезки текста через .split().

2. Выбор структуры для индексации и почему:
   - Выбор: Словарь.
   - Почему: Обеспечивает максимальную скорость поиска по ключу за константное
     время O(1). Это позволяет мгновенно достать логи конкретного пользователя
     или статуса без полного перебора всего списка.
"""
