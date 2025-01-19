from sqlalchemy.sql import func
from models import Question, Answer

def get_initial_question(user_skill_level):
    """
    Get the first question for the user based on their skill level.
    :param user_skill_level: int
    :return: Question or None
    """
    return Question.query.filter(Question.thinking_level >= user_skill_level).order_by(func.random()).first()

def get_next_question(current_question_id, user_skill_level):
    """
    Get the next question for the user based on their skill level.
    :param current_question_id: int
    :param user_skill_level: int
    :return: Question or None
    """
    return Question.query.filter(Question.id > current_question_id, Question.thinking_level >= user_skill_level).order_by(Question.id).first()

def check_and_upgrade_skill_level(user, correct_answers_to_level_up):
    """
    Check if the user has answered enough questions correctly to level up.
    :param user: User object
    :param correct_answers_to_level_up: int
    :return: (bool, int) Whether leveled up and remaining correct answers needed
    """
    correct_answers_count = Answer.query.filter_by(
        user_id=user.id,
        is_correct=True
    ).join(Question).filter(Question.thinking_level == user.skill_level).count()

    if correct_answers_count >= correct_answers_to_level_up:
        user.skill_level = min(user.skill_level + 1, 5)  # Max skill level is 5
        return True, 0
    else:
        remaining = correct_answers_to_level_up - correct_answers_count
        return False, remaining