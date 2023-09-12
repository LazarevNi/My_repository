def concatenate_strings(s1, s2):
    return str(s1) + str(s2)

def test_concatenate_strings_base():    #Проверка базового случая: конкатенация двух непустых строк
    assert concatenate_strings("Hello", "World") == "HelloWorld"

def test_concatenate_strings_first_is_null():    #Проверка пустая первая
    assert concatenate_strings("", "World") == "World"

def test_concatenate_strings_second_is_null():    #Проверка пустая вторая
    assert concatenate_strings("World", "") == "World"

def test_concatenate_strings_all_is_null():    #Обе пустые
    assert concatenate_strings("", "") == ""

def test_concatenate_strings_with_special_characters():    #Сложение строк со спец символами
    assert concatenate_strings("№%%2+@++===!!", "") == "№%%2+@++===!!"

def test_concatenate_strings_have_numbers():    #Проверка если одна из строк это число
    assert concatenate_strings(2, "") == "2"

def test_concatenate_strings_have_numbers():    #Проверка если вместо строк подаются числа
    assert concatenate_strings(2, 3) == "23"

def test_concatenate_strings_order():   #Проверка порядка строк
    assert concatenate_strings("Hello", "World") == "HelloWorld"
    assert concatenate_strings("World", "Hello") == "WorldHello"

def test_concatenate_strings_type():    #Проверка типа возвращаемых данных
    assert isinstance(concatenate_strings("Hello", "World"), str) == True

