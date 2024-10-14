import requests

endpoints='http://localhost:8000/carlist/display/'
response=requests.get(endpoints)
print(response.json())
print(response.status_code)