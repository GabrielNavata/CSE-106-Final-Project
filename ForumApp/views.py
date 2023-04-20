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