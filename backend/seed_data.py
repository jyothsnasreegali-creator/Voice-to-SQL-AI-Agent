from sqlalchemy import create_engine, text

# Connect to your existing database
engine = create_engine("sqlite:///sales.db")

# Sample data to insert
students = [
    ('Jyothsna', 21, 'Computer Science'),
    ('Priya Sharma', 22, 'Artificial Intelligence'),
    ('Rahul Verma', 20, 'Data Science'),
    ('Siddharth', 23, 'Machine Learning'),
    ('Ananya', 21, 'Software Engineering')
]

def seed_database():
    with engine.connect() as conn:
        # 1. Create table if it doesn't exist
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                major TEXT
            )
        """))
        
        # 2. Clear existing data so you don't get duplicates
        conn.execute(text("DELETE FROM students"))
        
        # 3. Insert the sample records
        for name, age, major in students:
            conn.execute(
                text("INSERT INTO students (name, age, major) VALUES (:name, :age, :major)"),
                {"name": name, "age": age, "major": major}
            )
        
        conn.commit()
        print("✅ Sample data created successfully!")

if __name__ == "__main__":
    seed_database()