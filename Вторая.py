import time
import random

# =====================================================================
# БЛОК 1: РЕАЛИЗАЦИЯ (Три версии проверки пароля)
# =====================================================================

# Дополнительные списки для правил 4 и 5
BANNED_SUBSTRINGS = ["password", "qwerty", "1234"]

# --- 1. НАИВНАЯ ВЕРСИЯ ---
# Для каждого правила выполняется отдельный проход по строке
def check_password_naive(password, username):
    # Правило 1: Длина (хотя бы 8 символов, возьмем стандарт для примера)
    if len(password) < 8:
        return False

    # Правило 2: Заглавная буква
    has_upper = False
    for char in password:
        if char.isupper():
            has_upper = True
    if not has_upper:
        return False

    # Правило 3: Строчная буква
    has_lower = False
    for char in password:
        if char.islower():
            has_lower = True
    if not has_lower:
        return False

    # Правило 4: Цифра
    has_digit = False
    for char in password:
        if char.isdigit():
            has_digit = True
    if not has_digit:
        return False

    # Правило 5: Отсутствие пробелов
    has_space = False
    for char in password:
        if char == " ":
            has_space = True
    if has_space:
        return False

    # Правило 6: Запрещенные подстроки
    for banned in BANNED_SUBSTRINGS:
        if banned in password.lower():
            return False

    # Правило 7: Запрет на включение имени пользователя
    if username.lower() in password.lower():
        return False

    return True


# --- 2. ОПТИМИЗИРОВАННАЯ ВЕРСИЯ ---
# Один проход по строке, все базовые условия проверяются параллельно
def check_password_optimized(password, username):
    if len(password) < 8:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_space = False

    # Один единственный цикл по всей строке пароля
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char == " ":
            has_space = True

    # Проверяем накопленные флаги
    if not has_upper or not has_lower or not has_digit or has_space:
        return False

    # Внешние проверки подстрок (вынужденные отдельные проходы)
    for banned in BANNED_SUBSTRINGS:
        if banned in password.lower():
            return False

    if username.lower() in password.lower():
        return False

    return True


# --- 3. КОНФИГУРИРУЕМАЯ ВЕРСИЯ ---
# Правила описываются функциями. Проверка применяет их динамически.

# Вспомогательные функции для конфигурации
def rule_length(p, u): return len(p) >= 8
def rule_upper(p, u): return any(c.isupper() for c in p)
def rule_lower(p, u): return any(c.islower() for c in p)
def rule_digit(p, u): return any(c.isdigit() for c in p)
def rule_no_space(p, u): return " " not in p
def rule_banned(p, u): return not any(b in p.lower() for b in BANNED_SUBSTRINGS)
def rule_username(p, u): return u.lower() not in p.lower()

# Набор правил (флагов/функций)
PASSWORD_RULES = [
    rule_length, rule_upper, rule_lower,
    rule_digit, rule_no_space, rule_banned, rule_username
]

def check_password_configurable(password, username, rules=PASSWORD_RULES):
    for rule in rules:
        if not rule(password, username):
            return False # Если хоть одно правило вернуло False — пароль не прошел
    return True

# =====================================================================
# БЛОК 2: ЭКСПЕРИМЕНТ (Генерация и замеры)
# =====================================================================

def generate_passwords():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@"
    username = "admin"

    short_batch = []
    medium_batch = []
    long_batch = []

    for _ in range(1000):
        # Намеренно закидываем в 30% случаев нарушающие правила элементы
        trigger_fail = random.random() < 0.3

        # 1. Короткие (4-7 символов)
        len_s = random.randint(4, 7)
        p_s = "".join(random.choice(chars) for _ in range(len_s))
        if trigger_fail: p_s += "1234"
        short_batch.append(p_s)

        # 2. Средние (8-15 символов)
        len_m = random.randint(8, 15)
        p_m = "".join(random.choice(chars) for _ in range(len_m))
        if trigger_fail: p_m += "password"
        medium_batch.append(p_m)

        # 3. Длинные (16-64 символов)
        len_l = random.randint(16, 64)
        p_l = "".join(random.choice(chars) for _ in range(len_l))
        if trigger_fail: p_l += "admin"
        long_batch.append(p_l)

    return short_batch, medium_batch, long_batch, username

# Запуск замеров
short_p, medium_p, long_p, uname = generate_passwords()
batches = {
    "Короткие (4-7)": short_p,
    "Средние (8-15)": medium_p,
    "Длинные (16-64)": long_p
}

implementations = {
    "Наивная": check_password_naive,
    "Оптимизированная": check_password_optimized,
    "Конфигурируемая": check_password_configurable
}

print(f"{'Длина пароля':<16} | {'Версия':<18} | {'Время (сек)':<12} | {'Доля отклонённых'}")
print("-" * 70)

for b_name, b_data in batches.items():
    for impl_name, impl_func in implementations.items():

        rejected = 0
        t_start = time.perf_counter()

        for password in b_data:
            result = impl_func(password, uname)
            if not result:
                rejected += 1

        t_total = time.perf_counter() - t_start
        reject_rate = rejected / len(b_data)

        print(f"{b_name:<16} | {impl_name:<18} | {t_total:<12.6f} | {reject_rate:.2%}")

# Наивная - O(N * M). Каждое правило запускает свой отдельный цикл по всей длине строки.
# Оптимизированная - O(N). Делает всего один проход по строке, собирая все базовые флаги параллельно. От количества простых правил время почти не зависит.
# Конфигурируемая - O(N * M). Пробегается по списку функций, где каждая функция заново читает строку. Дополнительно тратит время на накладные расходы вызова функций в Python.

# Длина пароля: Разница критична на длинных паролях (от 16 до 64 символов) и больших объемах данных. На коротких строках (4–7 знаков) процессор обрабатывает всё мгновенно, и разницу в микросекундах не видно.
# Количество правил: Разница становится огромной, когда правил много (более 5–10). В наивной версии это приведет к 10 циклам вместо одного в оптимизированной.

# Наивная (Средне): Придется дописать еще один независимый цикл for в конец функции. Старый код не ломается, но добавляется лишний проход по памяти.
# Оптимизированная (Тяжело): Придется усложнять логику внутри существующего единственного цикла for. Добавятся новые счетчики, вложенные условия if-elif, что сильно запутает код.
# Конфигурируемая (Идеально): Сам код проверки вообще не меняется. Мы просто пишем одну изолированную функцию rule_three_classes(p, u) и дописываем ее имя в общий список правил PASSWORD_RULES.




































"""
1. Понятие «один проход по данным» и его связь с линейной сложностью:
   - Что это: Процесс, когда алгоритм считывает каждый элемент структуры
     (каждый символ пароля) строго один раз за один цикл for.
   - Связь: Это дает линейную сложность O(N). Время работы программы
     растет прямо пропорционально длине входных данных (длина строки N).

2. Почему важно учитывать количество проходов при больших объёмах данных:
   - Реальная скорость: В теории 1*O(N) и 10*O(N) — это один и тот же порядок
     линейной сложности. Но на практике 10 проходов займут в 10 раз больше
     реального процессорного времени.
   - Работа с памятью: При одном проходе данные считываются в быстрый кэш
     процессора один раз. Многократные проходы заставляют программу постоянно
     перечитывать данные из медленной оперативной памяти (RAM), что сильно
     замедляет систему на миллионах записей.
"""
