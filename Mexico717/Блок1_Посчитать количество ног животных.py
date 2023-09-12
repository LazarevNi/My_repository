with open('farm.txt', 'r') as file:
    lines = file.readlines()
number_sheep = int(lines[0])
number_pig = int(lines[1])
number_duck = int(lines[2])
print("Количество овец =", number_sheep,
      "\nКоличество свиней =", number_pig,
      "\nКоличество уток =", number_duck)
number_legsAll = number_sheep*4+number_pig*4+number_duck*2
print("Количество всех ног животных =", number_legsAll)

