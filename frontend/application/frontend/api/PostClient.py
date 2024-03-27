# application/frontend/api/PostClient.py
import requests
from flask import session, request
from application import app


class PostClient:

    post_service = app.config['POST_SERVICE']

    def get_posts(per_page,offset):        
        url = 'http://' + PostClient.post_service + '/api/posts/' + str(per_page) + '/' + str(offset)
        response = requests.request(method="GET", url=url)

        if response.status_code == 404:
            return response.status_code
            
        response = response.json()

        return response

    def get_hot_posts(per_page,offset):        
        url = 'http://' + PostClient.post_service + '/api/hotposts/' + str(per_page) + '/' + str(offset)
        response = requests.request(method="GET", url=url)

        if response.status_code == 404:
            return response.status_code
            
        response = response.json()

        return response

    def get_category_posts(category,per_page,offset):        
        url = 'http://' + PostClient.post_service + '/api/posts/'+ str(category) + '/' + str(per_page) + '/' + str(offset)
        response = requests.request(method="GET", url=url)

        if response.status_code == 404:
            return response.status_code
            
        response = response.json()

        return response

    def get_user_posts(user_id):        
        url = 'http://' + PostClient.post_service + '/api/posts/'+ str(user_id)
        response = requests.request(method="GET", url=url)

        if response.status_code == 404:
            return response.status_code
            
        response = response.json()

        return response

    def get_post(post_id):
        url = 'http://' + PostClient.post_service  + '/api/' + str(post_id)
        response = requests.request(method="GET", url=url)

        if response.status_code == 404:
            return response.status_code

        response = response.json()

        return response

    def get_search(query,per_page,offset):
        url = 'http://' + PostClient.post_service  + '/api/search/' + str(query) + '/' + str(per_page) + '/' + str(offset)
        response = requests.request(method="GET", url=url)

        if response.status_code == 404:
            return response.status_code

        response = response.json()

        return response

    def get_comment(post_id, comment_id):
        url = 'http://' + PostClient.post_service + '/api/' + str(post_id) + '/' + str(comment_id)
        response = requests.request(method="GET", url=url)

        if response.status_code == 404:
            return response.status_code

        response = response.json()

        return response

    def create_post(form):

        payload = {'title':form.title.data, 'category':form.category.data,
                        'content':form.content.data, 'image':form.image_url, 'user_api':session['user_api_key']}

        url = 'http://' + PostClient.post_service + '/api/new-post'
        response = requests.request(method="POST", url=url, data=payload)

        if response:
            return response

    def delete_post(post_id):

        url = 'http://'+ PostClient.post_service + '/api/' + str(post_id) + '/delete'
        response = requests.request(method="POST", url=url)

        if response:
            return response

    def create_comment(form, post_id):
        payload = {'content':form.content.data, 'user_api':session['user_api_key'], 
                'post_id':post_id}

        url = 'http://' + PostClient.post_service + '/api/new-comment'
        response = requests.request(method="POST", url=url, data=payload)

        if response:
            return response

    def delete_comment(post_id,comment_id):

        url = 'http://' + PostClient.post_service + '/api/' + str(post_id) + '/' + str(comment_id) + '/delete'
        response = requests.request(method="POST", url=url)

        if response:
            return response
