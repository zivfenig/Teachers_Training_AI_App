from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User, Question, Answer
from utils.nlp_utils import is_answer_correct
from sqlalchemy.sql import func
from sequence_logic import *
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/zivfenig/Teachers_training_application_V2/instance/teachers_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db.init_app(app)

# Default number of correct answers needed to level up
CORRECT_ANSWERS_TO_LEVEL_UP = 4

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=password, skill_level=2)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['skill_level'] = user.skill_level
            session['start_time'] = datetime.utcnow()  # Start time for the session
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('get_question'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/question', defaults={'question_id': None}, methods=['GET', 'POST'])
@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def get_question(question_id):
    if 'user_id' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    # Fetch the question based on user skill level
    if question_id is None:
        question = get_initial_question(user.skill_level)
        if not question:
            flash('No questions available for your skill level.', 'info')
            return redirect(url_for('home'))
        question_id = question.id
    else:
        question = Question.query.get_or_404(question_id)

    # Parse possible MCQ answers if the question is MCQ
    possible_answers = []
    if question.question_type == 'mcq' and question.possible_mcq_answers:
        possible_answers = question.possible_mcq_answers.split('|')

    if request.method == 'POST':
        user_answer = request.form['answer']
        correct_answer = question.correct_answer
        is_correct = is_answer_correct(user_answer, correct_answer)
        time_taken = float(request.form['time_taken'])
        geogebra_data = request.form.get('geogebra_data')

        # Save the answer
        new_answer = Answer(
            user_id=user.id,
            question_id=question.id,
            user_answer=user_answer,
            is_correct=is_correct,
            time_taken=time_taken,
            geogebra_data=geogebra_data
        )
        db.session.add(new_answer)

        # Check skill level upgrade
        if is_correct:
            leveled_up, remaining = check_and_upgrade_skill_level(user, CORRECT_ANSWERS_TO_LEVEL_UP)
            if leveled_up:
                flash('Correct! Leveling up to the next level.', 'success')
            else:
                flash(f'Correct! You need {remaining} more correct answers to level up.', 'success')
        else:
            flash('Incorrect. Try again.', 'danger')

        db.session.commit()
        return redirect(url_for('get_question'))

    # Get the next question
    next_question = get_next_question(question_id, user.skill_level)
    next_question_id = next_question.id if next_question else None

    return render_template(
        'question_detail.html',
        question=question,
        possible_answers=possible_answers,
        next_question_id=next_question_id
    )

@app.route('/save_user_answer/<int:question_id>', methods=['POST'])
def save_user_answer(question_id):
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "User not logged in"}), 403

    question = Question.query.get_or_404(question_id)
    user_id = session['user_id']
    data = request.get_json()
    user_answer = data.get('answer')
    explanation = data.get('explanation', '').strip()  # Get explanation, default to empty
    time_taken = data.get('time_taken', 0)
    geogebra_data = data.get('geogebra_data', '')
    snapshot = data.get('snapshot', '')  # Get snapshot data

    if not user_answer:
        return jsonify({"success": False, "error": "Answer is missing"}), 400

    # Determine if the question is MCQ
    is_mcq = question.question_type == 'mcq'

    # Correctness logic
    if is_mcq:
        is_correct = user_answer == question.correct_answer
        if explanation:  # Concatenate explanation if provided
            user_answer = f"{user_answer}  - Explanation: {explanation}"
    else:
        # Open-ended questions use NLP utility
        is_correct = bool(is_answer_correct(user_answer, question.correct_answer))

    # Save the answer with all required details
    answer = Answer(
        user_id=user_id,
        question_id=question_id,
        user_answer=user_answer,
        is_correct=is_correct,
        time_taken=time_taken,
        geogebra_data=geogebra_data,
        snapshot=snapshot  # Save snapshot if available
    )
    db.session.add(answer)
    db.session.commit()

    # Feedback message
    feedback = "Correct answer! Well done." if is_correct else "Incorrect answer. Please try again."

    return jsonify({"success": True, "correct": is_correct, "feedback": feedback})


@app.route('/next_question/<int:current_question_id>')
def get_next_question_route(current_question_id):
    user = User.query.get(session['user_id'])
    next_question = get_next_question(current_question_id, user.skill_level)
    next_question_id = next_question.id if next_question else None

    current_question = Question.query.get_or_404(current_question_id)
    return render_template(
        'question_detail.html',
        question=current_question,
        next_question_id=next_question_id
    )

if __name__ == '__main__':
    app.run(debug=True)
