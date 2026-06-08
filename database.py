import psycopg2
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

# Support Streamlit secrets
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        os.environ["DB_HOST"] = st.secrets.get("DB_HOST", os.getenv("DB_HOST", "localhost"))
        os.environ["DB_NAME"] = st.secrets.get("DB_NAME", os.getenv("DB_NAME", "postgres"))
        os.environ["DB_USER"] = st.secrets.get("DB_USER", os.getenv("DB_USER", "postgres"))
        os.environ["DB_PASSWORD"] = st.secrets.get("DB_PASSWORD", os.getenv("DB_PASSWORD", ""))
        os.environ["DB_PORT"] = st.secrets.get("DB_PORT", os.getenv("DB_PORT", "5432"))
except Exception:
    pass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432"),
        sslmode="require"
    )

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outfit_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            city VARCHAR(100),
            occasion VARCHAR(50),
            suggestion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Tables created successfully!")

def register_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    try:
        cursor.execute("""
            INSERT INTO users (username, email, password) 
            VALUES (%s, %s, %s)
        """, (username, email, hashed))
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, hashed))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return user[0]
    return None

def save_outfit_history(user_id, city, occasion, suggestion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO outfit_history (user_id, city, occasion, suggestion)
        VALUES (%s, %s, %s, %s)
    """, (user_id, city, occasion, suggestion))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()