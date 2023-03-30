from flask import Flask, render_template, request, redirect, url_for, flash, session,get_flashed_messages,make_response
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_mysqldb import MySQL
from models import db, User
from datetime import datetime
import urllib.parse
import yaml
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,template_folder='templates', static_folder='templates/static')
db_params = yaml.load(open('db.yaml'),Loader=yaml.FullLoader)
db_params['DB_PASSWORD'] = urllib.parse.quote_plus(db_params['DB_PASSWORD'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%(DB_USER)s:%(DB_PASSWORD)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s' % db_params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'insurance123'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db.init_app(app)
with app.app_context():
    db.create_all()

mysql = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            session['username'] = username
            return redirect(url_for('LandingPage'))
        else:
            flash('Invalid username or password', 'error')
            messages = get_flashed_messages()
            return render_template('login.html',messages=messages)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        dob = request.form['dob']
        phone = request.form['phone']
        email = request.form['email']
        
        # Check if username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('index'))
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Create new user object
        new_user = User(username=username, password=password_hash,
                        fname=fname, mname=mname, lname=lname, dob=dob,
                        phone=phone, email=email)
        
        # Add user to database
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered. Please login.', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html')
    
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    response = make_response(redirect(url_for('login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/LandingPage')
@login_required
def LandingPage():
    username = session['username']
    if username:
        response = make_response(render_template('LandingPage.html', username=username))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    else:
        return redirect(url_for('login'))

@app.route('/Insuranceprod')
@login_required
def Insuranceprod():
    username = session['username']
    if username:
        response = make_response(render_template('Insuranceprod.html', username=username))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    else:
        return redirect(url_for('login'))


@app.route('/Renew')
@login_required
def Renew():
    username = session['username']
    if username:
        response = make_response(render_template('Renew.html', username=username))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    else:
        return redirect(url_for('login'))

@app.route('/AboutUs')
@login_required
def AboutUs():
    username = session['username']
    if username:
        response = make_response(render_template('AboutUs.html', username=username))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    else:
        return redirect(url_for('login'))

@app.route('/ContactUs')    
@login_required
def ContactUs():
    username = session['username']
    if username:
        response = make_response(render_template('ContactUs.html', username=username))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    else:
        return redirect(url_for('login'))

@app.route('/profile')    
@login_required
def profile():
    username = session['username']
    if username:
        user = User.query.filter_by(username=username).first()
        personal_details=user.get_personal_details()
        response = make_response(render_template('Profile.html', username=username,personal_details=personal_details))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
    else:
        return redirect(url_for('login'))

@app.route('/Updateform', methods=['GET', 'POST'])
@login_required
def Updateform():
    username=session['username']
    if username:
        user = User.query.filter_by(username=username).first()
        personal_details=user.get_personal_details()
        if request.method=='POST':
            user = User.query.filter_by(username=username).first()
            user.fname = request.form['fname']
            user.mname = request.form['mname']
            user.lname = request.form['lname']
            user.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
            user.phone = request.form['phone']
            user.email = request.form['email']
            db.session.commit()
            flash('Your personal details have been updated successfully.')
            return redirect(url_for('Updateform'))
    response = make_response(render_template('Updateform.html', username=username,personal_details=personal_details))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response
        


if __name__ == '__main__':
    app.run(port=8080)
