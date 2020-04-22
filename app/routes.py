import requests, json
from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm, RegisterForm, SearchRestForm
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User, Post

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = SearchRestForm()
    if form.validate_on_submit():
        headers = app.config['HEADERS']
        endpoints = app.config['ENDPOINTS']
        location = form.location.data
        term = form.term.data
        query = f'''
        {{
            search(term: "{term}",
                    location: "{location}",
                    limit: 2) {{
                total
                business {{
                    name
                    id
                    url
                    review_count
                    rating
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
        result = json.loads(request.text)['data']['search']['business']
        return render_template('index.html', title='Homepage', form=form, result=result)
    return render_template('index.html', title='Homepage', form=form)

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
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
