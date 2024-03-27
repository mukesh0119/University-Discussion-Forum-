# application/post_api/api/UserClient.py
import requests
from application import app

class UserClient:

    user_service = app.config['USER_SERVICE']

    @staticmethod
    def get_username(user_id):
        url='http://'+ UserClient.user_service +'/api/' + str(user_id) + '/username'
        response = requests.request(method="GET", url=url)

        response = response.json()

        if response is None:
            return None
            
        return response

    @staticmethod
    def get_user(api_key):
        headers = {
            'Authorization': api_key
        }
        url='http://'+ UserClient.user_service +'/api/user'
        response = requests.request(method="GET", url=url, headers=headers)
        if response.status_code == 401:
            return False
        user = response.json()
        return user