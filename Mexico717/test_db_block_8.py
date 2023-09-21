import psycopg2
import allure
import pytest


# Функция для подключения к базе
def connect_to_database():
    return psycopg2.connect(
        dbname="booking1695044281716gitjcybcuypocsdz",
        user="xbyhldngfbnffycorsngyajd@psql-mock-database-cloud",
        password="ahekqydueyjvpamoigqmffgp",
        host="psql-mock-database-cloud.postgres.database.azure.com"
    )


# Функция для создания пользователя
def create_user(connection, user_id, first_name):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (id, first_name) VALUES (%s, %s)", (user_id, first_name))
        connection.commit()
    finally:
        cursor.close()


# Функция удаления пользователя
def delete_user(connection, user_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()
    finally:
        cursor.close()
# Функция получения информации о пользователе по id
def get_user_by_id(connection, user_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        return result
    finally:
        cursor.close()

# Функция получения информации о пользователе по name
def get_user_by_name(connection, first_name):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE first_name = %s", (first_name,))
        result = cursor.fetchone()
        return result
    finally:
        cursor.close()

# Обновить id пользователя
def update_user_id(connection, user_id, new_user_id):
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE users SET id = %s WHERE id = %s", (new_user_id, user_id))
        connection.commit()
    finally:
        cursor.close()

# Обновить имя пользователя
def update_user_name(connection, user_id, new_name):
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE users SET first_name = %s WHERE id = %s", (new_name, user_id))
        connection.commit()
    finally:
        cursor.close()

# Тестовый сценарий для создания пользователя
@allure.feature("Создание пользователей по id и имени")
@allure.story("Добавляем неймара и месси")
@pytest.mark.parametrize("user_id, first_name",
                         [(131, "Messi"), (132, "Neymar")])  # Примеры параметров для создания пользователей
def test_create_user(user_id, first_name):
    # соединение с базой
    connection = connect_to_database()

    # Создание пользователя
    create_user(connection, user_id, first_name)

    # проверка что пользователь создан в БД
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()

    # Проверка что запись в БД
    assert result is not None
    assert result[0] == user_id
    assert result[1] == first_name

    # Закрываем соединение с базой данных
    connection.close()


@allure.feature('Удаление пользователей')
@allure.story('Удаление пользователей по id')
@pytest.mark.parametrize("user_id", [131, 132])
def test_delete_user(user_id):
    # Соединение с базой
    connection = connect_to_database()
    # Удаление пользователя
    delete_user(connection, user_id)

    # Проверка что пользователь удален из базы
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    assert result is None, f"Пользователь с ID {user_id} не был удален из базы данных."


@allure.feature('Получение информации о пользователях')
@allure.story('Получение информации о пользователях по id')
def test_get_user_by_id():
    # Соединение с базой
    connection = connect_to_database()

    # Создаем пользователя для теста
    user_id = 999
    first_name = "TestUser"
    create_user(connection, user_id, first_name)

    # Получаем информацию о пользователе по ID
    result = get_user_by_id(connection, user_id)

    # Проверяем, что результат не пустой и содержит правильные данные
    assert result is not None
    assert result[0] == user_id
    assert result[1] == first_name

    #Удаляем созданного юзера
    delete_user(connection, user_id)

    # Проверка что пользователь удален из базы
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    assert result is None, f"Пользователь с ID {user_id} не был удален из базы данных."

    # Закрываем соединение с базой данных
    connection.close()


@allure.feature('Получение информации о пользователях')
@allure.story('Получение информации о пользователях по name')
def test_get_user_by_name():
    # Соединение с базой
    connection = connect_to_database()

    # Создаем пользователя для теста
    user_id = 1000
    first_name = "TestUser2"
    create_user(connection, user_id, first_name)

    # Получаем информацию о пользователе по имени
    result = get_user_by_name(connection, first_name)

    # Проверяем, что результат не пустой и содержит правильные данные
    assert result is not None
    assert result[0] == user_id
    assert result[1] == first_name

    # Удаляем созданного юзера
    delete_user(connection, user_id)

    # Проверка что пользователь удален из базы
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    assert result is None, f"Пользователь с ID {user_id} не был удален из базы данных."

    # Закрываем соединение с базой данных
    connection.close()

@allure.feature('Изменение информации о пользователях')
@allure.story('Изменение информации о пользователях по id')
def test_update_user_id():
    # Соединение с базой
    connection = connect_to_database()

    # Создаем пользователя для теста
    user_id = 999
    new_user_id = 888
    first_name = "TestUser"
    create_user(connection, user_id, first_name)

    # Обновляем ID пользователя
    update_user_id(connection, user_id, new_user_id)

    # Получаем информацию о пользователе по новому ID
    result = get_user_by_id(connection, new_user_id)

    # Проверяем, что результат не пустой и содержит правильные данные
    assert result is not None
    assert result[0] == new_user_id
    assert result[1] == first_name

    # Закрываем соединение с базой данных
    connection.close()

@allure.feature('Изменение информации о пользователях')
@allure.story('Изменение информации о пользователях по name')
def test_update_user_name():
    # Соединение с базой
    connection = connect_to_database()

    # Создаем пользователя для теста
    user_id = 1000
    first_name = "TestUser"
    create_user(connection, user_id, first_name)

    # Обновляем имя пользователя
    new_name = "UpdatedUser"
    update_user_name(connection, user_id, new_name)

    # Получаем информацию о пользователе по ID
    result = get_user_by_id(connection, user_id)

    # Проверяем, что результат не пустой и содержит правильное обновленное имя
    assert result is not None
    assert result[0] == user_id
    assert result[1] == new_name

    # Закрываем соединение с базой данных
    connection.close()