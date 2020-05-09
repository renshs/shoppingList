from flask_login import current_user
from requests import get, post, delete

print(get('http://localhost:5000/api/users').json())
