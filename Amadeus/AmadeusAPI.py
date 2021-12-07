import requests
import credentials

# https://developers.amadeus.com/self-service/category/air/api-doc/airport-nearest-relevant/api-reference

access_token = credentials.ACCESS_TOKEN
headers = {"Authorization": "Bearer " + access_token}
params = {
  "latitude": 38.7452,
  "longitude": -9.1604,
  "radius": 500
}

r = requests.get('https://test.api.amadeus.com/v1/reference-data/locations/airports', headers=headers, params=params)

print(r.text)     #Solo para imprimir
# print(r.json()) #Para procesar