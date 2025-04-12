import requests

BASE_URL = "http://localhost:3000/api"

# Test: Get all hotels
def test_get_all_hotels():
    response = requests.get(f"{BASE_URL}/hotels")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)

# Test: Get hotel by ID (valid ID)
def test_get_hotel_by_id_valid():
    hotel_id = 1  # Assuming this ID exists
    response = requests.get(f"{BASE_URL}/hotels/{hotel_id}")
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert body["id"] == hotel_id

# Test: Get hotel by ID (invalid ID)
def test_get_hotel_by_id_invalid():
    hotel_id = 9999  # Assuming this ID does not exist
    response = requests.get(f"{BASE_URL}/hotels/{hotel_id}")
    assert response.status_code == 404

# Test: Create a new hotel with valid data
def test_create_hotel_valid():
    payload = {
        "name": "Test Hotel",
        "location": "Test City",
        "stars": 4
    }
    response = requests.post(f"{BASE_URL}/hotels", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["name"] == payload["name"]

# Test: Create a new hotel with missing data (edge case)
def test_create_hotel_invalid():
    payload = {"name": "Invalid Hotel"}
    response = requests.post(f"{BASE_URL}/hotels", json=payload)
    assert response.status_code == 400  # Bad request, missing location or stars

# Test: Update hotel (valid)
def test_update_hotel_valid():
    hotel_id = 1  # Assuming this ID exists
    payload = {
        "name": "Updated Hotel",
        "location": "Updated City",
        "stars": 5
    }
    response = requests.put(f"{BASE_URL}/hotels/{hotel_id}", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == payload["name"]

# Test: Delete hotel (valid)
def test_delete_hotel_valid():
    hotel_id = 1  # Assuming this ID exists
    response = requests.delete(f"{BASE_URL}/hotels/{hotel_id}")
    assert response.status_code == 200

# Test: Delete hotel (invalid ID)
def test_delete_hotel_invalid():
    hotel_id = 9999  # Assuming this ID does not exist
    response = requests.delete(f"{BASE_URL}/hotels/{hotel_id}")
    assert response.status_code == 404
