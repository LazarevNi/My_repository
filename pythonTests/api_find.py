import json
import pytest
import requests
from pydantic import BaseModel
from typing import List, Optional

class Pet(BaseModel):
    id: Optional[int]
    name: Optional[str]
    photoUrls: Optional[List[str]]
    tags: Optional[List[dict]]
    status: Optional[str]


class TestAPI:
    @pytest.mark.test_find_by_status
    def test_find_by_status(self):
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