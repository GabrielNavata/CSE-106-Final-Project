#views
from . import db, app
from .models import *
from flask import *
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')