import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
import allure


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@allure.feature("Тест логина и разлогина на сайте")
def test_login_logout(driver):
    driver.get("https://www.saucedemo.com/")

    # Логин и ожидание пока элемент не станет кликабельным
    # во всех следующих проверках добавлено время ожидания до появления элементов
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "user-name"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys("standard_user")
    password_input.send_keys("secret_sauce")
    login_button.click()

    # Проверка успешного входа
    inventory_url = WebDriverWait(driver, 10).until(
        EC.url_contains("inventory.html")
    )
    assert inventory_url, "Вход не выполнен успешно"

    # Выход
    menu_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    )
    menu_button.click()

    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    )
    logout_link.click()

    # Проверка успешного выхода
    login_url = WebDriverWait(driver, 10).until(
        EC.url_to_be("https://www.saucedemo.com/")
    )
    assert login_url, "Выход не выполнен успешно"


@allure.feature("Тест, что каждый товар  можно купить")
@pytest.mark.parametrize("product_name_id", ["add-to-cart-sauce-labs-backpack",
                                             "add-to-cart-sauce-labs-bike-light",
                                             "add-to-cart-sauce-labs-bolt-t-shirt",
                                             "add-to-cart-sauce-labs-fleece-jacket",
                                             "add-to-cart-sauce-labs-onesie",
                                             "add-to-cart-test.allthethings()-t-shirt-(red)"])
def test_buy_some_things(driver, product_name_id):
    # Заходим на сайт и авторизуемся
    driver.get("https://www.saucedemo.com/")
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "user-name"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys("standard_user")
    password_input.send_keys("secret_sauce")
    login_button.click()
    # находим кнопку добавления сумки и кликаем по ней
    button_for_sale = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, product_name_id))
    )
    button_for_sale.click()
    # Находим иконку корзины и кликаем по ней и нажимаем чекаут
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    button_checkout = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    )
    button_checkout.click()
    # Заполняем данные и нажимаем Continue
    firstname_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "first-name"))
    )
    lastname_input = driver.find_element(By.ID, "last-name")
    postal_code_input = driver.find_element(By.ID, "postal-code")
    continue_button = driver.find_element(By.ID, "continue")

    firstname_input.send_keys("Nikita")
    lastname_input.send_keys("Lazarev")
    postal_code_input.send_keys("389567")
    continue_button.click()
    finish_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "finish"))
    )
    finish_button.click()

    expected_url = "https://www.saucedemo.com/checkout-complete.html"
    assert driver.current_url == expected_url


@allure.story("Тестирование изменения счетчика товаров")
def test_change_counter(driver):
    # Заходим на сайт и авторизуемся
    driver.get("https://www.saucedemo.com/")
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "user-name"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys("standard_user")
    password_input.send_keys("secret_sauce")
    login_button.click()

    # добавляем первый товар в корзину
    add_to_cart_button1 = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_to_cart_button1.click()
    # Находим элемент счетчика и запоминаем
    time.sleep(1)
    counter_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    one_cart_count = int(counter_badge.text)
    # добавляем второй товар в корзину
    add_to_cart_button2 = driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light")
    add_to_cart_button2.click()
    # элемент счетчика корзины новый
    new_cart_count = int(counter_badge.text)

    # Проверьте, что значение счетчика увеличилось на 1
    assert new_cart_count == one_cart_count + 1, "Счетчик корзины не изменился после добавления товара"
    # Удаляем товар из корзины
    remove_button = driver.find_element(By.ID, "remove-sauce-labs-backpack")
    remove_button.click()
    time.sleep(1)
    # Проверка
    updated_cart_count_after_remove = int(counter_badge.text)
    assert updated_cart_count_after_remove == new_cart_count - 1, "Счетчик корзины не вернулся к значению 1 njdfhf после удаления товара"


@allure.feature("Тестирование сортировок")
@allure.story("Тест сортировки от низкой до высокой цены")
def test_sorting_price_low_to_high(driver):
    # Заходим на сайт и авторизуемся
    driver.get("https://www.saucedemo.com/")
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "user-name"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys("standard_user")
    password_input.send_keys("secret_sauce")
    login_button.click()

    # Получим цены всех продуктов
    product_prices = []
    product_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    for element in product_elements:
        price_text = element.text
        # Преобразуем текст цены в число (удаляем символ "$")
        price = float(price_text.replace("$", ""))
        product_prices.append(price)
    # print(product_prices)

    # Выполним сортировку цен
    sort_select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_select.select_by_value("lohi")  # Сортировка от низкой к высокой цене

    time.sleep(2)

    # Запихиваем в новый список отсортированные значения
    product_prices_new = []
    product_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    for element in product_elements:
        price_text = element.text
        # Преобразуем текст цены в число (удаляем символ "$")
        price = float(price_text.replace("$", ""))
        product_prices_new.append(price)
    # print(product_prices_new)

    # Проверяем, что если отсортированный 1 список будет таким же как новый product_prices_new
    assert product_prices_new == sorted(product_prices)


@allure.feature("Тестирование сортировок")
@allure.story("Тест сортировки от высокой до низкой цены")
def test_sorting_price_high_to_low(driver):
    # Заходим на сайт и авторизуемся
    driver.get("https://www.saucedemo.com/")
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "user-name"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys("standard_user")
    password_input.send_keys("secret_sauce")
    login_button.click()

    # Получим цены всех продуктов
    product_prices = []
    product_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    for element in product_elements:
        price_text = element.text
        # Преобразуем текст цены в число (удаляем символ "$")
        price = float(price_text.replace("$", ""))
        product_prices.append(price)
    # print(product_prices)

    # Выполним сортировку цен
    sort_select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_select.select_by_value("hilo")  # Сортировка от высокой к низкой цене

    time.sleep(2)

    # Запихиваем в новый список отсортированные значения
    product_prices_new = []
    product_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    for element in product_elements:
        price_text = element.text
        # Преобразуем текст цены в число (удаляем символ "$")
        price = float(price_text.replace("$", ""))
        product_prices_new.append(price)
    # print(product_prices_new)

    # Проверяем, что если отсортированный 1 список будет таким же как новый product_prices_new
    assert product_prices_new == sorted(product_prices, reverse=True)


@allure.feature("Тестирование сортировок")
@allure.story("Тест сортироваки from A to Z")
def test_sort_names_AtoZ(driver):
    # Заходим на сайт и авторизуемся
    driver.get("https://www.saucedemo.com/")
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "user-name"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys("standard_user")
    password_input.send_keys("secret_sauce")
    login_button.click()

    # Получим имена всех продуктов в список
    names = []
    product_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    for element in product_elements:
        name_text = element.text
        names.append(name_text)
    # print(names)

    # Выполним сортировку имен от A to Z на сайте
    sort_select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_select.select_by_value("az")  # Сортировка от a to z

    time.sleep(2)

    # Получим имена всех продуктов в список после сортировки
    names_new = []
    product_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    for element in product_elements:
        name_text = element.text
        names_new.append(name_text)
    # print(names_new)

    # Сравниваем отсортированный список с сайта со старым списком(отсортированным нами)
    assert names_new == sorted(names, key=lambda x: x.lower())


@allure.feature("Тестирование сортировок")
@allure.story("Тест сортироваки from Z to A")
def test_sort_names_ZtoA(driver):
    # Заходим на сайт и авторизуемся
    driver.get("https://www.saucedemo.com/")
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "user-name"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys("standard_user")
    password_input.send_keys("secret_sauce")
    login_button.click()

    # Получим имена всех продуктов в список
    names = []
    product_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    for element in product_elements:
        name_text = element.text
        names.append(name_text)
    print(names)

    # Выполним сортировку имен от Z to A на сайте
    sort_select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_select.select_by_value("za")  # Сортировка от z to a

    time.sleep(2)

    # Получим имена всех продуктов в список после сортировки
    names_new = []
    product_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    for element in product_elements:
        name_text = element.text
        names_new.append(name_text)
    print(names_new)

    # Сравниваем отсортированный список с сайта со старым списком(отсортированным нами)
    assert names_new == sorted(names, key=lambda x: x.lower(), reverse=True)


@allure.feature("Тест входа под заблокированным пользователем")
@allure.story("Тест нахождения контейнера с ошибкой")
def test_login_lockedUser(driver):
    # Заходим на сайт и авторизуемся
    driver.get("https://www.saucedemo.com/")
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "user-name"))
    )
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys("locked_out_user")
    password_input.send_keys("secret_sauce")
    login_button.click()

    # Ищем контейнер ошибки
    element_selector = ".error-message-container.error"
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
    )

    # Получаем текст, содержащийся внутри селектора
    element_text = element.text
    # print(element_text)
    # Проверяем, что элемент найден и содержит ожидаемый текст
    expected_text = "Epic sadface: Sorry, this user has been locked out."
    assert element_text == expected_text, f"Текст элемента не соответствует ожидаемому: {element_text}"
