##################################################################
# How to run? 
# python performance_test.py
##################################################################

import requests
import time
import json

BASE_URL = "http://localhost:3000"  # Adjust as needed

def measure_response_time(method, endpoint, payload=None, max_response_time=2.0):
    url = f"{BASE_URL}{endpoint}"
    start_time = time.time()
    
    if method == "GET":
        response = requests.get(url)
    elif method == "POST":
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
    else:
        raise ValueError("Unsupported HTTP method")

    end_time = time.time()
    duration = end_time - start_time

    print(f"[{method}] {endpoint} → {response.status_code} in {duration:.3f}s")

    assert response.status_code == 200 or response.status_code == 201, f"Failed {method} {endpoint}"
    assert duration <= max_response_time, f"Slow response for {endpoint}: {duration:.3f}s"

    return response

# --- GET Tests ---
def test_get_all_hotels():
    measure_response_time("GET", "/api/hotels")

def test_get_hotel_by_id():
    measure_response_time("GET", "/api/hotels/1")

def test_get_all_users():
    measure_response_time("GET", "/api/users")

def test_get_user_by_id():
    measure_response_time("GET", "/api/users/1")

def test_get_all_rooms():
    measure_response_time("GET", "/api/rooms")

def test_get_room_by_id():
    measure_response_time("GET", "/api/rooms/1")

def test_get_all_bookings():
    measure_response_time("GET", "/api/bookings")

def test_get_booking_by_id():
    measure_response_time("GET", "/api/bookings/1")

# --- POST Tests ---
def test_post_user():
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone": "9998887777"
    }
    measure_response_time("POST", "/api/users", payload)

def test_post_hotel():
    payload = {
        "name": "Performance Inn",
        "address": "123 Speed Lane",
        "city": "Fastville",
        "country": "Quickland",
        "rating": 4
    }
    measure_response_time("POST", "/api/hotels", payload)

def test_post_booking():
    payload = {
        "user_id": 1,
        "room_id": 1,
        "check_in_date": "2025-04-12",
        "check_out_date": "2025-04-14"
    }
    measure_response_time("POST", "/api/bookings", payload)

# --- Run All Tests ---
def run_performance_tests():
    print("\n--- Running Performance Tests ---\n")
    
    test_get_all_hotels()
    test_get_hotel_by_id()
    test_get_all_users()
    test_get_user_by_id()
    test_get_all_rooms()
    test_get_room_by_id()
    test_get_all_bookings()
    test_get_booking_by_id()

    print("\n--- Testing POST Performance ---\n")
    test_post_user()
    test_post_hotel()
    test_post_booking()
    
    print("\n✅ All performance tests passed!")

if __name__ == "__main__":
    run_performance_tests()
