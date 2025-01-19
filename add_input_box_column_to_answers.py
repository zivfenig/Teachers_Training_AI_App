from app import app, db
from sqlalchemy.sql import text

def add_input_box_column():
    try:
        with app.app_context():  # Ensure the application context is active
            with db.engine.connect() as connection:
                # Check if the column already exists
                result = connection.execute(text("PRAGMA table_info(answers);"))
                columns = [row[1] for row in result]  # Use tuple index 1 for column names
                
                if 'input_box_name' not in columns:
                    # Add the new column to the table
                    connection.execute(
                        text("ALTER TABLE answers ADD COLUMN input_box_name TEXT;")
                    )
                    print("Column 'input_box_name' added successfully to 'answers' table.")
                else:
                    print("Column 'input_box_name' already exists in 'answers' table.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    add_input_box_column()
