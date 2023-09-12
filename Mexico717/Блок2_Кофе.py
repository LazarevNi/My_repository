from typing import List

with open('test_1.txt', 'r') as file:
    lines = file.readlines()
i = 0
my_list = []  # Лист для сбора значений чашек кофе
kolichestvo_strok = len(lines)
while i <= len(lines) - 1:  # Цикл для записи всех значений чашек кофе в лист
    t = lines[i]
    p = t.split()
    my_list.append(p[1])
    i += 1
i = 0
for i in range(len(my_list)):  # цикл для преобразования значений листа в тип int
    my_list[i] = int(my_list[i])
max_number = max(my_list)  # Присваиваем переменной максимальное значение из этого списка
i = 0
my_list2 = []  # Лист для сбора имен
my_list3 = []  # Лист для сбора количества бонусных чашек кофе
while i <= kolichestvo_strok - 1:  # Цикл для записи имен и бонусных чашек кофе в лист 2 и 3
    names_and_numbers1: list[str] = lines[i].split()
    k = int(names_and_numbers1[1]) // 6
    print("Для", names_and_numbers1[0], "Количество бонусных чашек кофе ", k)
    i += 1
    my_list2.append(names_and_numbers1[0])
    my_list3.append(k)
my_dictionary = dict(zip(my_list2, my_list3))  # словарь для записи имени и количества чашек бонусных для него
key_val = my_dictionary.items()
key_val_list = list(key_val)
kv = max(key_val_list, key=lambda i: i[1])
print("Максимальное значение чашек кофе будет у", kv[0], kv[1])
my_file = open("my_file.txt", "w+")
my_file.write(kv[0])
my_file.close()
