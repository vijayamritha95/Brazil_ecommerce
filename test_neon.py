from database.connection import test_database_connection

if test_database_connection():
    print("Connected to Neon PostgreSQL successfully!")
else:
    print("Database connection failed.")