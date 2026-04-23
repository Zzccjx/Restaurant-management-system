# Restaurant Billing & POS System

Production-ready Restaurant Billing & Point of Sale (POS) web application built with Flask and SQLite.

## Tech Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **ORM**: SQLAlchemy 2.0.23
- **Database**: SQLite (file-based, no server required)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Authentication**: Session-based + OTP (mobile)
- **Architecture**: MVC / Modular

## Features

### Core Features
- ✅ Table-based ordering (no login required for guests)
- ✅ Mobile number authentication (OTP)
- ✅ Guest mode support
- ✅ User registration (optional)
- ✅ Admin panel with full system control

### Advanced Features
- ✅ **Merge Tables** - Group multiple tables together
- ✅ **Split Bills** - Item-based bill splitting
- ✅ **QR Code Ordering** - Table-specific QR codes
- ✅ **Kitchen Display System (KDS)** - Real-time order tracking
- ✅ **Order Analytics** - Timing and performance metrics

### Business Features
- ✅ Menu management with multiple photos per item
- ✅ Membership system (Silver, Gold, Platinum) with discounts
- ✅ Offer management with minimum bill validation
- ✅ GST calculation
- ✅ Payment processing
- ✅ Feedback system with ratings and photos

## Project Structure

```
RestroProject/
├── app.py                 # Flask application entry point
├── config.py              # Configuration settings
├── models.py              # SQLAlchemy database models
├── requirements.txt       # Python dependencies
├── database_schema.sql    # SQLite schema
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── auth.py           # Authentication & OTP
│   ├── database.py       # Database utilities
│   ├── billing.py        # Billing & payments
│   ├── orders.py         # Order management
│   └── offers.py         # Offer management
├── routes/                # Route handlers
│   ├── __init__.py
│   ├── main.py           # Customer-facing routes
│   └── admin.py          # Admin panel routes
├── templates/             # Jinja2 templates
│   ├── base.html
│   └── main/
│       ├── index.html
│       └── error.html
└── static/                # Static files (CSS, JS, images)
    ├── css/
    ├── js/
    ├── photos/
    ├── qr_codes/
    └── feedback/
```

## Setup Instructions

### 1. Python Environment Setup

1. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

**Note**: SQLite is built into Python, so no additional database server or drivers are required!

### 2. Database Setup

The database will be created automatically when you first run the application. The SQLite database file (`restaurant_pos.db`) will be created in the project root directory.

To manually create the database from the schema:

1. **Option 1 - Using SQLite CLI:**
   ```bash
   sqlite3 restaurant_pos.db < database_schema.sql
   ```

2. **Option 2 - Using Python:**
   ```python
   from app import create_app
   from models import db
   
   app = create_app()
   with app.app_context():
       db.create_all()
   ```

### 3. Configuration

1. **Set Environment Variables** (optional, or modify `config.py`):
   ```bash
   set DATABASE_NAME=restaurant_pos.db  # Default: restaurant_pos.db
   set SECRET_KEY=your-secret-key-here
   set FLASK_ENV=development
   ```

2. **Database Configuration:**
   The database file location can be customized in `config.py` via the `DATABASE_NAME` environment variable. By default, it creates `restaurant_pos.db` in the project root.

### 4. Initialize Database

1. **Create Tables and Set Admin Password:**
   ```python
   from app import create_app
   from models import db, Admin
   from utils.auth import hash_password
   
   app = create_app()
   with app.app_context():
       # Create all tables
       db.create_all()
       
       # Set admin password
       admin = Admin.query.filter_by(Username='admin').first()
       if admin:
           admin.PasswordHash = hash_password('admin123')
           db.session.commit()
           print("Admin password set to: admin123")
       else:
           # Create admin user if it doesn't exist
           admin = Admin(
               Username='admin',
               PasswordHash=hash_password('admin123'),
               FullName='System Administrator',
               IsSuperAdmin=True
           )
           db.session.add(admin)
           db.session.commit()
           print("Admin user created with password: admin123")
   ```

### 5. Run Application

```bash
python app.py
```

Application will run on `http://localhost:5000`

## Default Credentials

- **Admin Username**: `admin`
- **Admin Password**: `admin123` (change after first login)

## API Endpoints

### Customer Endpoints
- `POST /api/send-otp` - Send OTP to mobile
- `POST /api/verify-otp` - Verify OTP and login
- `POST /api/create-order` - Create new order
- `POST /api/add-item` - Add item to order
- `POST /api/update-item` - Update item quantity
- `POST /api/remove-item` - Remove item from order
- `GET /api/order/<id>` - Get order details
- `POST /api/apply-offer` - Apply offer code
- `GET /api/generate-bill/<id>` - Generate bill

### Admin Endpoints
- `GET /admin/api/tables` - Get all tables
- `POST /admin/api/tables/merge` - Merge tables
- `POST /admin/api/tables/unmerge` - Unmerge tables
- `GET /admin/api/orders` - Get orders
- `POST /admin/api/orders/<id>/status` - Update order status
- `GET /admin/api/kds` - Get KDS orders
- `POST /admin/api/kds/item/<id>/status` - Update item status
- `GET /admin/api/menu/items` - Get menu items
- `POST /admin/api/menu/items` - Create menu item
- `PUT /admin/api/menu/items/<id>` - Update menu item
- `GET /admin/api/bills` - Get bills
- `POST /admin/api/bills/<id>/payment` - Process payment
- `GET /admin/api/reports/sales` - Get sales report

## Database Schema

The database includes 14 main tables:
1. Memberships
2. Users (Guest + Registered)
3. Admins
4. RestaurantTables
5. TableReservations
6. MenuItems
7. MenuPhotos
8. Orders
9. OrderItems
10. Bills
11. BillSplits
12. Offers
13. OrderOffers
14. Feedback

See `database_schema.sql` for complete schema definition.

## Development Notes

- **OTP in Development**: OTP is displayed on screen for testing. Configure Twilio for SMS in production.
- **File Uploads**: Configure `UPLOAD_FOLDER` in `config.py`
- **SMS Gateway**: Twilio SMS integration is available. See `TWILIO_SETUP.md` for setup instructions.
- **Production**: Set `FLASK_ENV=production` and update `SECRET_KEY`

## SMS Integration (Twilio)

The application supports Twilio SMS for sending OTP codes. 

**Quick Setup:**
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env`
3. Get Twilio credentials from https://www.twilio.com/console
4. Add credentials to `.env` file
5. Restart the application

**Detailed Guide:** See `TWILIO_SETUP.md` for complete setup instructions.

**Development Mode:** If Twilio is not configured, OTP will be displayed on the login page.

## Next Steps

1. Complete frontend templates (menu, table, bill views)
2. Add file upload handling for photos
3. Add print functionality for bills
4. Implement real-time updates (WebSocket/SSE)
5. Add comprehensive error handling
6. Write unit tests
7. Deploy to production server

## License

Proprietary - Restaurant POS System

## Author
**Nikunj Nakum**  
💻 Python & Flask Developer  
📍 India  
🔗 GitHub: https://github.com/Zzccjx
