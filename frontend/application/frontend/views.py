# application/frontend/views.py
from flask_wtf import FlaskForm
import requests
from . import forms
from . import frontend_blueprint
from .. import login_manager
from .api.UserClient import UserClient
from .api.PostClient import PostClient
from password_strength import PasswordPolicy
from password_strength import PasswordStats
from flask import render_template, session, redirect, url_for, flash, request, abort, current_app
from flask_login import login_user, logout_user, login_required, current_user
import secrets
from PIL import Image
from flask import send_file
from os import environ, path

@login_manager.user_loader
def load_user(user_id):
    return None


policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1, 
    numbers=1, 
    strength=0.4)


@frontend_blueprint.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if len(session)>=4:
        return redirect(url_for('frontend.get_posts'))

    DOMAINS_ALLOWED = ['surrey.ac.uk']

    form = forms.RegistrationForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            # check email domain
            email = form.email.data
            uni_number = form.uni_number.data
            phone_number = form.phone_number.data

            email_domain = email.split('@')[-1]
            if email_domain not in DOMAINS_ALLOWED:
                flash("You need to register with @surrey.ac.uk domain.", 'error')
                return render_template('auth/signup.html', form=form)
            # check password strength
            password = form.password.data
            stats = PasswordStats(password)
            checkpolicy = policy.test(password)
            if stats.strength() < 0.4:
                flash("Password not strong enough. Avoid consecutive characters and easily guessed words.")
                return render_template('auth/signup.html', form=form)
            # Search for existing user
            mail = UserClient.does_exist(email)
            if mail:
                # Existing email found
                flash('Please try another email', 'error')
                return render_template('auth/signup.html', form=form)

            urn = False
            if uni_number != '':
                urn = UserClient.urn_exist(uni_number)
            if urn:
                # Existing urn found
                flash('Please try another URN', 'error')
                return render_template('auth/signup.html', form=form)

            phone = False
            if phone_number != '':
                phone = UserClient.phone_exist(phone_number)
            if phone:
                # Existing phone found
                flash('Please try another phone number', 'error')
                return render_template('auth/signup.html', form=form)

            else:
                # Attempt to create new user
                form.image_url = 'defaultpp.png'
                user = UserClient.post_user_create(form)
                if user:
                    flash('Thanks for registering, login to access home page', 'success')
                    return redirect(url_for('frontend.login_route'))
                else:
                    flash('Errorfound', 'error')
                    return render_template('auth/signup.html', form=form)
        else:
            flash('Error found', 'error')

    return render_template('auth/signup.html', form=form)


@frontend_blueprint.route('/login', methods=['GET', 'POST'])
def login_route():
    if len(session)>=4:
        return redirect(url_for('frontend.get_posts'))

    form = forms.LoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            api_key = UserClient.post_login(form)
            if api_key:
                session['user_api_key'] = api_key
                user = UserClient.get_user()
                session['user'] = user['result']

                flash('Welcome back, ' + user['result']['first_name'], 'success')
                return redirect(url_for('frontend.get_posts'))
            else:
                flash('Cannot login, check your email or password', 'error')
                return redirect(url_for('frontend.login_route'))

    return render_template('auth/login.html', form=form)


@frontend_blueprint.route('/', methods=['GET'])
@frontend_blueprint.route('/page/<int:page>', methods=['GET'])
def get_posts(page=1):

    if len(session)<4:
        return redirect(url_for('frontend.login_route'))

    categories = []
    image_urls = []

    per_page = 4
    offset = (page - 1) * per_page
    posts = PostClient.get_posts(per_page,offset)

    categories = ['activities','courses&modules','societies',
    'student_union','accommodation','transportation','lost&found','sale&rental','other'] 

    if posts == 404:
        if PostClient.get_posts(per_page,0) != 404:
            return redirect(url_for('frontend.get_posts'))
        elif page == 1:
            return render_template('forum/index.html',categories=categories, page=1, page_limit=False)
        else :
            return redirect(url_for('frontend.get_posts'))

    page_limit = True
    offset_ = (page) * per_page
    next_posts = PostClient.get_posts(per_page,offset_)
    if next_posts == 404:
        page_limit = False
    if len(posts) < per_page:
        page_limit = False

    for post in posts:
        user = UserClient.get_otheruser(post['user_id'])
        image_urls.append(user['image_url'])  

    return render_template('forum/index.html',
                           data=zip(posts,image_urls), categories=categories,page=page, page_limit=page_limit)


@frontend_blueprint.route('/category/<category>/', methods=['GET'])
@frontend_blueprint.route('/category/<category>/<int:page>', methods=['GET'])
def categories(category, page=1):
    if len(session)<4:
        return redirect(url_for('frontend.login_route'))

    image_urls = []
    per_page = 4
    offset = (page - 1) * per_page
    posts = PostClient.get_category_posts(category,per_page,offset)  

    if posts == 404:
        flash('None or more post found in the category', 'fail')
        return redirect(url_for('frontend.get_posts')) 

    page_limit = True
    offset_ = (page) * per_page
    next_posts = PostClient.get_category_posts(category,per_page,offset_)
    if next_posts == 404:
        page_limit = False
    if len(posts) < per_page:
        page_limit = False

    for post in posts:
            user = UserClient.get_otheruser(post['user_id'])
            image_urls.append(user['image_url'])

    categories = ['activities','courses&modules','societies',
    'student_union','accommodation','transportation','lost&found','sale&rental','other']   

    return render_template('forum/category.html',
                           data=zip(posts,image_urls), category=category, categories=categories,page=page, page_limit=page_limit)


@frontend_blueprint.route('/search/', methods=['GET','POST'])
@frontend_blueprint.route('/search/<int:page>', methods=['GET','POST'])
def search(page=1):
    if len(session)<4:
        return redirect(url_for('frontend.login_route'))

    form = forms.SearchForm(request.form)
    form_words = form.keywords.data

    if request.method == 'POST':
        session["words"] = form_words

    words = session.get('words', '')

    image_urls = []
    per_page = 4
    offset = (page - 1) * per_page
    posts = PostClient.get_search(words,per_page,offset)

    if posts == 404:
        flash('None or more result found', 'fail')
        return redirect(url_for('frontend.get_posts'))

    page_limit = True
    offset_ = (page) * per_page
    next_posts = PostClient.get_search(words,per_page,offset_)
    if next_posts == 404:
        page_limit = False
    if len(posts) < per_page:
        page_limit = False

    for post in posts:
        user = UserClient.get_otheruser(post['user_id'])
        image_urls.append(user['image_url']) 

    categories = ['activities','courses&modules','societies',
    'student_union','accommodation','transportation','lost&found','sale&rental','other']  

    return render_template('forum/search.html',
                           data=zip(posts,image_urls), words=words, categories=categories,page=page, page_limit=page_limit)


@frontend_blueprint.route('/weeklyhots/', methods=['GET','POST'])
@frontend_blueprint.route('/weeklyhots/<int:page>', methods=['GET','POST'])
def get_hot_posts(page=1):
    image_urls = []
    per_page = 4
    offset = (page - 1) * per_page
    posts = PostClient.get_hot_posts(per_page,offset)

    if page >= 4:
        return redirect(url_for('frontend.get_posts')) 

    if posts == 404:
        flash('No hot posts for last 7 days', 'fail')
        return redirect(url_for('frontend.get_posts')) 

    page_limit = True
    offset_ = (page) * per_page
    next_posts = PostClient.get_hot_posts(per_page,offset_)
    if next_posts == 404:
        page_limit = False
    if len(posts) < per_page:
        page_limit = False

    for post in posts:
            user = UserClient.get_otheruser(post['user_id'])
            image_urls.append(user['image_url'])

    categories = ['activities','courses&modules','societies',
    'student_union','accommodation','transportation','lost&found','sale&rental','other']   

    return render_template('forum/hotposts.html',
                           data=zip(posts,image_urls), categories=categories,page=page, page_limit=page_limit)


def save_post_image(image_file):
    random_hex = secrets.token_hex(8)
    _, file_ext = path.splitext(image_file.filename)
    picture_filename = random_hex + file_ext
    picture_path = path.join(current_app.root_path,
                             'static/images', picture_filename)
    output_size = (500, 500)
    pic = Image.open(image_file)
    pic.thumbnail(output_size)
    pic.save(picture_path)

    return picture_filename 


def save_user_image(image_file):
    random_hex = secrets.token_hex(8)
    _, file_ext = path.splitext(image_file.filename)
    picture_filename = random_hex + file_ext
    picture_path = path.join(current_app.root_path,
                             'static/images/users', picture_filename)
    output_size = (200, 200)
    pic = Image.open(image_file)
    pic.thumbnail(output_size)
    pic.save(picture_path)

    return picture_filename 


@frontend_blueprint.route('/post/images/users/<image_id>' , methods=['GET'])
@frontend_blueprint.route('/weeklyhots/images/users/<image_id>' , methods=['GET'])
@frontend_blueprint.route('/search/images/users/<image_id>' , methods=['GET'])
@frontend_blueprint.route('/page/images/users/<image_id>' , methods=['GET'])
@frontend_blueprint.route('/user/images/users/<image_id>' , methods=['GET'])
@frontend_blueprint.route('/images/users/<image_id>' , methods=['GET'])
def get_user_image(image_id):
    picture_path = path.join(current_app.root_path,
                             'static/images/users', image_id)

    return send_file(picture_path, mimetype='image/gif')


@frontend_blueprint.route('/post/images/<image_id>' , methods=['GET'])
@frontend_blueprint.route('/weeklyhots/static/images/<image_id>' , methods=['GET'])
@frontend_blueprint.route('/page/static/images/<image_id>' , methods=['GET'])
@frontend_blueprint.route('/search/static/images/<image_id>' , methods=['GET'])
def get_post_image(image_id):
    picture_path = path.join(current_app.root_path,
                             'static/images', image_id)
    
    return send_file(picture_path, mimetype='image/gif')


categories = ['activities','courses&modules','societies',
'student_union','accommodation','transportation','lost&found','sale&rental','other'] 
for category in categories:
    frontend_blueprint.add_url_rule(f"/category/{category}/images/users/<image_id>", view_func=get_user_image, methods=['GET'])
    frontend_blueprint.add_url_rule(f"/category/{category}/static/images/<image_id>", view_func=get_post_image, methods=['GET'])


@frontend_blueprint.route('/post/new', methods=['GET','POST'])
def create_post():
    if len(session)<4:
        return redirect(url_for('frontend.login_route'))
    form = forms.CreatePostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.image.data:
                post_image = save_post_image(form.image.data)
                form.image_url = post_image
            else:
                form.image_url = ''

            post = PostClient.create_post(form)
            if post:
                flash('Post created successfully', 'success')
                return redirect(url_for('frontend.get_posts', _external=True))
            else :
                flash('Post not successful', 'fail')
                return redirect(url_for('frontend.get_posts', _external=True))
    content = {
        'page_title': 'New',
        'form': form,
        'post': None
        }

    categories = ['activities','courses&modules','societies',
    'student_union','accommodation','transportation','lost&found','sale&rental','other']

    return render_template('forum/create_post.html', **content, categories=categories)


@frontend_blueprint.route('/post/<int:post_id>', methods=['GET','POST'])
def display_post(post_id):
    if len(session)<4:
        return redirect(url_for('frontend.login_route'))
    user_id = session['user']['id']
    response = PostClient.get_post(post_id)

    if response == 404:
        abort(404)

    post = response[0]
    post_owner = UserClient.get_otheruser(post['user_id'])

    comments = response[1:]
    comment_owners_images = []
    for comment in comments:
        comment_owner = UserClient.get_otheruser(comment['user_id'])
        comment_owners_images.append(comment_owner['image_url'])

    form = forms.CommentForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            comment = PostClient.create_comment(form, post_id)
            if comment:
                flash('Comment created successfully', 'success')
                return redirect(url_for('frontend.display_post', post_id=post_id))
            else:
                flash('Comment not successful', 'fail')
                return redirect(url_for('frontend.display_post', form=form, post_id=post_id))                

    content = {
        'post': post,
        'owner_image': post_owner['image_url'],
        'form': form,
        'current_user_id':user_id,
        'comments': zip(comments, comment_owners_images)
        }

    return render_template('forum/post.html', **content)


@frontend_blueprint.route('/post/<int:post_id>/<int:comment_id>/delete', methods=['GET', 'POST'])
def delete_comment(post_id,comment_id):
    if len(session)<4:
        return redirect(url_for('frontend.login_route'))

    comment = PostClient.get_comment(post_id,comment_id)

    if comment == 404:
        abort(404)

    comment_user_id = comment[0]['user_id']
    user_id = session['user']['id']

    if comment_user_id != user_id:
        abort(403)

    delete_comment = PostClient.delete_comment(post_id, comment_id)

    if delete_comment:
        flash(' Your comment has been deleted', 'success')
    else:
        flash(' Comment deletion not successful', 'fail')

    return redirect(url_for('frontend.display_post',post_id=post_id))


@frontend_blueprint.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
    if len(session)<4:
        return redirect(url_for('frontend.login_route'))

    post = PostClient.get_post(post_id)
    user_id = session['user']['id']

    if post == 404:
        abort(404)

    post_user_id = post[0]['user_id']

    if post_user_id != user_id:
        abort(403)

    delete_post = PostClient.delete_post(post_id)
    if delete_post:
        flash(' Your post has been deleted', 'success')
    else:
        flash(' Post deletion not successful', 'fail')

    return redirect(url_for('frontend.get_posts'))


@frontend_blueprint.route('/logout', methods=['GET'])
def logout():
    if len(session)<4:
        return redirect(url_for('frontend.login_route'))
    UserClient.post_logout()
    session.clear()
    return redirect(url_for('frontend.get_posts'))
    

@frontend_blueprint.route('/user/<int:user_id>', methods=['GET'])
def display_user(user_id):
    if len(session)<4:
        return redirect(url_for('frontend.login_route'))

    response = UserClient.get_otheruser(user_id)

    if response is None:
        flash('Profile is not detected', 'fail')
        return redirect(url_for('frontend.get_posts'))

    if user_id == int(session['user']['id']):
        return redirect(url_for('frontend.display_currentuser'))

    user_posts = []
    posts = PostClient.get_user_posts(response['id'])
    if posts == 404:
        posts = []

    content = {
    'name': response['full_name'],
    'email': response['email'],
    'role': response['user_role'],
    'image': response['image_url']
    }

    return render_template('forum/user.html', **content, posts=posts)


@frontend_blueprint.route('/user/profile', methods=['GET','POST'])
def display_currentuser():
    if len(session)<4:
        return redirect(url_for('frontend.login_route'))

    user_posts = []
    posts = PostClient.get_user_posts(session['user']['id'])
    if posts == 404:
        posts = []

    form = forms.AccountUpdateForm()
    if request.method == "POST":
        if form.validate_on_submit():
            
            if not any([form.image.data, form.first_name.data, form.last_name.data, form.phone_number.data, form.user_role.data]):
                flash('At least one field required', 'error')
                return redirect(url_for('frontend.display_currentuser'))

            if form.image.data:
                post_image = save_user_image(form.image.data)
                form.image_url = post_image
            else:
                form.image_url = 'defaultpp.png'

            phone_number = form.phone_number.data
            phone = False
            if phone_number != '':
                phone = UserClient.phone_exist(phone_number)
            if phone:
                # Existing phone found
                flash('Please try another phone number', 'error')
                return redirect(url_for('frontend.display_currentuser'))

            user = UserClient.post_user_update(form)
            if user:
                flash('Account information updated', 'success')
                updated_user=UserClient.get_otheruser(session['user']['id'])
                session['user'] = updated_user
                return redirect(url_for('frontend.display_currentuser'))
        else:
            flash('Account update failed', 'fail')
            return redirect(url_for('frontend.display_currentuser'))

    return render_template('forum/profile.html', user=session['user'], posts=posts, form=form)