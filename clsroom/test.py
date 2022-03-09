import requests
import json

for i in range(1, 15):
    data= {
    "account_id" : f"student{i}",
    "password" : "student",
    "email" : f"student{i}@gmail.com",
    "is_faculty": False
    }
    data = json.dumps(data)
    url = "http://localhost:8000/api/register"
    response = requests.post(url, data)
    print(response)
