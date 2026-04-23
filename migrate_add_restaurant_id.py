"""
Migration script to add RestaurantID column to RestaurantTables
Run this script once to update your existing database schema.
"""
import sqlite3
import os
from config import Config

def migrate_database():
    """Add RestaurantID column to RestaurantTables if it doesn't exist"""
    
    # Get database path
    db_path = Config.DATABASE_PATH
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(RestaurantTables)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'RestaurantID' in columns:
            print("[OK] RestaurantID column already exists. No migration needed.")
            conn.close()
            return True
        
        # Add the column
        print("Adding RestaurantID column to RestaurantTables...")
        cursor.execute("""
            ALTER TABLE RestaurantTables 
            ADD COLUMN RestaurantID INTEGER REFERENCES Restaurants(RestaurantID)
        """)
        
        conn.commit()
        conn.close()
        
        print("[OK] Migration completed successfully!")
        print("  RestaurantID column added to RestaurantTables table.")
        print("  Note: All existing tables will have RestaurantID = NULL (which is fine).")
        return True
        
    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Database Migration: Add RestaurantID to RestaurantTables")
    print("=" * 60)
    print()
    
    success = migrate_database()
    
    if success:
        print()
        print("You can now restart your Flask application.")
    else:
        print()
        print("Migration failed. Please check the error above.")
        print("Make sure to backup your database before running migrations.")
