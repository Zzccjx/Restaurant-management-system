"""
Script to populate the database with sample menu items
Run this script to add sample food items to the menu
"""
from app import create_app
from models import db, MenuItem
from decimal import Decimal

def populate_menu():
    """Add sample menu items to the database"""
    app = create_app()
    
    with app.app_context():
        # Check if menu items already exist
        existing_items = MenuItem.query.count()
        if existing_items > 0:
            print(f"[WARNING] {existing_items} menu items already exist.")
            response = input("Do you want to add more items? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled.")
                return
        
        # Sample menu items
        menu_items = [
            # Appetizers
            {
                'ItemName': 'Paneer Tikka',
                'ItemCode': 'APP001',
                'Description': 'Grilled cottage cheese cubes marinated in spices, served with mint chutney',
                'Category': 'Appetizers',
                'Price': Decimal('180.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 15,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': True,
                'IsAvailable': True,
                'DisplayOrder': 1
            },
            {
                'ItemName': 'Chicken Wings',
                'ItemCode': 'APP002',
                'Description': 'Crispy fried chicken wings with hot sauce',
                'Category': 'Appetizers',
                'Price': Decimal('220.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 20,
                'IsVegetarian': False,
                'IsVegan': False,
                'IsSpicy': True,
                'IsAvailable': True,
                'DisplayOrder': 2
            },
            {
                'ItemName': 'Spring Rolls',
                'ItemCode': 'APP003',
                'Description': 'Crispy vegetable spring rolls with sweet and sour sauce',
                'Category': 'Appetizers',
                'Price': Decimal('150.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 12,
                'IsVegetarian': True,
                'IsVegan': True,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 3
            },
            {
                'ItemName': 'Chicken Lollipop',
                'ItemCode': 'APP004',
                'Description': 'Spicy chicken drumsticks marinated and deep fried',
                'Category': 'Appetizers',
                'Price': Decimal('250.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 18,
                'IsVegetarian': False,
                'IsVegan': False,
                'IsSpicy': True,
                'IsAvailable': True,
                'DisplayOrder': 4
            },
            
            # Main Course - Vegetarian
            {
                'ItemName': 'Butter Paneer Masala',
                'ItemCode': 'MCV001',
                'Description': 'Creamy tomato-based curry with soft paneer cubes, served with naan',
                'Category': 'Main Course',
                'Price': Decimal('280.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 25,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 10
            },
            {
                'ItemName': 'Dal Makhani',
                'ItemCode': 'MCV002',
                'Description': 'Creamy black lentils cooked overnight, served with rice',
                'Category': 'Main Course',
                'Price': Decimal('200.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 20,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 11
            },
            {
                'ItemName': 'Vegetable Biryani',
                'ItemCode': 'MCV003',
                'Description': 'Fragrant basmati rice cooked with mixed vegetables and spices',
                'Category': 'Main Course',
                'Price': Decimal('220.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 30,
                'IsVegetarian': True,
                'IsVegan': True,
                'IsSpicy': True,
                'IsAvailable': True,
                'DisplayOrder': 12
            },
            {
                'ItemName': 'Palak Paneer',
                'ItemCode': 'MCV004',
                'Description': 'Spinach curry with cottage cheese cubes, served with roti',
                'Category': 'Main Course',
                'Price': Decimal('240.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 22,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 13
            },
            
            # Main Course - Non-Vegetarian
            {
                'ItemName': 'Butter Chicken',
                'ItemCode': 'MCN001',
                'Description': 'Creamy tomato-based curry with tender chicken pieces, served with naan',
                'Category': 'Main Course',
                'Price': Decimal('320.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 30,
                'IsVegetarian': False,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 20
            },
            {
                'ItemName': 'Chicken Biryani',
                'ItemCode': 'MCN002',
                'Description': 'Fragrant basmati rice with spiced chicken, served with raita',
                'Category': 'Main Course',
                'Price': Decimal('280.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 35,
                'IsVegetarian': False,
                'IsVegan': False,
                'IsSpicy': True,
                'IsAvailable': True,
                'DisplayOrder': 21
            },
            {
                'ItemName': 'Mutton Rogan Josh',
                'ItemCode': 'MCN003',
                'Description': 'Aromatic lamb curry with rich gravy, served with naan',
                'Category': 'Main Course',
                'Price': Decimal('380.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 40,
                'IsVegetarian': False,
                'IsVegan': False,
                'IsSpicy': True,
                'IsAvailable': True,
                'DisplayOrder': 22
            },
            {
                'ItemName': 'Fish Curry',
                'ItemCode': 'MCN004',
                'Description': 'Spicy fish curry with coconut milk, served with rice',
                'Category': 'Main Course',
                'Price': Decimal('300.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 25,
                'IsVegetarian': False,
                'IsVegan': False,
                'IsSpicy': True,
                'IsAvailable': True,
                'DisplayOrder': 23
            },
            
            # Breads
            {
                'ItemName': 'Garlic Naan',
                'ItemCode': 'BRD001',
                'Description': 'Fresh baked naan bread with garlic and butter',
                'Category': 'Breads',
                'Price': Decimal('50.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 8,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 30
            },
            {
                'ItemName': 'Butter Naan',
                'ItemCode': 'BRD002',
                'Description': 'Soft naan bread brushed with butter',
                'Category': 'Breads',
                'Price': Decimal('45.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 8,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 31
            },
            {
                'ItemName': 'Roti',
                'ItemCode': 'BRD003',
                'Description': 'Whole wheat flatbread',
                'Category': 'Breads',
                'Price': Decimal('25.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 5,
                'IsVegetarian': True,
                'IsVegan': True,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 32
            },
            {
                'ItemName': 'Tandoori Roti',
                'ItemCode': 'BRD004',
                'Description': 'Whole wheat bread baked in tandoor',
                'Category': 'Breads',
                'Price': Decimal('35.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 6,
                'IsVegetarian': True,
                'IsVegan': True,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 33
            },
            
            # Desserts
            {
                'ItemName': 'Gulab Jamun',
                'ItemCode': 'DES001',
                'Description': 'Sweet milk dumplings in sugar syrup',
                'Category': 'Desserts',
                'Price': Decimal('80.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 10,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 40
            },
            {
                'ItemName': 'Ice Cream',
                'ItemCode': 'DES002',
                'Description': 'Vanilla, Chocolate, or Strawberry ice cream',
                'Category': 'Desserts',
                'Price': Decimal('100.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 5,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 41
            },
            {
                'ItemName': 'Kheer',
                'ItemCode': 'DES003',
                'Description': 'Traditional rice pudding with nuts and cardamom',
                'Category': 'Desserts',
                'Price': Decimal('90.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 15,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 42
            },
            {
                'ItemName': 'Rasmalai',
                'ItemCode': 'DES004',
                'Description': 'Soft cottage cheese dumplings in sweetened milk',
                'Category': 'Desserts',
                'Price': Decimal('110.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 10,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 43
            },
            
            # Beverages
            {
                'ItemName': 'Mango Lassi',
                'ItemCode': 'BEV001',
                'Description': 'Refreshing yogurt drink with mango',
                'Category': 'Beverages',
                'Price': Decimal('80.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 5,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 50
            },
            {
                'ItemName': 'Sweet Lassi',
                'ItemCode': 'BEV002',
                'Description': 'Sweetened yogurt drink',
                'Category': 'Beverages',
                'Price': Decimal('60.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 5,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 51
            },
            {
                'ItemName': 'Fresh Lime Soda',
                'ItemCode': 'BEV003',
                'Description': 'Refreshing lime soda with salt',
                'Category': 'Beverages',
                'Price': Decimal('50.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 3,
                'IsVegetarian': True,
                'IsVegan': True,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 52
            },
            {
                'ItemName': 'Masala Chai',
                'ItemCode': 'BEV004',
                'Description': 'Spiced Indian tea with milk',
                'Category': 'Beverages',
                'Price': Decimal('40.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 5,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 53
            },
            {
                'ItemName': 'Cold Coffee',
                'ItemCode': 'BEV005',
                'Description': 'Iced coffee with milk and sugar',
                'Category': 'Beverages',
                'Price': Decimal('90.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 5,
                'IsVegetarian': True,
                'IsVegan': False,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 54
            },
            {
                'ItemName': 'Fresh Orange Juice',
                'ItemCode': 'BEV006',
                'Description': 'Freshly squeezed orange juice',
                'Category': 'Beverages',
                'Price': Decimal('70.00'),
                'GSTPercentage': Decimal('5.00'),
                'PreparationTime': 5,
                'IsVegetarian': True,
                'IsVegan': True,
                'IsSpicy': False,
                'IsAvailable': True,
                'DisplayOrder': 55
            },
        ]
        
        # Add items to database
        added_count = 0
        for item_data in menu_items:
            # Check if item with same code already exists
            existing = MenuItem.query.filter_by(ItemCode=item_data['ItemCode']).first()
            if existing:
                print(f"[SKIP] Item {item_data['ItemCode']} already exists, skipping...")
                continue
            
            item = MenuItem(**item_data)
            db.session.add(item)
            added_count += 1
        
        db.session.commit()
        print(f"[OK] Successfully added {added_count} menu items to the database!")
        print(f"[OK] Total menu items: {MenuItem.query.count()}")
        print("\nCategories added:")
        categories = db.session.query(MenuItem.Category).distinct().all()
        for cat in categories:
            count = MenuItem.query.filter_by(Category=cat[0]).count()
            print(f"  - {cat[0]}: {count} items")

if __name__ == '__main__':
    print("=" * 50)
    print("Restaurant Menu Population Script")
    print("=" * 50)
    populate_menu()
    print("\n[OK] Done! You can now view the menu at http://localhost:5000/menu")
