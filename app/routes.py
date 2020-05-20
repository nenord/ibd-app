import requests, json
from app import app, db
from flask import render_template, url_for, redirect, flash, request, jsonify
from app.forms import LoginForm, RegisterForm, SearchRestForm, SearchPostsForm
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User, Post, Rest

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Homepage')

@app.route('/rest_search', methods=['GET', 'POST'])
@login_required
def rest_search():
    form = SearchRestForm()
    if form.validate_on_submit():
        headers = json.loads(app.config['HEADERS'])
        endpoints = app.config['ENDPOINTS']
        location = form.location.data
        term = form.term.data
        query = f'''
        {{
            search(term: "{term}",
                    location: "{location}",
                    limit: 5) {{
                total
                business {{
                    name
                    alias
                    url
                    review_count
                    rating
                    categories {{
                        alias
                    }}
                    location {{
                        address1
                        city
                        postal_code
                        country
                  }}
                }}
            }}
        }}
        '''
        request = requests.post(endpoints, json={'query': query}, headers=headers)
        check = json.loads(request.text)
        if 'errors' in check.keys():
            flash(check['errors'][0]['message'])
            return redirect(url_for('rest_search'))
        result = check['data']['search']['business']
        return render_template('rest_search.html', title='Restaurant Search', form=form, result=result)
    return render_template('rest_search.html', title='Restaurant Search', form=form)

@app.route('/post_search', methods=['GET', 'POST'])
def post_search():
    form = SearchPostsForm()
    if form.validate_on_submit():
        rests = Rest.query.filter_by(city=form.location.data.strip().capitalize()).all()
        if rests == []:
            flash (f'There are no recommendations for {form.location.data} yet, maybe you can make one!')
            return redirect(url_for('post_search'))
        return render_template('post_search.html', title='Posts Search', form=form, rests=rests)
    return render_template('post_search.html', title='Posts Search', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash ('Invalid name or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign-in', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    alias = request.form.get("alias")
    if (Rest.query.filter_by(alias=alias).first() is None):
        rest = Rest(name=request.form.get("name"), alias=alias, url=request.form.get("url"),
        categories=request.form.get("categories"), city=request.form.get("city"), address=request.form.get("address"),
        postal_code=request.form.get("postal_code"), country=request.form.get("country"),
        rating=request.form.get("rating"), review_count=request.form.get("review_count"))
        db.session.add(rest)
        db.session.commit()
    this_rest_id = Rest.query.filter_by(alias=alias).first()
    post_text = request.form.get("post_text")
    post = Post(body=post_text, author=current_user, rest_id=this_rest_id.id)
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": 'Your post has been added.'})

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
