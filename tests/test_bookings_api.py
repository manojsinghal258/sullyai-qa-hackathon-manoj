########################################
# Enhanced Booking API Tests with Invalid & Edge Cases
# pytest test_bookings_api.py -v
########################################
import requests
import pytest
import logging

# Constants
BASE_URL = "http://localhost:3000/api" # Replace with your actual base URL
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

# Test Context to store user, hotel, room, and booking data
test_context = {}
mock_user = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "phone": "9876543210"
}

mock_hotel = {
    "name": "Sunrise Inn",
    "address": "123 Sunrise Blvd",
    "city": "Sunnytown",
    "state": "CA",                # Optional but safe to include
    "country": "Sunnyland",
    "zipcode": "12345",           # Optional
    "rating": 5
}

mock_room = {
    "room_number": "505",
    "room_type": "Deluxe",
    "price_per_night": 180.0,
    "hotel_id": None,  # Will be filled after hotel creation
    "amenities": ["Wi-Fi", "Air Conditioning", "TV", "Mini Bar", "Balcony"]
}


# ----------- Helper Functions ----------- #

def create_user():
    logger.info("[Setup] Creating mock user")
    response = requests.post(f"{BASE_URL}/users", json=mock_user)
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    if response.status_code == 201:
        user_data = response.json()
        print(response.json())
        test_context["user_id"] = user_data['data']['id']
    else:
        pytest.fail(f"Failed to create user: {response.status_code}, {response.json()}")

def create_hotel():
    logger.info("[Setup] Creating mock hotel")
    response = requests.post(f"{BASE_URL}/hotels", json=mock_hotel)
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    if response.status_code == 201:
        hotel_data = response.json()
        test_context["hotel_id"] = hotel_data["id"]
    else:
        pytest.fail(f"Failed to create hotel: {response.status_code}, {response.json()}")

def create_room():
    logger.info("[Setup] Creating mock room")
    payload = {**mock_room, "hotelId": test_context["hotel_id"]}
    response = requests.post(f"{BASE_URL}/rooms", json=payload)
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    if response.status_code == 201:
        room_data = response.json()
        test_context["room_id"] = room_data["id"]
    else:
        pytest.fail(f"Failed to create room: {response.status_code}, {response.json()}")

def create_booking():
    logger.info("[Setup] Creating a valid booking")
    payload = {
        "userId": test_context["user_id"],
        "hotelId": test_context["hotel_id"],
        "roomId": test_context["room_id"],
        "check_in_date": "2025-04-10",
        "check_out_date": "2025-04-12"
    }
    response = requests.post(f"{BASE_URL}/bookings", json=payload)
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    if response.status_code == 201:
        booking_data = response.json()
        test_context["booking_id"] = booking_data["id"]
    else:
        pytest.fail(f"Failed to create booking: {response.status_code}, {response.json()}")

# ----------- Tests ----------- #

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    logger.info("\n[Setup] Creating mock user, hotel, and room")

    # Create User
    user_resp = requests.post(f"{BASE_URL}/users", json=mock_user)
    assert user_resp.status_code == 201, f"Failed to create user: {user_resp.text}"
    user_data = user_resp.json()
    logger.info(f"User created: {user_data}")
    user_id = user_data.get("id")
    assert user_id, f"No 'id' returned in user creation response: {user_data}"

    # Create Hotel
    hotel_resp = requests.post(f"{BASE_URL}/hotels", json=mock_hotel)
    assert hotel_resp.status_code == 201, f"Failed to create hotel: {hotel_resp.text}"
    hotel_data = hotel_resp.json()
    logger.info(f"Hotel created: {hotel_data}")
    hotel_id = hotel_data.get("id")
    assert hotel_id, f"No 'id' returned in hotel creation response: {hotel_data}"

    # Create Room
    room_payload = {**mock_room, "hotel_id": hotel_id}
    room_resp = requests.post(f"{BASE_URL}/rooms", json=room_payload)
    assert room_resp.status_code == 201, f"Failed to create room: {room_resp.text}"
    room_data = room_resp.json()
    logger.info(f"Room created: {room_data}")
    room_id = room_data.get("id")
    assert room_id, f"No 'id' returned in room creation response: {room_data}"

    test_context.update({
        "user_id": user_id,
        "hotel_id": hotel_id,
        "room_id": room_id
    })

    yield  # Run the tests

    logger.info("\n[Teardown] Deleting mock data")
    requests.delete(f"{BASE_URL}/rooms/{room_id}")
    requests.delete(f"{BASE_URL}/hotels/{hotel_id}")
    requests.delete(f"{BASE_URL}/users/{user_id}")



def test_get_rooms_by_hotel_id():
    logger.info("[Test] Get rooms by hotel ID")
    hotel_id = test_context["hotel_id"]
    response = requests.get(f"{BASE_URL}/rooms/hotel/{hotel_id}")
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert all("id" in room for room in body)

def test_create_booking_valid():
    logger.info("[Test] Create a valid booking")
    payload = {
        "userId": test_context["user_id"],
        "hotelId": test_context["hotel_id"],
        "roomId": test_context["room_id"],
        "check_in_date": "2025-04-10",
        "check_out_date": "2025-04-12"
    }
    response = requests.post(f"{BASE_URL}/bookings", json=payload)
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    test_context["booking_id"] = body["id"]

def test_get_bookings_by_user_id():
    logger.info("[Test] Get bookings by user ID")
    user_id = test_context["user_id"]
    response = requests.get(f"{BASE_URL}/bookings/user/{user_id}")
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)

def test_cancel_booking_valid():
    logger.info("[Test] Cancel booking")
    booking_id = test_context["booking_id"]
    response = requests.patch(f"{BASE_URL}/bookings/{booking_id}/cancel")
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 200

def test_delete_booking_valid():
    logger.info("[Test] Delete booking")
    booking_id = test_context["booking_id"]
    response = requests.delete(f"{BASE_URL}/bookings/{booking_id}")
    logger.info(f"Status Code: {response.status_code}")
    assert response.status_code == 200

# Edge Cases

def test_create_booking_invalid_room():
    logger.info("[Test] Create booking with invalid room")
    payload = {
        "userId": test_context["user_id"],
        "hotelId": test_context["hotel_id"],
        "roomId": 9999,  # Invalid room ID
        "check_in_date": "2025-04-10",
        "check_out_date": "2025-04-12"
    }
    response = requests.post(f"{BASE_URL}/bookings", json=payload)
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 400  # Bad Request

def test_create_booking_missing_user():
    logger.info("[Test] Create booking with missing userId")
    payload = {
        "hotelId": test_context["hotel_id"],
        "roomId": test_context["room_id"],
        "check_in_date": "2025-04-10",
        "check_out_date": "2025-04-12"
    }
    response = requests.post(f"{BASE_URL}/bookings", json=payload)
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 400  # Bad Request

def test_get_bookings_by_invalid_user_id():
    logger.info("[Test] Get bookings by invalid user ID")
    invalid_user_id = 9999  # Non-existing user ID
    response = requests.get(f"{BASE_URL}/bookings/user/{invalid_user_id}")
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 404  # Not Found

def test_cancel_booking_invalid():
    logger.info("[Test] Cancel booking for non-existing booking ID")
    response = requests.patch(f"{BASE_URL}/bookings/9999/cancel")
    logger.info(f"Status Code: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 404  # Not Found

def test_delete_booking_invalid():
    logger.info("[Test] Delete booking for non-existing booking ID")
    response = requests.delete(f"{BASE_URL}/bookings/9999")
    logger.info(f"Status Code: {response.status_code}")
    assert response.status_code == 404  # Not Found
