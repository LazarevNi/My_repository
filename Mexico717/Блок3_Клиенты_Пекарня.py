def hello(t):  # Функция приветствующая клиента на входе
    return print("Привет,",t, end='')

with open('client.txt', 'r', encoding="utf-8") as file:
    for t in file:
        hello(t)

def decorator(func):
    def wrapper():
        for i in range(4, 10000):
            m = input("\nСледующий клиент:")
            if i % 5 == 0:
                func(m)
                print("! Вам полагается бесплатная плюшка!", sep=" ", end='' )
            else:
                func(m)
            i += 1
    return wrapper

hello = decorator(hello)
hello()
