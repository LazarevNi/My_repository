def decorator(func):
    def wrapper(*args, **kwargs):
        if i % 5 == 0:
            func(t)
            print("Вам полагается бесплатная плюшка!")
        else:
            func(t)
            print()
    return wrapper


@decorator
def hello(t):  # Функция приветствующая клиента на входе
    return print(f"Привет,{t}!", end=' ')


i = 3

with open('client.txt', 'r', encoding="utf-8") as file:
    for t in file.read().split('\n'):
        hello(t)

while True:
    t = input("Имя следующего клиента:")
    i += 1
    hello(t)
