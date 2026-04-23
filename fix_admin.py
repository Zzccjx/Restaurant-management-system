"""
Script to fix/create admin user and verify login
Run this script to ensure admin user exists with correct password
"""
from app import create_app
from models import db, Admin
from utils.auth import hash_password, check_password_hash

app = create_app()

with app.app_context():
    print("=" * 60)
    print("ADMIN USER DIAGNOSTIC & FIX SCRIPT")
    print("=" * 60)
    
    # Check existing admins
    admins = Admin.query.all()
    print(f"\nFound {len(admins)} admin user(s) in database:")
    for a in admins:
        print(f"  - ID: {a.AdminID}, Username: '{a.Username}', Active: {a.IsActive}, SuperAdmin: {a.IsSuperAdmin}")
        if a.PasswordHash:
            print(f"    PasswordHash: {a.PasswordHash[:20]}... (length: {len(a.PasswordHash)})")
        else:
            print(f"    PasswordHash: NULL (NOT SET!)")
    
    # Get or create admin user
    username = 'admin'
    password = 'admin123'
    
    admin = Admin.query.filter_by(Username=username).first()
    
    # Set password hash first
    print(f"\n[SET PASSWORD] Generating password hash for '{password}'...")
    password_hash = hash_password(password)
    print(f"[SET PASSWORD] Password hash generated: {password_hash[:30]}...")
    
    if not admin:
        print(f"\n[CREATE] Creating new admin user '{username}'...")
        admin = Admin(
            Username=username,
            PasswordHash=password_hash,  # Set password hash when creating
            FullName='System Administrator',
            IsSuperAdmin=True,
            IsActive=True
        )
        db.session.add(admin)
        print(f"[CREATE] Admin user created with password hash")
    else:
        print(f"\n[FOUND] Admin user '{username}' exists (ID: {admin.AdminID})")
        print(f"[UPDATE] Updating password hash...")
        admin.PasswordHash = password_hash
        admin.IsActive = True
    
    db.session.commit()
    print(f"[COMMIT] Changes committed to database")
    
    # Verify password
    print(f"\n[VERIFY] Verifying password...")
    test_admin = Admin.query.filter_by(Username=username, IsActive=True).first()
    if test_admin:
        is_valid = check_password_hash(test_admin.PasswordHash, password)
        if is_valid:
            print(f"[VERIFY] [OK] Password verification SUCCESSFUL!")
        else:
            print(f"[VERIFY] [FAIL] Password verification FAILED!")
            print(f"         This means the hash doesn't match. Trying to re-hash...")
            test_admin.PasswordHash = hash_password(password)
            db.session.commit()
            is_valid = check_password_hash(test_admin.PasswordHash, password)
            if is_valid:
                print(f"[VERIFY] [OK] Password re-hashed and verified successfully!")
            else:
                print(f"[VERIFY] [FAIL] Still failing - there may be an issue with password hashing")
    else:
        print(f"[VERIFY] ✗ Admin user not found after commit!")
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL STATUS:")
    print("=" * 60)
    final_admin = Admin.query.filter_by(Username=username).first()
    if final_admin:
        print(f"Username: {final_admin.Username}")
        print(f"Active: {final_admin.IsActive}")
        print(f"SuperAdmin: {final_admin.IsSuperAdmin}")
        print(f"PasswordHash Set: {final_admin.PasswordHash is not None}")
        if final_admin.PasswordHash:
            verify_ok = check_password_hash(final_admin.PasswordHash, password)
            print(f"Password Verification: {'[PASS]' if verify_ok else '[FAIL]'}")
    print("\nYou can now login with:")
    print(f"  Username: {username}")
    print(f"  Password: {password}")
    print("=" * 60)
