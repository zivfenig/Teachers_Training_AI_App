from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    skill_level = db.Column(db.Integer, nullable=False, default=2)
    correct_count = db.Column(db.Integer, default=0) 
    level_threshold = db.Column(db.Integer, default=1)  

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applet_id = db.Column(db.String(255), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    thinking_level = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(255))
    learning_goal = db.Column(db.Text)
    required_knowledge = db.Column(db.Text)
    question_type = db.Column(db.String(10), default='open') # 'open_ended' or 'mcq'
    possible_mcq_answers = db.Column(db.Text)  # Answers separated by '|'
    question_image_url = db.Column(db.String(255))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    tries = db.Column(db.Integer, default=1)
    time_taken = db.Column(db.Float, nullable=True)  
    geogebra_data = db.Column(db.Text, nullable=True)  # JSON to store GeoGebra applet data
    snapshot = db.Column(db.Text, nullable=True)
