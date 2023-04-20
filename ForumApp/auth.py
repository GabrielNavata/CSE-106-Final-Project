#auth
from flask import *
from . import db
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from .models import Users

auth = Blueprint('auth', __name__)

# Signup Route
@auth.route('/signup', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm_password')

        user = Users.query.filter_by(username = username).first()
        if user:
            flash('Username Already Exists', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 4:
            flash('Password must be at least 4 characters.', category='error')
        else:
            new_user = Users(username=username, password=generate_password_hash(password1, method='sha256'))

            db.session.add(new_user)

            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')

            return redirect(url_for('views.index'))


    return render_template("sign_up.html", user=current_user)

# Login Route
@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))      
            else:
                flash('Incorrect password, try again.', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('Username does not exist.', category='error')
            return redirect(url_for('auth.login'))

    elif request.method == 'GET':
        return render_template("login.html",user=current_user, )
    
# Logout Route
@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Log out successfull!', category='success')
  return redirect(url_for('auth.login'))