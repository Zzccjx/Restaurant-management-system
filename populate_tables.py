"""
Script to populate the database with sample restaurant tables
Run this script to add sample tables to the database
"""
from app import create_app
from models import db, RestaurantTable

def populate_tables():
    """Add sample restaurant tables to the database"""
    app = create_app()
    
    with app.app_context():
        # Check if tables already exist
        existing_tables = RestaurantTable.query.count()
        if existing_tables > 0:
            print(f"[WARNING] {existing_tables} tables already exist.")
            response = input("Do you want to add more tables? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled.")
                return
        
        # Sample restaurant tables
        table_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        
        added_count = 0
        for table_num in table_numbers:
            # Check if table with same number already exists
            existing = RestaurantTable.query.filter_by(TableNumber=table_num).first()
            if existing:
                print(f"[SKIP] Table {table_num} already exists, skipping...")
                continue
            
            table = RestaurantTable(
                TableNumber=table_num,
                Capacity=4,
                Status='Free',
                IsActive=True
            )
            db.session.add(table)
            added_count += 1
        
        db.session.commit()
        print(f"[OK] Successfully added {added_count} tables to the database!")
        print(f"[OK] Total tables: {RestaurantTable.query.count()}")
        print("\nTables created:")
        tables = RestaurantTable.query.filter_by(IsActive=True).order_by(RestaurantTable.TableNumber).all()
        for table in tables:
            print(f"  - Table {table.TableNumber} (Capacity: {table.Capacity}, Status: {table.Status})")

if __name__ == '__main__':
    print("=" * 50)
    print("Restaurant Tables Population Script")
    print("=" * 50)
    populate_tables()
    print("\n[OK] Done! Tables are now available for ordering.")
