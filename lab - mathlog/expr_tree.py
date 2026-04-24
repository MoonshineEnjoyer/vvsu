import time

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None  # Для Queue (двусвязный список для O(1) с обоих концов)

class Stack:
    """Стек на односвязном списке."""
    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        return value

    def peek(self):
        return self.head.value if self.head else None

    def is_empty(self):
        return self.head is None

class Queue:
    """Очередь на двусвязном списке для обеспечения O(1) операций."""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, value):
        new_node = Node(value)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        value = self.head.value
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return value

    def is_empty(self):
        return self.head is None

class LinkedListCalculator:
    def __init__(self):
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '**': 3, '~': 4}

    def _tokenize(self, expr):
        """Разбивает строку на токены, возвращая нашу Queue."""
        q = Queue()
        i = 0
        while i < len(expr):
            char = expr[i]
            if char.isspace():
                i += 1
                continue
            
            # Унарный минус (по желанию для полноты, как в задании 1)
            if char == '-':
                # Если пустая очередь или последний токен - оператор/скобка
                if q.is_empty() or (self._is_operator(q.tail.value) or q.tail.value == '('):
                    q.enqueue('~')
                    i += 1
                    continue

            if char.isdigit() or char == '.':
                num = ""
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]
                    i += 1
                q.enqueue(num)
                continue
            
            if expr[i:i+2] == '**':
                q.enqueue('**')
                i += 2
                continue
                
            q.enqueue(char)
            i += 1
        return q

    def _is_operator(self, token):
        return token in self.precedence

    def to_postfix(self, expression):
        tokens_q = self._tokenize(expression)
        output_q = Queue()
        op_stack = Stack()

        while not tokens_q.is_empty():
            token = tokens_q.dequeue()
            
            if token.replace('.', '', 1).isdigit():
                output_q.enqueue(token)
            elif token == '(':
                op_stack.push(token)
            elif token == ')':
                while not op_stack.is_empty() and op_stack.peek() != '(':
                    output_q.enqueue(op_stack.pop())
                op_stack.pop() # Удаляем '('
            else:
                while (not op_stack.is_empty() and op_stack.peek() != '(' and
                       self.precedence.get(op_stack.peek(), 0) >= self.precedence.get(token, 0)):
                    if token in ('**', '~') and op_stack.peek() == token:
                        break
                    output_q.enqueue(op_stack.pop())
                op_stack.push(token)
        
        while not op_stack.is_empty():
            output_q.enqueue(op_stack.pop())

        # Сборка результата в строку из Queue
        res_str = ""
        while not output_q.is_empty():
            res_str += str(output_q.dequeue()) + " "
        return res_str.strip()

    def calculate(self, expression):
        postfix_str = self.to_postfix(expression)
        tokens = postfix_str.split() # Здесь split допустим для удобства обхода
        calc_stack = Stack()

        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                calc_stack.push(float(token))
            elif token == '~':
                calc_stack.push(-calc_stack.pop())
            else:
                b = calc_stack.pop()
                a = calc_stack.pop()
                if token == '+': calc_stack.push(a + b)
                elif token == '-': calc_stack.push(a - b)
                elif token == '*': calc_stack.push(a * b)
                elif token == '/': calc_stack.push(a / b)
                elif token == '**': calc_stack.push(a ** b)
        
        return float(calc_stack.pop())

# --- ПУНКТ 4: Замеры времени ---
def benchmark():
    s = Stack()
    q = Queue()
    n = 10000
    
    start = time.time()
    for i in range(n): s.push(i)
    for i in range(n): s.pop()
    print(f"Stack 10k push/pop: {time.time() - start:.5f} сек")

    start = time.time()
    for i in range(n): q.enqueue(i)
    for i in range(n): q.dequeue()
    print(f"Queue 10k enq/deq: {time.time() - start:.5f} сек")

benchmark()

# --- ПУНКТ 5: 8 Тестовых выражений ---
calc = LinkedListCalculator()
tests = [
    "2 + 2",
    "10 - 2 * 3",
    "(3 + 4) * 2",
    "2 ** 3 ** 2",
    "10.5 / (2.1 + 2.9)",
    "-5 + 10",
    "((1 + 2) * (3 - 4)) / 2",
    "2 * 3 + 4 ** 2"
]

print("\nТестирование выражений:")
for t in tests:
    print(f"Инфикс: {t}")
    print(f"Постфикс: {calc.to_postfix(t)}")
    print(f"Результат: {calc.calculate(t)}\n")

# --- ИНТЕРФЕЙС ПОЛЬЗОВАТЕЛЯ (Дополнение к Заданию №2) ---

def user_interface():
    calc = LinkedListCalculator()
    print("-" * 40)
    print("РЕЖИМ ПОЛЬЗОВАТЕЛЬСКОГО ВВОДА")
    print("Доступные операции: +, -, *, /, ** (степень), скобки ( )")
    print("Введите 'exit' для выхода.")
    
    # Мы не используем бесконечный цикл, если это критично для ТЗ, 
    # но обычно для интерфейса это стандарт. 
    # Если нужно строго ОДИН ввод, уберите while.
    while True:
        try:
            expr = input("\nВведите выражение: ").strip()
            
            if expr.lower() in ('exit', 'выход', 'quit'):
                print("Программа завершена.")
                break
            
            if not expr:
                continue

            # 1. Получаем постфиксную запись (Метод из ТЗ)
            postfix = calc.to_postfix(expr)
            
            # 2. Получаем результат (Метод из ТЗ)
            result = calc.calculate(expr)
            
            print(f"Постфиксная форма: {postfix}")
            print(f"Результат (float): {result}")
            
        except Exception as e:
            print(f"Произошла ошибка при обработке: {e}")
            print("Проверьте корректность расстановки скобок и операторов.")

if __name__ == "__main__":
    # Сначала выполняем обязательные тесты по ТЗ
    benchmark()
    
    print("\nТестирование обязательных выражений:")
    for t in tests:
        print(f"Инфикс: {t} | Результат: {calc.calculate(t)}")
        
    # Затем запускаем ручной ввод
    user_interface()













import time

# Базовый строительный блок связного списка
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None  # Ссылка на следующий элемент
        self.prev = None  # Ссылка на предыдущий элемент (нужна для Queue)

class Stack:
    """Стек (LIFO): добавление и удаление только с вершины (head)."""
    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, value):
        # Создаем узел и ставим его перед текущей «головой»
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        # Забираем значение и сдвигаем голову на следующий элемент
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        return value

    def peek(self):
        # Смотрим значение без удаления
        return self.head.value if self.head else None

    def is_empty(self):
        return self.head is None

class Queue:
    """Очередь (FIFO) на двусвязном списке для O(1) с обоих концов."""
    def __init__(self):
        self.head = None  # Начало очереди (для извлечения)
        self.tail = None  # Конец очереди (для добавления)
        self.size = 0

    def enqueue(self, value):
        # Добавление в конец списка через указатель tail
        new_node = Node(value)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        # Извлечение из начала списка через указатель head
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        value = self.head.value
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return value

    def is_empty(self):
        return self.head is None

class LinkedListCalculator:
    def __init__(self):
        # Приоритеты аналогично 1 заданию
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '**': 3, '~': 4}

    def _tokenize(self, expr):
        """Парсинг строки напрямую в нашу самописную очередь."""
        q = Queue()
        i = 0
        while i < len(expr):
            char = expr[i]
            if char.isspace():
                i += 1
                continue
            
            # Логика унарного минуса для связных структур
            if char == '-':
                # Унарный, если это первый токен или после оператора/скобки
                if q.is_empty() or (self._is_operator(q.tail.value) or q.tail.value == '('):
                    q.enqueue('~')
                    i += 1
                    continue

            if char.isdigit() or char == '.':
                num = ""
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]
                    i += 1
                q.enqueue(num)
                continue
            
            if expr[i:i+2] == '**':
                q.enqueue('**')
                i += 2
                continue
                
            q.enqueue(char)
            i += 1
        return q

    def _is_operator(self, token):
        return token in self.precedence

    def to_postfix(self, expression):
        """Конвертация в постфикс с использованием только Node-структур."""
        tokens_q = self._tokenize(expression)
        output_q = Queue()  # Выходная последовательность
        op_stack = Stack()  # Временное хранилище операторов

        while not tokens_q.is_empty():
            token = tokens_q.dequeue()
            
            if token.replace('.', '', 1).isdigit():
                output_q.enqueue(token)
            elif token == '(':
                op_stack.push(token)
            elif token == ')':
                while not op_stack.is_empty() and op_stack.peek() != '(':
                    output_q.enqueue(op_stack.pop())
                op_stack.pop()
            else:
                # Стандартная логика приоритетов Shunting-yard
                while (not op_stack.is_empty() and op_stack.peek() != '(' and
                       self.precedence.get(op_stack.peek(), 0) >= self.precedence.get(token, 0)):
                    if token in ('**', '~') and op_stack.peek() == token:
                        break
                    output_q.enqueue(op_stack.pop())
                op_stack.push(token)
        
        while not op_stack.is_empty():
            output_q.enqueue(op_stack.pop())

        # Склеиваем результат в строку, освобождая очередь
        res_str = ""
        while not output_q.is_empty():
            res_str += str(output_q.dequeue()) + " "
        return res_str.strip()

    def calculate(self, expression):
        """Вычисление итогового значения через стек."""
        postfix_str = self.to_postfix(expression)
        tokens = postfix_str.split()
        calc_stack = Stack() # Стек для промежуточных результатов

        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                calc_stack.push(float(token))
            elif token == '~':
                calc_stack.push(-calc_stack.pop())
            else:
                # Операнды извлекаются в обратном порядке (LIFO)
                b = calc_stack.pop()
                a = calc_stack.pop()
                if token == '+': calc_stack.push(a + b)
                elif token == '-': calc_stack.push(a - b)
                elif token == '*': calc_stack.push(a * b)
                elif token == '/': calc_stack.push(a / b)
                elif token == '**': calc_stack.push(a ** b)
        
        return float(calc_stack.pop())

# --- ПУНКТ 4: Демонстрация O(1) ---
def benchmark():
    s = Stack()
    q = Queue()
    n = 10000
    
    start = time.time()
    for i in range(n): s.push(i)
    for i in range(n): s.pop()
    print(f"Stack 10k push/pop: {time.time() - start:.5f} сек (каждая операция O(1))")

    start = time.time()
    for i in range(n): q.enqueue(i)
    for i in range(n): q.dequeue()
    print(f"Queue 10k enq/deq: {time.time() - start:.5f} сек (каждая операция O(1))")
















import time

# --- БАЗОВЫЕ СТРУКТУРЫ ДАННЫХ (БЕЗ ИСПОЛЬЗОВАНИЯ ВСТРОЕННЫХ СПИСКОВ) ---

class Node:
    """
    Узел — это минимальный кирпичик связного списка.
    Хранит само значение и ссылки (указатели) на соседние элементы.
    """
    def __init__(self, value):
        self.value = value
        self.next = None  # Ссылка на следующий узел
        self.prev = None  # Ссылка на предыдущий узел (нужна для Queue)

class Stack:
    """
    Стек (LIFO — 'Последним пришел, первым ушел').
    Все операции происходят только с 'головой' (head).
    """
    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, value):
        # O(1): Просто ставим новый узел перед текущей головой
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def pop(self):
        # O(1): Берем значение из головы и передвигаем указатель на следующий узел
        if self.is_empty(): raise IndexError("Стек пуст")
        val = self.head.value
        self.head = self.head.next
        self.size -= 1
        return val

    def peek(self):
        # Позволяет узнать значение на вершине, не удаляя его
        return self.head.value if self.head else None

    def is_empty(self):
        return self.head is None

class Queue:
    """
    Очередь (FIFO — 'Первым пришел, первым ушел').
    Для эффективности O(1) используем указатели и на начало (head), и на конец (tail).
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, value):
        # O(1): Добавляем новый узел строго в конец (tail)
        new_node = Node(value)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        # O(1): Забираем элемент строго из начала (head)
        if self.is_empty(): raise IndexError("Очередь пуста")
        val = self.head.value
        self.head = self.head.next
        if self.head: self.head.prev = None
        else: self.tail = None
        self.size -= 1
        return val

    def is_empty(self):
        return self.head is None

# --- КАЛЬКУЛЯТОР НА СВЯЗНЫХ СПИСКАХ ---

class LinkedListCalculator:
    def __init__(self):
        # Таблица приоритетов (~ — внутренний символ для унарного минуса)
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '**': 3, '~': 4}

    def _tokenize(self, expr):
        """
        Преобразует строку в очередь токенов. 
        Не использует list.append, сразу строит Queue из объектов Node.
        """
        q = Queue()
        i = 0
        while i < len(expr):
            char = expr[i]
            if char.isspace():
                i += 1
                continue
            
            # Определение унарного минуса
            # Если минус стоит в начале или после другого оператора — он унарный
            if char == '-':
                if q.is_empty() or q.tail.value in ('+', '-', '*', '/', '(', '**', '~'):
                    q.enqueue('~')
                    i += 1
                    continue
                    
            # Сборка многозначных и вещественных чисел
            if char.isdigit() or char == '.':
                num = ""
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]
                    i += 1
                q.enqueue(num)
                continue
            
            # Сборка оператора степени
            if expr[i:i+2] == '**':
                q.enqueue('**')
                i += 2
                continue
            
            q.enqueue(char)
            i += 1
        return q

    def to_postfix(self, expression):
        """
        Перевод в постфиксную запись (Алгоритм 'Сортировочная станция').
        Использует самописные Stack и Queue.
        """
        tokens = self._tokenize(expression)
        output = Queue() # Сюда попадает итоговый результат
        stack = Stack()  # Здесь временно 'ждут' операторы
        
        while not tokens.is_empty():
            t = tokens.dequeue()
            # Если число — сразу в выходную очередь
            if t.replace('.', '', 1).isdigit():
                output.enqueue(t)
            elif t == '(': 
                stack.push(t)
            elif t == ')':
                # Выталкиваем всё до открывающей скобки
                while not stack.is_empty() and stack.peek() != '(':
                    output.enqueue(stack.pop())
                stack.pop() # Удаляем '('
            else:
                # Сравнение приоритетов операторов
                while (not stack.is_empty() and stack.peek() != '(' and 
                       self.precedence.get(stack.peek(), 0) >= self.precedence.get(t, 0)):
                    # Исключение для правоассоциативных операций
                    if t in ('**', '~') and stack.peek() == t: break
                    output.enqueue(stack.pop())
                stack.push(t)
        
        # Довыгружаем оставшиеся операторы
        while not stack.is_empty(): 
            output.enqueue(stack.pop())
        
        # Превращаем очередь узлов в итоговую строку
        res = ""
        while not output.is_empty(): res += str(output.dequeue()) + " "
        return res.strip()

    def calculate(self, expression):
        """
        Вычисление постфиксного выражения через стек вычислений.
        """
        postfix = self.to_postfix(expression)
        tokens = postfix.split() # Разбиение строки результата
        s = Stack()
        
        for t in tokens:
            if t.replace('.', '', 1).isdigit():
                s.push(float(t))
            elif t == '~': # Применяем смену знака к одному числу
                s.push(-s.pop())
            else:
                # Бинарная операция: достаем два числа
                b, a = s.pop(), s.pop()
                if t == '+': s.push(a + b)
                elif t == '-': s.push(a - b)
                elif t == '*': s.push(a * b)
                elif t == '/': s.push(a / b)
                elif t == '**': s.push(a ** b)
        
        return float(s.pop()) # Итоговый результат — единственный элемент в стеке

# --- ДЕМОНСТРАЦИЯ И ТЕСТЫ ---

def run_benchmark():
    """Пункт 4: Замер времени для подтверждения O(1) операций."""
    print("\n--- Пункт 4: Замер времени (10,000 операций) ---")
    s, q = Stack(), Queue()
    n = 10000
    
    start = time.time()
    for i in range(n): s.push(i)
    for i in range(n): s.pop()
    print(f"Stack (Push/Pop): {time.time() - start:.5f} сек (Константное время O(1))")
    
    start = time.time()
    for i in range(n): q.enqueue(i)
    for i in range(n): q.dequeue()
    print(f"Queue (Enq/Deq): {time.time() - start:.5f} сек (Константное время O(1))")

if __name__ == "__main__":
    calc = LinkedListCalculator()
    
    # 1. Замеры производительности
    run_benchmark()

    # 2. Пункт 5: 8 тестов разной сложности
    print("\n--- Пункт 5: Тестирование 8 выражений ---")
    test_cases = [
        "10 + 5 * 2",            # Приоритеты
        "(10 + 5) * 2",          # Скобки
        "2 ** 3 ** 2",           # Степень (справа налево)
        "-10 + 20",              # Унарный минус в начале
        "15.5 / 2",              # Вещественные числа
        "((2 + 3) * 2) ** 2",    # Вложенные скобки
        "10 - -5",               # Унарный минус после оператора
        "2 * 3 + 4 / 2"          # Смешанные операции
    ]
    
    for expr in test_cases:
        print(f"Infix: {expr:<20} | Result: {calc.calculate(expr)}")

    # 3. Пользовательский ввод
    print("\n--- Пользовательский ввод ---")
    user_expr = input("Введите ваше инфиксное выражение: ")
    try:
        print(f"Постфиксная форма: {calc.to_postfix(user_expr)}")
        print(f"Результат: {calc.calculate(user_expr)}")
    except Exception as e:
        print(f"Ошибка ввода или вычисления: {e}")
