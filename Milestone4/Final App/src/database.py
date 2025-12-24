import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "pcb_production.db"

def init_db():
    """Initializes the database with the required table."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            filename TEXT,
            defects_count INTEGER,
            health_score REAL,
            status TEXT,
            cost REAL,
            is_scrap INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def log_inspection(filename, defects_count, score, status, cost, is_scrap):
    """Saves a single inspection result to the DB."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO inspections (timestamp, filename, defects_count, health_score, status, cost, is_scrap)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename, defects_count, score, status, cost, 1 if is_scrap else 0))
    conn.commit()
    conn.close()

def get_production_stats():
    """Fetches aggregated stats for the sidebar."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM inspections", conn)
    conn.close()
    
    if df.empty:
        return 0, 0.0, pd.DataFrame() # Total, Avg Score, History DF
        
    total_boards = len(df)
    avg_score = df['health_score'].mean()
    # Return last 50 records for the trend chart
    history_df = df[['health_score']].tail(20) 
    
    return total_boards, avg_score, history_df

def get_full_history():
    """Returns the complete history for export."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM inspections ORDER BY id DESC", conn)
    conn.close()
    return df

def clear_all_data():
    """Wipes all data from the inspections table."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM inspections")
    conn.commit()
    conn.close()