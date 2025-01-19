from app import app
from models import db, Question, Answer

def delete_questions_in_range(start_id, end_id):
    with app.app_context():
        for question_id in range(start_id, end_id + 1):  # Loop through the specified range
            question = Question.query.get(question_id)
            if question:
                # Delete related answers first
                Answer.query.filter_by(question_id=question_id).delete()
                
                # Delete the question
                db.session.delete(question)
                print(f"Deleted question with id {question_id}")
            else:
                print(f"No question found with id {question_id}")
        
        db.session.commit()  # Commit the transaction after all deletions
        print(f"Deletion complete for IDs {start_id} to {end_id}")

if __name__ == "__main__":
    # Replace with your desired ID range
    start_id = 1
    end_id = 4
    delete_questions_in_range(start_id, end_id)