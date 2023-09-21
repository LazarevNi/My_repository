import json
import pytest
import requests
from pydantic import BaseModel
from typing import List, Optional


# Создадим модель данных для тестовых данных
class Pet(BaseModel):
    id: Optional[int]
    name: Optional[str]
    photoUrls: Optional[List[str]]
    tags: Optional[List[dict]]
    status: Optional[str]


class TestPetAPI:

    @pytest.mark.create
    def test_create_pet(self):
        # POST-запрос для создания нового питомца
        pet_data = {
            "id": 1,
            "category": {
                "id": 1,
                "name": "Пудели"
            },
            "photoUrls": ["string"],
            "tags":[
                {
                "id": 2,
                "name": "string"
                }
                 ],
            "name": "Тузик",
            "status": "available"
        }
        response = requests.post("https://petstore.swagger.io/v2/pet", json=pet_data)

        # Проверка успешного создания питомца
        assert response.status_code == 200
        created_pet = Pet(**response.json())
        assert created_pet == Pet(**pet_data)

    @pytest.mark.edit
    def test_edit_pet(self):
        pet_data = {
            "id": 1,
            "category": {
                "id": 2,
                "name": "Пудели"
            },
            "photoUrls": ["string"],
            "tags": [
                {
                    "id": 3,
                    "name": "string"
                }
            ],
            "name": "Тузик",
            "status": "sold"
        }
        response = requests.put("https://petstore.swagger.io/v2/pet", json=pet_data)

        # Проверка успешного редактирования питомца
        assert response.status_code == 200
        edited_pet = Pet(**response.json())
        assert edited_pet == Pet(**pet_data)

    @pytest.mark.test_find_by_status
    def test_find_by_status_available(self):
        response = requests.get('https://petstore.swagger.io/v2/pet/findByStatus?status=available')

        assert response.status_code == 200  # Проверка успешного ответа (код 200 OK)
        pets_data = json.loads(response.text)  # Преобразование JSON-строки в объект Python

        # Проверка, что список питомцев не пустой
        assert pets_data, "Список питомцев пустой"

        for pet_data in pets_data:
            if "name" not in pet_data:
                continue
            pet = Pet(**pet_data)  # Создание экземпляра класса Pet для каждого питомца
            assert pet.status == 'available'  # Проверка, что статус питомца равен 'available'

    @pytest.mark.test_find_by_status
    def test_find_by_status_pending(self):
        response = requests.get('https://petstore.swagger.io/v2/pet/findByStatus?status=pending')

        assert response.status_code == 200  # Проверка успешного ответа (код 200 OK)
        pets_data = json.loads(response.text)  # Преобразование JSON-строки в объект Python

        # Проверка, что список питомцев не пустой
        assert pets_data, "Список питомцев пустой"

        for pet_data in pets_data:
            if "name" not in pet_data:
                continue
            pet = Pet(**pet_data)  # Создание экземпляра класса Pet для каждого питомца
            assert pet.status == 'pending'  # Проверка, что статус питомца равен 'pending'

    @pytest.mark.test_find_by_status
    def test_find_by_status_sold(self):
        response = requests.get('https://petstore.swagger.io/v2/pet/findByStatus?status=sold')

        assert response.status_code == 200  # Проверка успешного ответа (код 200 OK)
        pets_data = json.loads(response.text)  # Преобразование JSON-строки в объект Python

        # Проверка, что список питомцев не пустой
        assert pets_data, "Список питомцев пустой"

        for pet_data in pets_data:
            if "name" not in pet_data:
                continue
            pet = Pet(**pet_data)  # Создание экземпляра класса Pet для каждого питомца
            assert pet.status == 'sold'  # Проверка, что статус питомца равен 'sold'

    @pytest.mark.test_find_by_status
    @pytest.mark.parametrize("pet_id", [1])  # Параметризация для теста с разными значениями pet_id
    def test_get_pet_by_id(self, pet_id):
        # Отправляем GET-запрос для получения информации о питомце по заданному pet_id
        response = requests.get(f'https://petstore.swagger.io/v2/pet/{pet_id}')

        # Проверяем, что успешный запрос
        assert response.status_code == 200

        # записываем JSON-ответ в словарь
        pet_data = response.json()

        # Проверяем, что полученная информация соответствует ожиданиям
        assert pet_data['id'] == pet_id

    @pytest.mark.edit
    def test_update_pet_with_form(self):
        # Создаем данные для обновления питомца с помощью формы
        pet_id = 1
        name = "Новое имя питомца"
        status = "sold"

        # Создаем словарь с данными формы, чтобы передать их в запрос, можно без словаря
        data = {
            "name": name,
            "status": status
        }
        # Отправляем POST-запрос с данными формы
        response = requests.post(f'https://petstore.swagger.io/v2/pet/{pet_id}', data=data)

        # Проверка успешного ответа (код 200 OK)
        assert response.status_code == 200

        #Проверка, что данные были обновлены

        response = requests.get(f'https://petstore.swagger.io/v2/pet/{pet_id}')
        pet_data = response.json()
        assert pet_data['name'] == name
        assert pet_data['status'] == status

    @pytest.mark.edit
    def test_delete_pet(self):
        # Здесь мы указываем ID питомца, который мы хотим удалить
        pet_id = 1

        # Отправляем DELETE-запрос для удаления питомца с заданным ID
        response = requests.delete(f'https://petstore.swagger.io/v2/pet/{pet_id}')

        # Проверка успешного ответа (код 200 OK) после удаления
        assert response.status_code == 200

        #Проверка что питомец удален
        response = requests.get(f'https://petstore.swagger.io/v2/pet/{pet_id}')
        assert response.status_code == 404


