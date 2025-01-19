from sqlalchemy.sql import text
from app import app
from models import db

def add_page_link_column():
    with app.app_context():
        try:
            # Check the existing columns in the questions table
            result = db.session.execute(text("PRAGMA table_info(questions)"))
            columns = [row[1] for row in result]  # Extract column names
            
            if 'page_link' not in columns:
                # Add the new column if it doesn't exist
                db.session.execute(text("ALTER TABLE questions ADD COLUMN page_link TEXT"))
                db.session.commit()
                print("Column 'page_link' added successfully.")
            else:
                print("Column 'page_link' already exists in the 'questions' table.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Run the function
if __name__ == "__main__":
    add_page_link_column()