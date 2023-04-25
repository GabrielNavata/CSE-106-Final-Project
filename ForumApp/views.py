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
    posts = Posts.query.order_by(Posts.timestamp.desc()).all()

    return render_template('browse.html', posts=posts)

# Route for individual posts
# change later to include the post id in the route
@views.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Posts.query.get_or_404(post_id)
    post.views += 1
    db.session.commit()

    if request.method == 'POST':
        comment_content = request.form['comment']
        new_comment = Comments(content=comment_content, post_id=post_id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()

 

    return render_template('post.html', post=post)

@views.route('/votes/<int:post_id>/<int:comment_id>/<action>', methods=['GET', 'POST'])
@login_required
def comment_vote(post_id, comment_id, action):
    # comment = Comments.query.get_or_404(comment_id)
    comment = Comments.query.filter_by(id = comment_id).first_or_404()
    votes = CommentVotes.query.filter_by(user = current_user, comment = comment).first()

    # if action == 'like':
    #     comment_like = CommentLikes(liked=True, user_id=current_user.id, comment_id=comment.id)
    #     db.session.add(comment_like)
    # else:
    #     comment_like = CommentLikes.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
    #     db.session.delete(comment_like)
    if votes:
        if votes.vote != bool(int(action)):
            votes.vote = bool(int(action))
            db.session.commit()
            return redirect(url_for('views.post', post_id = post_id))
        else:
            flash('You already vote for this post')
            return redirect(url_for('views.post', post_id = post_id))
        
    vote = CommentVotes(user=current_user, comment=comment, vote = bool(int(action)))
    db.session.add(vote)
    db.session.commit()
    return redirect(url_for('views.post', post_id = post_id))




# Route for creating posts
@views.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = current_user.id
        category = request.form['category']
        
        post = Posts(title=title, content=content, user_id=user_id, category=category)
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('views.browse'))
    else:
        return render_template('create.html')

    

# Route for editing a user's own account
@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    return render_template('account.html')

# Route for viewing a user profile
# change later to include the username 
@views.route('/profile', methods=['GET'])
def profile():

    return render_template('profile.html')
