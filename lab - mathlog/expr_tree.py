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
