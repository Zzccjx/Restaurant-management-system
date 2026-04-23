# Quick Setup Guide

## Prerequisites

1. **Python 3.8+** installed
2. **No database server required** - SQLite is built into Python!

## Step-by-Step Setup

### 1. Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note**: SQLite is included with Python, so no additional database installation is needed!

### 2. Database Setup

The database will be created automatically when you first run the application. The SQLite database file (`restaurant_pos.db`) will be created in the project root.

**Manual Database Creation (Optional):**

If you want to create the database manually using the schema file:

```bash
# Using SQLite CLI (if installed):
sqlite3 restaurant_pos.db < database_schema.sql

# Or using Python (recommended):
python
>>> from app import create_app
>>> from models import db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

### 3. Configuration

Create a `.env` file in the project root (optional, or edit `config.py`):

```env
DATABASE_NAME=restaurant_pos.db
SECRET_KEY=your-secret-key-change-in-production
FLASK_ENV=development
```

Or edit `config.py` directly. The database file location defaults to `restaurant_pos.db` in the project root.

### 4. Initialize Admin User

Run this Python script to set admin password:

```python
from app import create_app
from models import db, Admin
from utils.auth import hash_password

app = create_app()
with app.app_context():
    admin = Admin.query.filter_by(Username='admin').first()
    if admin:
        admin.PasswordHash = hash_password('admin123')
        db.session.commit()
        print("Admin password set to: admin123")
```

Or run in Python console:
```python
python
>>> from app import create_app
>>> from models import db, Admin
>>> from utils.auth import hash_password
>>> app = create_app()
>>> with app.app_context():
...     admin = Admin.query.filter_by(Username='admin').first()
...     if admin:
...         admin.PasswordHash = hash_password('admin123')
...         db.session.commit()
```

### 5. Run Application

```powershell
python app.py
```

Application will start on: `http://localhost:5000`

## Default Credentials

- **Admin Username**: `admin`
- **Admin Password**: `admin123` (change after first login)

## Testing the Application

### 1. Customer Flow
1. Visit `http://localhost:5000`
2. Click on a table
3. Enter mobile number → Send OTP
4. Verify OTP (check console/response for OTP in development)
5. Browse menu and add items to cart
6. Place order
7. Generate bill

### 2. Admin Flow
1. Visit `http://localhost:5000/admin/login`
2. Login with admin credentials
3. Access dashboard, tables, orders, KDS, menu management

## Common Issues

### Issue: Database File Not Created
**Solution**: 
- Ensure you have write permissions in the project directory
- Check that the directory exists and is accessible
- Verify SQLite is working: `python -c "import sqlite3; print(sqlite3.sqlite_version)"`

### Issue: Database Locked / Permission Denied
**Solution**: 
- Make sure no other process is using the database file
- Check file permissions on `restaurant_pos.db`
- On Windows, ensure the file is not locked by another application

### Issue: Module Not Found
**Solution**: 
```powershell
pip install -r requirements.txt
```

### Issue: Permission Denied on Uploads
**Solution**: Ensure `uploads/` and `static/` directories have write permissions

## Next Steps

1. **Configure SMS Gateway**: Update `utils/auth.py` `send_otp()` function to integrate with SMS provider (Twilio, AWS SNS, etc.)

2. **Production Deployment**:
   - Set `FLASK_ENV=production` in environment
   - Change `SECRET_KEY` to a secure random string
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Set up HTTPS
   - Configure proper database connection pooling

3. **Add Sample Data**: Create menu items, tables, and test orders

4. **Customize**: Update branding, colors, and business logic as needed

## File Structure

```
RestroProject/
├── app.py                 # Main application
├── config.py              # Configuration
├── models.py              # Database models
├── database_schema.sql    # Database schema
├── requirements.txt       # Dependencies
├── utils/                 # Utility modules
│   ├── auth.py           # Authentication
│   ├── database.py       # DB utilities
│   ├── billing.py        # Billing logic
│   ├── orders.py         # Order management
│   ├── offers.py         # Offer management
│   └── uploads.py        # File uploads
├── routes/                # Route handlers
│   ├── main.py           # Customer routes
│   └── admin.py          # Admin routes
├── templates/             # HTML templates
│   ├── base.html
│   ├── main/             # Customer pages
│   └── admin/            # Admin pages
├── static/                # Static files
│   ├── photos/           # Menu/user photos
│   ├── qr_codes/         # QR codes
│   └── feedback/         # Feedback photos
└── uploads/               # Upload storage
    ├── photos/
    ├── qr_codes/
    └── feedback/
```

## Support

For issues or questions, refer to the main `README.md` file.

