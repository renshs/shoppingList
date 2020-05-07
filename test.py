from flask_login import current_user
from requests import get, post, delete

print(get('http://localhost:5000/api/purchases/5').json())


# print(post('http://localhost:5000/api/purchases',
#            json={'title': 'Яблоко',
#                  'content': 'Красное',
#                  'user_id': 1,
#                  'count': 1}).json())