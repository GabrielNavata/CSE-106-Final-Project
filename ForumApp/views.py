#views
from . import db, app
from .models import *
from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
def index():
    if (current_user.is_anonymous):
        return render_template('landing.html')    
    

    return render_template('index.html')

# Route for browsing page
@views.route('/browse', methods=['GET', 'POST'])
def browse():

    return render_template('browse.html')

# Route for individual posts
# change later to include the post id in the route
@views.route('/post', methods=['GET', 'POST'])
def post():

    return render_template('post.html')

# Route for creating posts
@views.route('/create', methods=['GET', 'POST'])
def create():

    return render_template('create.html')

# Route for editing a user's own account
@views.route('/account', methods=['GET', 'POST'])
def account():

    return render_template('account.html')

# Route for viewing a user profile
# change later to include the username 
@views.route('/profile', methods=['GET'])
def profile():

    return render_template('profile.html')
