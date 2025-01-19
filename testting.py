from sqlalchemy import create_engine

uri = 'postgresql://flask_user:flaskpassword@localhost/teachers_app'
engine = create_engine(uri)
connection = engine.connect()
print("Connection successful!")
connection.close()
