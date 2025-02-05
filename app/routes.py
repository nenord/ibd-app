import requests, json
from app import app, db
from datetime import datetime
from flask import render_template, url_for, redirect, flash, request, jsonify, session
from app.forms import LoginForm, RegisterForm, SearchRestForm, SearchPostsForm
from flask_login import login_required, current_user, login_user, logout_user
from app.models import User, Post, Rest, Counters
from werkzeug.urls import url_parse

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    admin_email = app.config['ADMIN_EMAIL']
    return render_template('index.html', title='Homepage', admin_email=admin_email)

@app.route('/rest_search', methods=['GET', 'POST'])
@login_required
def rest_search():
    form = SearchRestForm()
    if form.validate_on_submit():
        rest_count = Counters.query.filter_by(name='rest_count').first()
        if (rest_count is None):
            rest_count = Counters(name='rest_count', count=0)
            db.session.add(rest_count)
            db.session.commit()
        rest_count.count += 1
        db.session.commit()
        session['location'] = form.location.data
        session['term'] = form.term.data
        return redirect(url_for('rest_search'))
    if session.get('location') is not None:
        headers = json.loads(app.config['HEADERS'])
        endpoints = app.config['ENDPOINTS']
        query = f'''
        {{
            search(term: "{session.get('term')}",
                    location: "{session.get('location')}",
                    limit: 10) {{
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
        if request.status_code != 200:
            flash('Something went wrong with Yelp search, please try again.')
            session.pop('location', 'term')
            return redirect(url_for('rest_search'))
        check = json.loads(request.text)
        if 'errors' in check.keys():
            flash(check['errors'][0]['message'])
            session.pop('location', 'term')
            return redirect(url_for('rest_search'))
        result = check['data']['search']['business']
        if result == []:
            flash ('Yelp cannot find restaurants for that combination of inputs!')
            session.pop('location', 'term')
            return redirect(url_for('rest_search'))
        session.pop('location', 'term')
        return render_template('rest_search.html', title='Restaurant Search', form=form, result=result)
    return render_template('rest_search.html', title='Restaurant Search', form=form)

@app.route('/post_search', methods=['GET', 'POST'])
def post_search():
    form = SearchPostsForm()
    unique_cities = Rest.query.with_entities(Rest.city).distinct()
    cities = [i[0] for i in unique_cities]
    if form.validate_on_submit():
        post_count = Counters.query.filter_by(name='post_count').first()
        if (post_count is None):
            post_count = Counters(name='post_count', count=0)
            db.session.add(post_count)
            db.session.commit()
        post_count.count += 1
        db.session.commit()
        session['city'] = form.location.data.strip().title()
        return redirect(url_for('post_search'))
    if session.get('city') is not None:
        rests = Rest.query.filter_by(city=session.get('city')).order_by(Rest.timestamp.desc()).all()
        if rests == []:
            flash (f'There are no recommendations for {session.get("city")} yet, maybe you can make one!')
            session.pop('city')
            return redirect(url_for('post_search'))
        session.pop('city')
        return render_template('post_search.html', title='Posts Search', form=form, rests=rests)
    return render_template('post_search.html', title='Post Search', form=form, cities=cities)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash ('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

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
        flash ('Account registered successfully!')
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
    this_rest = Rest.query.filter_by(alias=alias).first()
    this_rest.timestamp = datetime.utcnow()
    post_text = request.form.get("post_text")
    post = Post(body=post_text, author=current_user, rest_id=this_rest.id)
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": request.form.get("name")})

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
