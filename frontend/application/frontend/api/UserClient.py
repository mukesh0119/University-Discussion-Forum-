# application/frontend/api/UserClient.py
import requests
from flask import session, request
from application import app

class UserClient:

	user_service = app.config['USER_SERVICE']

	@staticmethod
	def get_user():
		headers = {
		    'Authorization': 'Basic ' + session['user_api_key']
		}
		url = 'http://' + UserClient.user_service + '/api/user'
		response = requests.request(method="GET", url=url, headers=headers)
		if response.status_code == 401:
			return False
		user = response.json()
		return user

	@staticmethod
	def get_otheruser(user_id):
		url = 'http://' + UserClient.user_service + '/api/user/' + str(user_id)
		response = requests.request("GET", url=url)
		if response.status_code == 404:
			return None
		user = response.json()
		return user
		
	@staticmethod
	def does_exist(email):
		url = 'http://' + UserClient.user_service + '/api/user/' + email + '/exists'
		response = requests.request("GET", url=url)
		return response.status_code == 200

	@staticmethod
	def urn_exist(uni_number):
		url = 'http://' + UserClient.user_service + '/api/user/uni_number/' + uni_number + '/exists'
		response = requests.request("GET", url=url)
		return response.status_code == 200

	@staticmethod
	def phone_exist(phone_number):
		url = 'http://' + UserClient.user_service + '/api/user/phone_number/' + phone_number + '/exists'
		response = requests.request("GET", url=url)
		return response.status_code == 200

	@staticmethod
	def post_user_create(form):
		user = False
		payload = {
	        'email': form.email.data,
	        'password': form.password.data,
	        'first_name': form.first_name.data,
	        'last_name': form.last_name.data,
	        'phone_number': form.phone_number.data,
	        'uni_number': form.uni_number.data,
	        'user_role': form.user_role.data,
	        'image_url': form.image_url
	    }
		url = 'http://' + UserClient.user_service +'/api/user/create'
		response = requests.request("POST", url=url, data=payload)

		if response:
			user = response.json()
		return user

	@staticmethod
	def post_user_update(form):
		user = False
		payload = {
			'user_id':session['user']['id'],
			'image_url': form.image_url,
	        'first_name': form.first_name.data,
	        'last_name': form.last_name.data,
	        'phone_number': form.phone_number.data,
	        'user_role': form.user_role.data,   
	    }	
		url = 'http://' + UserClient.user_service +'/api/user/update'
		response = requests.request("POST", url=url, data=payload)

		if response:
			user = response.json()
		return user

	@staticmethod
	def post_login(form):
		user = False
		payload = {'email': form.email.data,
		    'password': form.password.data}
		    
		url = 'http://'+ UserClient.user_service +'/api/user/login'
		response = requests.request("POST", url=url, data=payload)

		if response:
			d = response.json()
			# print("This is response from user api: " + str(d))
			if d['api_key'] is not None:
				api_key = d['api_key']
			return api_key

		return None

	@staticmethod
	def post_logout():
		headers = {
		    'Authorization': 'Basic ' + session['user_api_key']
		}

		url = 'http://' + UserClient.user_service + '/api/user/logout'
		response = requests.request("POST", url=url, headers=headers)

		return response