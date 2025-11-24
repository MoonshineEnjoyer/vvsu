def read_list(file_name):
    """
    Читает из файла список пронумерованных названий
    """
    l = []
    with open(file_name) as fin:
        for line in fin.readlines():
            l.append(line.split()[1])
    return l


def read_attributes(file_name, objects, predicates):
    """
    Читает из файла булеву матрицу, в которой
    строки - это объекты (с названиями objects)
    столбцы - это свойства (с названиями predicates)
    Возвращает словарь: ключ - название объекта, значение - множество названий
    """
    with open(file_name) as fin:
        l = dict()
        for j, line in enumerate(fin.readlines()):
            s = set()
            for i, x in enumerate(line.split()):
                if int(x):
                    s.add(predicates[i])
            l[objects[j]] = s
    return l


animals = read_list("classes.txt")
predicates = read_list("predicates.txt")
attributes = read_attributes("predicate-matrix-binary.txt", animals, predicates)


print("1. Из перечисленных животных летать умеет только летучая мышь.")
forall = True
counterexamples = []
for animal in animals:
    if 'flys' in attributes[animal]:
        if animal != 'bat':
            forall = False
            counterexamples.append(animal)
print(forall, counterexamples)

print("2. Существуют животные, которые одновременно сильные и слабые.")
exists = False
examples = []
for animal in animals:
    if 'strong' in attributes[animal] and 'weak' in attributes[animal]:
        exists = True
        examples.append(animal)
print(exists, examples)

print("3. Все животные, обитающие в океане, живут в воде.")
forall = True
counterexamples = []
for animal in animals:
    if 'ocean' in attributes[animal] and 'water' not in attributes[animal]:
        forall = False
        counterexamples.append(animal)
print(forall, counterexamples)

print("4. Среди животных, живущих в воде, найдутся те, которые живут не в океане.")
exists = False
examples = []
for animal in animals:
    if 'water' in attributes[animal] and 'ocean' not in attributes[animal]:
        exists = True
        examples.append(animal)
print(exists, examples)

print("5. Все животные оранжевого цвета умеют ходить.")
forall = True
counterexamples = []
for animal in animals:
    if 'orange' in attributes[animal] and 'walks' not in attributes[animal]:
        forall = False
        counterexamples.append(animal)
print(forall, counterexamples)

print("6. Все животные, обитающие в Новом Свете, водятся и в Старом Свете.")
forall = True
counterexamples = []
for animal in animals:
    if 'newworld' in attributes[animal] and 'oldworld' not in attributes[animal]:
        forall = False
        counterexamples.append(animal)
print(forall, counterexamples)

print("7. Все домашние животные умные.")
forall = True
counterexamples = []
for animal in animals:
    if 'domestic' in attributes[animal] and 'smart' not in attributes[animal]:
        forall = False
        counterexamples.append(animal)
print(forall, counterexamples)

print("8. Среди животных, живущих в воде, найдутся те, кто не питается рыбой.")
exists = False
examples = []
for animal in animals:
    if 'water' in attributes[animal] and 'fish' not in attributes[animal]:
        exists = True
        examples.append(animal)
print(exists, examples)

print("9. Среди животных, питающихся планктоном, найдутся те, кто не питается рыбой.")
exists = False
examples = []
for animal in animals:
    if 'plankton' in attributes[animal] and 'fish' not in attributes[animal]:
        exists = True
        examples.append(animal)
print(exists, examples)

print("10. Все животные, умеющие плавать, не умеют ходить.")
forall = True
counterexamples = []
for animal in animals:
    if 'swims' in attributes[animal] and 'walks' in attributes[animal]:
        forall = False
        counterexamples.append(animal)
print(forall, counterexamples)
