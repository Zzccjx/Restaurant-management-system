"""
Check database schema and fix if needed
"""
import sqlite3
import os
from config import Config

def check_and_fix_schema():
    """Check database schema and add missing tables/columns"""
    
    db_path = Config.DATABASE_PATH
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if Restaurants table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='Restaurants'
        """)
        restaurants_exists = cursor.fetchone() is not None
        
        if not restaurants_exists:
            print("Creating Restaurants table...")
            cursor.execute("""
                CREATE TABLE Restaurants (
                    RestaurantID INTEGER PRIMARY KEY AUTOINCREMENT,
                    RestaurantName TEXT NOT NULL,
                    CuisineType TEXT,
                    Address TEXT,
                    PhoneNumber TEXT,
                    Email TEXT,
                    Rating NUMERIC(3, 2) DEFAULT 0.00,
                    OfferPercentage NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
                    RestaurantImage TEXT,
                    IsActive INTEGER NOT NULL DEFAULT 1,
                    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UpdatedAt TIMESTAMP
                )
            """)
            print("[OK] Restaurants table created.")
        else:
            print("[OK] Restaurants table exists.")
        
        # Check RestaurantTables columns
        cursor.execute("PRAGMA table_info(RestaurantTables)")
        columns = {column[1]: column for column in cursor.fetchall()}
        
        if 'RestaurantID' not in columns:
            print("Adding RestaurantID column to RestaurantTables...")
            cursor.execute("""
                ALTER TABLE RestaurantTables 
                ADD COLUMN RestaurantID INTEGER
            """)
            print("[OK] RestaurantID column added.")
        else:
            print("[OK] RestaurantID column exists.")
        
        conn.commit()
        conn.close()
        
        print("\n[OK] Database schema check completed!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Database Schema Check and Fix")
    print("=" * 60)
    print()
    
    check_and_fix_schema()
    
    print("\nYou can now restart your Flask application.")
