from models import db, Question
from app import app
def insert_questions():
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    example_questions = [
        {
            "applet_id": "qdsarepc",
            "question_type": "פתוחה דינאמית",
            "question_text": "דוגמא 6",
            "correct_answer": "צלעות נגדיות מקבילות זו לזו.צלעות נגדיות שוות זו לזו.",
            "thinking_level": "רמה 2-3",
            "subject": "תכונות המקבילית",
            "learning_goal": "לזהות תכונה נשמרת של מקבילית: צלעות נגדיות מקבילות.",
            "required_knowledge": "ישרים מקבילים.מרובעים.",
            "page_link" :"https://www.geogebra.org/M/qdsarepc"
        }
        
    ]
    with app.app_context():
        for question_data in example_questions:
            print(f"Adding question: {question_data['question_text']}")
            question = Question(**question_data)
            db.session.add(question)
        db.session.commit()
        print("Questions committed to the database.")
        
if __name__ == "__main__":
    insert_questions()