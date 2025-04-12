import requests

BASE_URL = "http://localhost:3000/api"

# Test: Get all rooms
def test_get_all_rooms():
    response = requests.get(f"{BASE_URL}/rooms")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)

# Test: Get rooms by hotel ID
def test_get_rooms_by_hotel_id():
    hotel_id = 1  # Assuming this hotel exists
    response = requests.get(f"{BASE_URL}/rooms/hotel/{hotel_id}")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)

# Test: Get available rooms by hotel ID
def test_get_available_rooms_by_hotel_id():
    hotel_id = 1  # Assuming this hotel exists
    response = requests.get(f"{BASE_URL}/rooms/hotel/{hotel_id}/available")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)

# Test: Create a new room (valid)
def test_create_room_valid():
    payload = {
        "hotelId": 1,
        "roomNumber": "101",
        "capacity": 2,
        "price": 100
    }
    response = requests.post(f"{BASE_URL}/rooms", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["roomNumber"] == payload["roomNumber"]

# Test: Update room (valid)
def test_update_room_valid():
    room_id = 1  # Assuming this room exists
    payload = {
        "roomNumber": "102",
        "capacity": 2,
        "price": 120
    }
    response = requests.put(f"{BASE_URL}/rooms/{room_id}", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["roomNumber"] == payload["roomNumber"]

# Test: Delete room (valid)
def test_delete_room_valid():
    room_id = 1  # Assuming this room exists
    response = requests.delete(f"{BASE_URL}/rooms/{room_id}")
    assert response.status_code == 200

# Test: Delete room (invalid ID)
def test_delete_room_invalid():
    room_id = 9999  # Assuming this ID does not exist
    response = requests.delete(f"{BASE_URL}/rooms/{room_id}")
    assert response.status_code == 404
