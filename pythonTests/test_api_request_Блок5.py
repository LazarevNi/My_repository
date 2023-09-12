from api_request import ApiRequest

request_type = "GET"
payload = {"param1": "value1", "param2": "value2"}


def test_api_request_type():
    api_request = ApiRequest(request_type, payload)
    assert isinstance(api_request, ApiRequest)


def test_api_request_payload():
    api_request = ApiRequest(request_type, payload)
    assert api_request.payload == payload


def test_change_payload():
    api_request = ApiRequest(request_type, payload)
    new_payload = {"new_param": "new_value"}
    api_request.change_payload(new_payload)
    assert api_request.payload == new_payload
