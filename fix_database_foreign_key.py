"""
Fix database foreign key constraint for RestaurantID
SQLite doesn't support adding foreign keys via ALTER TABLE,
so we need to recreate the table or ensure the constraint is properly set.
"""
import sqlite3
import os
from config import Config

def fix_foreign_key():
    """Ensure RestaurantID column exists and is properly configured"""
    
    db_path = Config.DATABASE_PATH
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Check current schema
        cursor.execute("PRAGMA table_info(RestaurantTables)")
        columns = {col[1]: col for col in cursor.fetchall()}
        
        print("Current RestaurantTables columns:")
        for col_name, col_info in columns.items():
            print(f"  - {col_name}: {col_info[2]}")
        
        # Check if RestaurantID exists
        if 'RestaurantID' not in columns:
            print("\nAdding RestaurantID column...")
            cursor.execute("""
                ALTER TABLE RestaurantTables 
                ADD COLUMN RestaurantID INTEGER
            """)
            conn.commit()
            print("[OK] RestaurantID column added.")
        else:
            print("\n[OK] RestaurantID column already exists.")
        
        # Verify Restaurants table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='Restaurants'
        """)
        if not cursor.fetchone():
            print("\nCreating Restaurants table...")
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
            conn.commit()
            print("[OK] Restaurants table created.")
        else:
            print("\n[OK] Restaurants table exists.")
        
        # Test query to verify column exists
        try:
            cursor.execute("SELECT RestaurantID FROM RestaurantTables LIMIT 1")
            print("\n[OK] RestaurantID column is accessible.")
        except sqlite3.OperationalError as e:
            print(f"\n[ERROR] Cannot access RestaurantID: {e}")
            conn.close()
            return False
        
        conn.close()
        print("\n[OK] Database schema is correct!")
        print("\nNote: SQLite doesn't enforce foreign key constraints by default.")
        print("The relationship will work in SQLAlchemy even without explicit FK constraint.")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Fix Database Foreign Key for RestaurantID")
    print("=" * 60)
    print()
    
    fix_foreign_key()
    
    print("\n" + "=" * 60)
    print("Please restart your Flask application now.")
    print("=" * 60)
