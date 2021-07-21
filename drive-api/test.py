import math
import random

import requests

URL_BASE = 'http://localhost:5000'

data = requests.get(f'{URL_BASE}/').json()
print(data)

data = requests.post(f'{URL_BASE}/home').json()
print(data)

rnd = random.randint(0, 99999999999999999999999999)
data = requests.post(f'{URL_BASE}/product', json={
    'name': f'Product {rnd}',
    'description': f'This is Product {rnd}',
    'price': 250.00,
    'qty': 100
})
data.raise_for_status()

data = requests.get(f'{URL_BASE}/product')
data.raise_for_status()
print(data.json())

print(data.json())
