##################################################################
# Install locust using "pip install locust"
# How to run? 
# locust -f locustfile.py --host=http://localhost:3000
##################################################################

from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 5)  # User waits between 1 and 5 seconds between requests
    
    @task(1)
    def get_all_hotels(self):
        self.client.get("/api/hotels")
    
    @task(2)
    def create_hotel(self):
        self.client.post("/api/hotels", json={
            "name": "Test Hotel",
            "address": "Test Address",
            "city": "Test City",
            "country": "Test Country",
            "rating": 4
        })

    @task(3)
    def get_user(self):
        self.client.get("/api/users/1")

    @task(4)
    def create_user(self):
        self.client.post("/api/users", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890"
        })

    @task(5)
    def create_booking(self):
        self.client.post("/api/bookings", json={
            "user_id": 1,
            "room_id": 1,
            "check_in_date": "2025-04-12",
            "check_out_date": "2025-04-15"
        })
    
    # Add more tasks as needed for other endpoints
