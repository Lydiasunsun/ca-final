from flask import Flask, render_template, session, redirect, url_for, g, request
from flask_session import Session
from database import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, InsertForm, DeleteForm, EncryptForm
# , CheckoutForm, GreetingForm
from functools import wraps
from datetime import datetime, date

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config['SECRET_KEY'] = 'this-is-my-secret-key'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.before_request
def logged_in_user():
    g.user = session.get('user_id', None)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return view(*args, **kwargs)
    return wrapped_view


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['Get', 'POST'])
def register():  # 不可以写 def RegistrationForm()
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data

        db = get_db()
        clashing_user = db.execute(
            '''SELECT * FROM users WHERE user_id =?;''', (user_id,)).fetchone()  # clashing_gig 是指由一组内容的dictionary。 因为fetchone. 而当是fetchall 的时候是有多个内容的dictionary。
        if clashing_user is not None:
            form.user_id.errors.append('User id clashes with another')
        else:
            db.execute('''INSERT INTO users(user_id,password) VALUES(?,?);''',
                       (user_id, generate_password_hash((password))))  # 这里的gigs 是来源于schema.sql的定义
            db.commit()  # 这一行是为了更新的内容显示在结果中
            message = 'New gig inserted successfully'
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        possible_clashing_user = db.execute(
            '''SELECT * FROM users WHERE user_id = ?''', (user_id,)).fetchone()  # 加密过的密码被从数据库中取出
        if possible_clashing_user is None:
            form.user_id.errors.append('No such user!')
            return redirect(url_for('register'))
        elif not check_password_hash(possible_clashing_user['password'], password):
            form.password.errors.append('Incorrect password')
        else:  # 用户名存在且密码正确之后的下一步
            session.clear()
            session['user_id'] = user_id
            next_page = request.args.get('next')
            if not next_page:
                next_page = url_for('index')
            return redirect(next_page)  # ???
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/activities')
def activities():
    db = get_db()
    activities = db.execute('''SELECT * FROM activities;''').fetchall()
    return render_template('activities.html', activities=activities)


@app.route('/activity/<int:activity_id>')
def activity(activity_id):
    db = get_db()
    activity = db.execute(
        '''SELECT * FROM activities WHERE activity_id=?;''', (activity_id,)).fetchone()
    return render_template('activity.html', activity=activity)
    # 错误  wine = db.execute('''SELECT * FROM wines;''').fetchone()
    # 错误  wine_id 要在第一行def中先定义


@app.route('/account')
@login_required
def account():
    if 'account' not in session:   # what is a session, how does a  in session? session is a dictionary
        session['account'] = {}
    names = {}
    scores = {}
    db = get_db()
    for activity_id in session['account']:
        activity = db.execute(
            '''SELECT * FROM activities WHERE activity_id=?;''', (activity_id,)).fetchone()  # is this wine_id from user input or from for loop?
        name = activity['name']
        names[activity_id] = name
        score = activity['score']
        scores[activity_id] = score
    return render_template('account.html', account=session['account'], names=names, scores=scores)


# @app.route('/checkout', methods=['Get', 'POST'])
# def checkout():
#     form = CheckoutForm()
#     if form.validate_on_submit():
#         return render_template('sum.html', form=form, checkout=checkout)


# why there is a route but no html?


@app.route('/add_to_account/<int:activity_id>')
# why need to put wine_id here? because in the route,so need to say it.
@login_required
def add_to_account(activity_id):
    if 'account' not in session:
        session['account'] = {}
    # why didn't define wine_id in advance?
    if activity_id not in session['account']:
        session['account'][activity_id] = 1
    else:
        session['account'][activity_id] = session['account'][activity_id]+1
    return redirect(url_for('account'))


# @app.route('/ delete_in_account)
# # why need to put wine_id here? because in the route,so need to say it.
# @login_required
# def delete_in_account():
#     db = get_db()
#     for activity_id in session:
#         activity = db.execute(
#             '''SELECT * FROM activities WHERE activity_id=?;''', (activity_id,)).fetchone()

#     session['account'][activity_id] = session['account'][activity_id]-1
#     return redirect(url_for('account'))


@app.route('/insert_activities', methods=['GET', 'post'])
def insert_activities():
    form = InsertForm()
    message = ''
    if form.validate_on_submit():
        name = form.name.data
        score = int(form.score.data)
        description = form.description.data
        comment = form.comment.data
        db = get_db()
        db.execute('''INSERT INTO activities (name,score,description,comment) VALUES(?,?,?,?);''',
                   (name, score, description, comment))
        db.commit()
        message = 'New currency/activity created!'
    return render_template('insert_activities.html', form=form, message=message)


@app.route('/empty')
def empty():
    session['account'] = {}

    return redirect(url_for('account'))


# @app.route('/delete/<int:activity_id>', methods=['GET', 'POST'])
# def delete():
#     form = DeleteForm()
#     message = ''
#     if form.validate_on_submit():
#         delete = form.delete.data
#         db = get_db()
#         db.execute('''


# @app.route('/delete/<int:activity_id>', methods=['GEt', 'POST'])
# def delete(activity_id):
#     form = DeleteForm()
#     activity_to_delete = activities.query.get_or_404(activity_id)
#     try:
#         db.delete(activity_id)
#         db.commit()
#         return render_template('insert_activities.html', form=form, message='Deleted!', activity_id=activity_id)
#     except:
#         pass
# form = DeleteForm()
# message = ''
# if form.validate_on_submit():
#     db = get_db()
#     db.execute(
#         '''Delete * from activities where activity_id=?;''', (activity_id))
#     db.commit()
#     message = 'Deleted!'
# return render_template('insert_activities.html', form=form, message=message)
# @app.route('/name/<name>', methods=['Get', 'POST'])
# def name(name):
#     form = GreetingForm()
#     if form.validate_on_submit():
# return render_template('name.html', form=form, name=name)
# @app.route('/weather', methods=["GET", "POST"])
# def weather():
#     form = WeatherForm()
#     weatherData = ''
#     error = 0
#     cityName = ''
#     if form.validate_on_submit:
#         cityName = form.cityName.data
#         if cityName:
#             weatherApiKey = 'e0f6dac5a614708ae4bc38aaedf5d2d7'
#             url = "https://api.openweathermap.org/data/2.5/weather?q=" +\
#                 cityName+"&appid=" + weatherApiKey
#             url = "https://api.openweathermap.org/data/2.5/weather?q=?", (
#                 cityName,)+"&appid=?", (weatherApiKey,)
#             print(url)
#             weatherData = requests.get(url).json()
#         else:
#             error = 1
#     return render_template('index.html', weatherData=weatherData, cityName=cityName, error=error)
