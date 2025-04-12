import requests

BASE_URL = "http://localhost:3000/api"

# Test: Get all users
def test_get_all_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)

# Test: Get user by ID (valid ID)
def test_get_user_by_id_valid():
    user_id = 1  # Assuming this ID exists
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert body["id"] == user_id

# Test: Get user by ID (invalid ID)
def test_get_user_by_id_invalid():
    user_id = 9999  # Assuming this ID does not exist
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 404

# Test: Create a new user with valid data
def test_create_user_valid():
    payload = {
        "username": "test_user",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["username"] == payload["username"]

# Test: Create a new user with invalid data (missing email)
def test_create_user_invalid():
    payload = {"username": "invalid_user"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 400  # Missing email field

# Test: Update user (valid)
def test_update_user_valid():
    user_id = 1  # Assuming this ID exists
    payload = {
        "username": "updated_user",
        "email": "updated@example.com"
    }
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["username"] == payload["username"]

# Test: Delete user (valid)
def test_delete_user_valid():
    user_id = 1  # Assuming this ID exists
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200

# Test: Delete user (invalid ID)
def test_delete_user_invalid():
    user_id = 9999  # Assuming this ID does not exist
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 404
