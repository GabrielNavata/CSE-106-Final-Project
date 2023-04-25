#models
from . import db
from datetime import datetime
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    users_comment_vote = db.relationship('CommentVotes', backref='author', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.username

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('posts', lazy=True))

    comments = db.relationship('Comments', backref='post', lazy=True)

    def formatted_timestamp(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')


    def __repr__(self):
        return '<Post %r>' % self.title
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('comments', lazy=True))

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    comment_votes = db.relationship('CommentVotes', backref='comment_votes', lazy=True)

    def get_vote_counts(self):
        upvotes = CommentVotes.query.filter_by(comment_id=self.id, vote=True).count()
        downvotes = CommentVotes.query.filter_by(comment_id=self.id, vote=False).count()
        return upvotes, downvotes
    
    def formatted_timestamp(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')

class CommentVotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('users_comment_votes', lazy=True))

    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    comment = db.relationship('Comments', backref=db.backref('all_comment_votes', lazy=True))

    def __repr__(self):
        if self.vote == True:
            vote = 'Up'
        else:
            vote = 'Down'
        return '<Vote - {}, from {} for {}>'.format(vote, self.user.username)




