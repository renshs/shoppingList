from flask_login import current_user
from requests import get

print(get('http://localhost:5000/api/v2/purchases').json())
