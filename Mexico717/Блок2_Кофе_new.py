with open('test_1.txt', 'r') as file:
    lines = file.readlines()
i = 0
my_list = []    # Лист для сбора значений чашек кофе
numbers_rows = len(lines)   # Количество строк

while i <= len(lines) - 1:  # Цикл для записи всех значений чашек кофе в лист
    my_list.append(lines[i].split()[1])
    i += 1

i = 0

for i in range(len(my_list)):   # цикл для преобразования значений листа в тип int
    my_list[i] = int(my_list[i])
max_number = max(my_list)

i = 0

my_list2 = []  # Лист для сбора имен
my_list3 = []  # Лист для сбора количества бонусных чашек кофе
while i <= numbers_rows - 1:  # Цикл для записи имен и бонусных чашек кофе в лист 2 и 3
    names_and_numbers1: list[str] = lines[i].split()
    k = int(names_and_numbers1[1]) // 6
    print("Для", names_and_numbers1[0], "Количество бонусных чашек кофе ", k)
    i += 1
    my_list2.append(names_and_numbers1[0])
    my_list3.append(k)

my_dictionary = dict(zip(my_list2, my_list3))  # словарь для записи имени и количества чашек бонусных для него
r=1
my_file = open("my_file.txt", "w")  #Это для того чтобы очистить файл my_file перед работой цикла
my_file.close()
for k in my_dictionary: # Конструкция для поиска ключа с максимальным значением
    if my_dictionary[k]>=r:
        r=my_dictionary[k]
        m=k
        print("Максимальное значение чашек кофе будет у", m, r)
        my_file = open("my_file.txt", "a")
        my_file.write(k+'\n')
        my_file.close()