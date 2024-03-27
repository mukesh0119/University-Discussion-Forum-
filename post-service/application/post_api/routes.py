# application/post_api/routes.py
from flask import jsonify, request, make_response, abort
from . import post_api_blueprint
from .. import db
from ..models import Post, Comment
from .api.UserClient import UserClient
from datetime import datetime, timedelta
from sqlalchemy import desc, func

@post_api_blueprint.route('/api/posts/<int:per_page>/<int:offset>', methods=['GET'])
def get_posts(per_page,offset):
    data = []
    for row in Post.query.order_by(Post.date_added.desc()).offset(offset).limit(per_page).all():
        data.append(row.to_json())

    if data == []:
        abort(404) 

    response = jsonify(data)
    return response

@post_api_blueprint.route('/api/hotposts/<int:per_page>/<int:offset>', methods=['GET'])
def get_hot_posts(per_page,offset):
    data = []

    today = datetime.utcnow()
    one_week_ago = today - timedelta(days=7)

    if offset == 8:
        for row in Post.query.join(Post.comments).filter(Post.date_added >= one_week_ago).group_by(Post.id).order_by(desc(func.count(Comment.id))).offset(offset).limit(per_page)[:2]:
            data.append(row.to_json())
    else:
        for row in Post.query.join(Post.comments).filter(Post.date_added >= one_week_ago).group_by(Post.id).order_by(desc(func.count(Comment.id))).offset(offset).limit(per_page).all():
            data.append(row.to_json())

    if data == []:
        abort(404) 

    response = jsonify(data)
    return response

@post_api_blueprint.route('/api/posts/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    data = []
    for row in Post.query.filter_by(user_id=user_id).order_by(Post.date_added.desc()).all():
        data.append(row.to_json())
    if data == []:
        abort(404) 

    response = jsonify(data)
    return response

@post_api_blueprint.route('/api/posts/<category>/<int:per_page>/<int:offset>', methods=['GET'])
def get_category_posts(category,per_page,offset):
    data = []
    for row in Post.query.filter_by(category=category).order_by(Post.date_added.desc()).offset(offset).limit(per_page).all():
        data.append(row.to_json())

    if data == []:
        abort(404) 

    response = jsonify(data)
    return response

@post_api_blueprint.route('/api/search/<query>/<int:per_page>/<int:offset>', methods=['GET'])
def get_search(query,per_page,offset):
    responses = []
    query = query.replace(" ", "%")

    for row in Post.query.filter(Post.content.like('%'+query+'%')).order_by(Post.date_added.desc()).offset(offset).limit(per_page).all():
        responses.append(row.to_json())

    if responses == []:
        abort(404) 

    response = jsonify(responses)
    return response


@post_api_blueprint.route('/api/<int:post_id>', methods=['GET'])
def get_post(post_id):
    responses = []

    post = Post.query.get_or_404(post_id)
    responses.append(post.to_json())

    for row in Comment.query.filter(Comment.post_id == post_id).all():
        responses.append(row.to_json())

    if responses == []:
        abort(404)    

    response = jsonify(responses)

    return response

@post_api_blueprint.route('/api/comments', methods=['GET'])
def get_comments():
    data = []
    for row in Comment.query.all():
        data.append(row.to_json())

    if data == []:
        abort(404)  

    response = jsonify(data)
    return response

@post_api_blueprint.route('/api/<int:post_id>/<int:comment_id>', methods=['GET'])
def get_comment(post_id,comment_id):
    comment_response = []

    comment = Comment.query.filter(Comment.post_id == post_id,
        Comment.id == comment_id).first() 

    if comment is None:
        abort(404)

    comment_response.append(comment.to_json()) 

    response = jsonify(comment_response)

    return response

@post_api_blueprint.route('/api/new-post', methods=['POST'])
# @login_required
def post_newpost():

    user_response = UserClient.get_user(request.form['user_api'])
    user = user_response['result']
    u_id = user['id']
    u_name = user['full_name']

    title = request.form['title']
    category = request.form['category']
    content = request.form['content']
    image_url = request.form['image']

    post = Post()
    post.user_id = u_id
    post.user_name = u_name
    post.title = title
    post.category = category
    post.content = content
    post.image_url = image_url

    db.session.add(post)
    db.session.commit()

    response = jsonify({'message': 'Post added', 'result': post.to_json()})

    return response

@post_api_blueprint.route('/api/<int:post_id>/delete', methods=['GET','POST'])
# @login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    response = jsonify({'message': 'Post deleted'})

    return response

@post_api_blueprint.route('/api/new-comment', methods=['POST'])
# @login_required
def post_comment():

    user_response = UserClient.get_user(request.form['user_api'])
    user = user_response['result']
    u_id = user['id']
    u_name = user['full_name']

    content = request.form['content']
    post_id = request.form['post_id']

    comment = Comment()
    comment.user_id = u_id
    comment.user_name = u_name
    comment.post_id = post_id
    comment.content = content

    db.session.add(comment)
    db.session.commit()

    response = jsonify({'message': 'Comment added', 'result': comment.to_json()})

    return response


@post_api_blueprint.route('/api/<int:post_id>/<int:comment_id>/delete', methods=['GET','POST'])
# @login_required
def delete_comment(post_id,comment_id): 
 
    comment = Comment.query.filter(Comment.post_id == post_id,
        Comment.id == comment_id).first()

    db.session.delete(comment)
    db.session.commit()

    response = jsonify({'message': 'Comment deleted'})

    return response
