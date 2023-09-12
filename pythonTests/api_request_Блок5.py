class ApiRequest:
    def __init__(self, request_type, payload):
        self.request_type = request_type
        self.payload = payload

    def change_payload(self, new_payload):
        self.payload = new_payload
