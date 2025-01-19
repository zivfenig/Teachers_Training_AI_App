from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()  # Initialize the SQLAlchemy object
bcrypt = Bcrypt()  # Initialize Bcrypt for password hashing
login_manager = LoginManager()  # Manages user login sessions

# User model to store user accounts
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(50), unique=True, nullable=False)  # Unique username
    password = db.Column(db.String(200), nullable=False)  # Securely hashed password
    reports = db.relationship('Report', backref='user', lazy=True)  # Link to user reports

# Question model to store GeoGebra questions
class Question(db.Model): #### Modify this if needded ###
    id = db.Column(db.String(50), primary_key=True)  # GeoGebra ID
    question_text = db.Column(db.Text, nullable=False)  # Question content
    type = db.Column(db.String(10), nullable=False)  # 'open' or 'mcq' (multiple-choice)
    choices = db.Column(db.Text)  # JSON string for multiple-choice options

# Report model to track user answers
class Report(db.Model):  #### Modify this if needded ###
    id = db.Column(db.Integer, primary_key=True)  # Unique report ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User ID (foreign key)
    question_id = db.Column(db.String(50), db.ForeignKey('question.id'), nullable=False)  # Question ID
    answer = db.Column(db.Text, nullable=True)  # User's answer
    # correct = db.Column(db.Boolean, nullable=True)  # Indicates whether the answer was correct

# Flask-Login: Load the user for session management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))