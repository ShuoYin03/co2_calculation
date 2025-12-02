from locust import HttpUser, task, between
import random
import time

# Update or pass the host via CLI: e.g. --host=http://localhost:8000
# The app requires an API key in header `x-api-key` (see utils/security.py).
API_KEY = "MYXfWcOW5vBi86n1TaiL569bUIJt7MXA"

REGISTRATIONS = ["01/2019", "06/2020", "12/2018", "03/2021"]
ENERGIES = ["1", "2", "3", "8", "12"]

class CO2User(HttpUser):
    wait_time = between(0.5, 2)

    @task
    def calculate_tax(self):
        # randomize inputs to better approximate real usage
        registration = random.choice(REGISTRATIONS)
        power = random.randint(3, 200)
        emission = round(random.uniform(50, 250), 1)
        energy = random.choice(ENERGIES)
        weight = random.randint(800, 3500)
        region = str(random.randint(1, 95))
        price = round(random.uniform(5000, 80000), 2)

        payload = {
            "registration": registration,
            "power": power,
            "emission": emission,
            "energy": energy,
            "weight": weight,
            "region": region,
            "price": price
        }

        headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

        with self.client.post("/api/calculate-tax", json=payload, headers=headers, catch_response=True, name="POST /api/calculate-tax") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"status {response.status_code}: {response.text}")
