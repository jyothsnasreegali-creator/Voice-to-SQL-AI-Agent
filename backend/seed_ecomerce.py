from sqlalchemy import create_engine, text

# Connect to your existing database
engine = create_engine("sqlite:///sales.db")

def seed():
    with engine.connect() as conn:
        print("Cleaning up old tables...")
        # 1. Drop existing tables to reset the schema
        conn.execute(text("DROP TABLE IF EXISTS orders"))
        conn.execute(text("DROP TABLE IF EXISTS products"))
        
        # 2. Create tables with the correct columns
        print("Creating fresh E-commerce tables...")
        conn.execute(text("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                price REAL, 
                stock INTEGER
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                product_id INTEGER, 
                status TEXT, 
                total REAL,
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        """))
        
        # 3. Insert fresh sample data
        print("Inserting sample data...")
        conn.execute(text("""
            INSERT INTO products (name, price, stock) VALUES 
            ('Laptop', 85000, 10), 
            ('Phone', 45000, 25), 
            ('Headphones', 5000, 50)
        """))
        
        conn.execute(text("""
            INSERT INTO orders (product_id, status, total) VALUES 
            (1, 'Shipped', 85000), 
            (2, 'Pending', 45000),
            (1, 'Delivered', 85000)
        """))
        
        conn.commit()
        print("✅ E-commerce database is ready for your demo, Jyothsna!")

if __name__ == "__main__":
    seed()