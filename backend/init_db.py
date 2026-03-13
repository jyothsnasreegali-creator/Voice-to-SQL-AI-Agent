from sqlalchemy import create_engine, text

# 1. Create the engine
engine = create_engine("sqlite:///sales.db")

# 2. Rebuild the tables
with engine.connect() as conn:
    print("Creating tables...")
    # Create products table
    conn.execute(text("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL)"))
    
    # Create employees table (to restore what was lost)
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            role TEXT, 
            salary REAL
        )
    """))
    
    conn.commit()
    print("✅ Database initialized successfully!")