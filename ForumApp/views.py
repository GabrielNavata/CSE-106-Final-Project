#views
from . import db, app
from .models import *
from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from sqlalchemy import or_
from sqlalchemy.orm import joinedload


views = Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
def index():
    if (current_user.is_anonymous):
        return render_template('landing.html')    
    

    return render_template('index.html')

# Route for browsing page
@views.route('/browse', methods=['GET', 'POST'])
def browse():
    # currently does not work with search function
    filter = request.args.get('filter', default='recent')
    
    if filter == 'views':
        sel = True
        posts = Posts.query.order_by(Posts.views.desc()).all()
    elif filter == 'recent':
        sel = False
        posts = Posts.query.order_by(Posts.timestamp.desc()).all()
    else:
        sel = False
        posts = Posts.query.all()

    return render_template('browse.html', posts=posts, sel=sel)



# Route for individual posts
@views.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Posts.query.get_or_404(post_id)

    if request.method == 'GET':
        # preventing view counter +1 if page is refeshed due to voting or deleting
        if not request.args.get('voted') and not request.args.get('comment_del'):
            post.views += 1
            db.session.commit()

    if request.method == 'POST':
        comment_content = request.form['comment']
        new_comment = Comments(content=comment_content, post_id=post_id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()

    return render_template('post.html', post=post)

# Route to handle upvotes and downvotes
@views.route('/votes/<int:post_id>/<int:comment_id>/<action>', methods=['GET', 'POST'])
@login_required
def comment_vote(post_id, comment_id, action):

    comment = Comments.query.filter_by(id = comment_id).first_or_404()
    votes = CommentVotes.query.filter_by(user = current_user, comment = comment).first()

    if votes:
        if votes.vote != bool(int(action)):
            votes.vote = bool(int(action))
            db.session.commit()
            flash('Your vote has been changed!', category='success')
            return redirect(url_for('views.post', post_id = post_id, voted=True))
        else:
            db.session.delete(votes)
            db.session.commit()
            flash('Your vote has been removed', category='success')
            return redirect(url_for('views.post', post_id = post_id, voted=True))
        
    vote = CommentVotes(user=current_user, comment=comment, vote = bool(int(action)))
    db.session.add(vote)
    db.session.commit()
    flash('Your vote has been made!', category='success')
    return redirect(url_for('views.post', post_id = post_id, voted=True))

# Route for deleting comments
@views.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):

    comment = Comments.query.options(joinedload(Comments.post)).filter_by(id=comment_id).first()

    # Check if the current user is the author of the comment
    if comment.user != current_user:
        flash("You can only delete your own comments.", category = 'warning')
        return redirect(url_for('views.post', post_id=comment.post.id))


    db.session.delete(comment)
    db.session.commit()
    flash('Your comment was deleted', category='success')

    return redirect(url_for('views.post', post_id=comment.post.id, comment_del=True))

# Route for deleting posts
@views.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Posts.query.filter_by(id=post_id).first_or_404()

    # Check if the current user is the author of the post
    if post.user != current_user:
        flash("You can only delete your own posts.", category='warning')
        return redirect(url_for('views.post', post_id=post.id))

    db.session.delete(post)
    db.session.commit()
    flash('Your post was deleted', category='success')

    return redirect(url_for('views.browse'))

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
        flash('Your post has been created!', category='success')
        return redirect(url_for('views.browse'))
    else:
        return render_template('create.html')

    

# Route for editing a user's own account
@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        current_password = request.form['current_password']

        if username:
            current_user.username = username

        if password and password == confirm_password:
            if check_password_hash(current_user.password, current_password):
                current_user.password = generate_password_hash(password)

        db.session.commit()
        flash('Your account has been updated!', category='success')
        return redirect(url_for('views.account'))

    return render_template('account.html')

# Route for viewing a user profile
@views.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):

    user = Users.query.get_or_404(user_id)
    posts = Posts.query.filter_by(user_id=user_id).all()


    return render_template('profile.html', user=user, posts=posts)

# Route for searching for posts on browse page
@views.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        search = request.form["search"]
        posts = Posts.query.filter(or_(Posts.content.contains(search), Posts.title.contains(search))).order_by(Posts.timestamp.desc()).all()
        if posts:
            return render_template("browse.html", posts = posts)
        else:
            return render_template("browse.html", posts = posts)   
                    
