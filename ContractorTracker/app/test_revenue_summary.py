import requests

# Define the base URL
url = "http://127.0.0.1:5000/revenue/summary"

# Test cases
test_cases = [
    {"params": {"user_id": 1}, "description": "Filter by user ID"},
    {"params": {"start_date": "2025-01-01", "end_date": "2025-01-31"}, "description": "Filter by date range"},
    {"params": {"user_id": 1, "start_date": "2025-01-01", "end_date": "2025-01-31"}, "description": "Filter by both"}
]

# Run each test case
for test in test_cases:
    response = requests.get(url, params=test["params"])
    print(f"Test: {test['description']}")
    print("Response:", response.json())
    print()
