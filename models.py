"""
SQLAlchemy Models for Restaurant Billing & POS System
Maps to SQLite database schema
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func, CheckConstraint
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# ====================================================
# MEMBERSHIP MODEL
# ====================================================
class Membership(db.Model):
    __tablename__ = 'Memberships'
    
    MembershipID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MembershipName = db.Column(db.String(50), nullable=False, unique=True)
    DiscountPercentage = db.Column(db.Numeric(5, 2), nullable=False, default=0.00)
    MinimumOrderAmount = db.Column(db.Numeric(10, 2), default=0.00)
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    users = relationship('User', back_populates='membership')
    
    def __repr__(self):
        return f'<Membership {self.MembershipName}>'
    
    def to_dict(self):
        return {
            'id': self.MembershipID,
            'name': self.MembershipName,
            'discount_percentage': float(self.DiscountPercentage),
            'minimum_order_amount': float(self.MinimumOrderAmount),
            'is_active': self.IsActive
        }

# ====================================================
# USER MODEL (Guest + Registered)
# ====================================================
class User(db.Model):
    __tablename__ = 'Users'
    
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MobileNumber = db.Column(db.String(15), nullable=False, unique=True)
    FullName = db.Column(db.String(100), nullable=True)
    Email = db.Column(db.String(100), nullable=True)
    PhotoPath = db.Column(db.String(500), nullable=True)
    MembershipID = db.Column(db.Integer, db.ForeignKey('Memberships.MembershipID'), nullable=True)
    IsGuest = db.Column(db.Boolean, nullable=False, default=True)
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    OTP = db.Column(db.String(10), nullable=True)
    OTPExpiry = db.Column(db.DateTime, nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    membership = relationship('Membership', back_populates='users')
    orders = relationship('Order', back_populates='user')
    # Removed bills relationship - using Order as single source of truth
    feedbacks = relationship('Feedback', back_populates='user')
    
    def __repr__(self):
        return f'<User {self.MobileNumber}>'
    
    def to_dict(self):
        return {
            'id': self.UserID,
            'mobile_number': self.MobileNumber,
            'full_name': self.FullName,
            'email': self.Email,
            'photo_path': self.PhotoPath,
            'membership_id': self.MembershipID,
            'is_guest': self.IsGuest,
            'is_active': self.IsActive,
            'created_at': self.CreatedAt.isoformat() if self.CreatedAt else None
        }

# ====================================================
# ADMIN MODEL
# ====================================================
class Admin(db.Model):
    __tablename__ = 'Admins'
    
    AdminID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(50), nullable=False, unique=True)
    PasswordHash = db.Column(db.String(255), nullable=False)
    FullName = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=True)
    MobileNumber = db.Column(db.String(15), nullable=True)
    IsSuperAdmin = db.Column(db.Boolean, nullable=False, default=False)
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    LastLogin = db.Column(db.DateTime, nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Admin {self.Username}>'
    
    def to_dict(self):
        return {
            'id': self.AdminID,
            'username': self.Username,
            'full_name': self.FullName,
            'email': self.Email,
            'is_super_admin': self.IsSuperAdmin,
            'is_active': self.IsActive
        }

# ====================================================
# RESTAURANT MODEL (Restaurant Information)
# ====================================================
class Restaurant(db.Model):
    __tablename__ = 'Restaurants'
    
    RestaurantID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RestaurantName = db.Column(db.String(200), nullable=False)
    CuisineType = db.Column(db.String(100), nullable=True)
    Address = db.Column(db.String(500), nullable=True)
    PhoneNumber = db.Column(db.String(20), nullable=True)
    Email = db.Column(db.String(100), nullable=True)
    Rating = db.Column(db.Numeric(3, 2), nullable=True, default=0.00)
    OfferPercentage = db.Column(db.Numeric(5, 2), nullable=False, default=0.00)
    RestaurantImage = db.Column(db.String(500), nullable=True)
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    tables = relationship('RestaurantTable', back_populates='restaurant')
    
    def __repr__(self):
        return f'<Restaurant {self.RestaurantName}>'
    
    def to_dict(self):
        return {
            'id': self.RestaurantID,
            'name': self.RestaurantName,
            'cuisine_type': self.CuisineType,
            'address': self.Address,
            'phone_number': self.PhoneNumber,
            'email': self.Email,
            'rating': float(self.Rating) if self.Rating else 0.00,
            'offer_percentage': float(self.OfferPercentage),
            'restaurant_image': self.RestaurantImage,
            'is_active': self.IsActive,
            'created_at': self.CreatedAt.isoformat() if self.CreatedAt else None
        }

# ====================================================
# RESTAURANT TABLE MODEL
# ====================================================
class RestaurantTable(db.Model):
    __tablename__ = 'RestaurantTables'
    
    TableID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RestaurantID = db.Column(db.Integer, db.ForeignKey('Restaurants.RestaurantID'), nullable=True)
    TableNumber = db.Column(db.String(10), nullable=False, unique=True)
    Capacity = db.Column(db.Integer, nullable=False, default=4)
    Status = db.Column(db.String(20), nullable=False, default='Free')
    GroupID = db.Column(db.Integer, nullable=True)  # For merged tables
    QRCodePath = db.Column(db.String(500), nullable=True)
    CurrentOrderID = db.Column(db.Integer, nullable=True)
    Notes = db.Column(db.String(500), nullable=True)
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    restaurant = relationship('Restaurant', back_populates='tables')
    orders = relationship('Order', back_populates='table')
    reservations = relationship('TableReservation', back_populates='table')
    # Removed bills relationship - using Order as single source of truth
    
    def __repr__(self):
        return f'<RestaurantTable {self.TableNumber}>'
    
    def to_dict(self):
        return {
            'id': self.TableID,
            'table_number': self.TableNumber,
            'capacity': self.Capacity,
            'status': self.Status,
            'group_id': self.GroupID,
            'qr_code_path': self.QRCodePath,
            'current_order_id': self.CurrentOrderID,
            'is_active': self.IsActive
        }

# ====================================================
# TABLE RESERVATION MODEL
# ====================================================
class TableReservation(db.Model):
    __tablename__ = 'TableReservations'
    
    ReservationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TableID = db.Column(db.Integer, db.ForeignKey('RestaurantTables.TableID'), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=True)
    MobileNumber = db.Column(db.String(15), nullable=False)
    CustomerName = db.Column(db.String(100), nullable=False)
    ReservationDate = db.Column(db.DateTime, nullable=False)
    ReservationTime = db.Column(db.Time, nullable=False)
    NumberOfGuests = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.String(20), nullable=False, default='Pending')
    SpecialRequests = db.Column(db.String(500), nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    table = relationship('RestaurantTable', back_populates='reservations')
    user = relationship('User')
    
    def __repr__(self):
        return f'<TableReservation {self.ReservationID}>'
    
    def to_dict(self):
        return {
            'id': self.ReservationID,
            'table_id': self.TableID,
            'user_id': self.UserID,
            'mobile_number': self.MobileNumber,
            'customer_name': self.CustomerName,
            'reservation_date': self.ReservationDate.isoformat() if self.ReservationDate else None,
            'reservation_time': str(self.ReservationTime) if self.ReservationTime else None,
            'number_of_guests': self.NumberOfGuests,
            'status': self.Status
        }

# ====================================================
# MENU ITEM MODEL
# ====================================================
class MenuItem(db.Model):
    __tablename__ = 'MenuItems'
    
    MenuItemID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ItemName = db.Column(db.String(200), nullable=False)
    ItemCode = db.Column(db.String(50), nullable=True, unique=True)
    Description = db.Column(db.String(1000), nullable=True)
    Category = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Numeric(10, 2), nullable=False)
    GSTPercentage = db.Column(db.Numeric(5, 2), nullable=False, default=5.00)
    PreparationTime = db.Column(db.Integer, nullable=True)
    IsVegetarian = db.Column(db.Boolean, nullable=False, default=False)
    IsVegan = db.Column(db.Boolean, nullable=False, default=False)
    IsSpicy = db.Column(db.Boolean, nullable=False, default=False)
    IsAvailable = db.Column(db.Boolean, nullable=False, default=True)
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    DisplayOrder = db.Column(db.Integer, nullable=True, default=0)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    photos = relationship('MenuPhoto', back_populates='menu_item', cascade='all, delete-orphan')
    order_items = relationship('OrderItem', back_populates='menu_item')
    
    def __repr__(self):
        return f'<MenuItem {self.ItemName}>'
    
    def to_dict(self, include_photos=False):
        data = {
            'id': self.MenuItemID,
            'item_name': self.ItemName,
            'item_code': self.ItemCode,
            'description': self.Description,
            'category': self.Category,
            'price': float(self.Price),
            'gst_percentage': float(self.GSTPercentage),
            'preparation_time': self.PreparationTime,
            'is_vegetarian': self.IsVegetarian,
            'is_vegan': self.IsVegan,
            'is_spicy': self.IsSpicy,
            'is_available': self.IsAvailable,
            'display_order': self.DisplayOrder
        }
        if include_photos:
            data['photos'] = [photo.to_dict() for photo in self.photos]
        return data

# ====================================================
# MENU PHOTO MODEL
# ====================================================
class MenuPhoto(db.Model):
    __tablename__ = 'MenuPhotos'
    
    PhotoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MenuItemID = db.Column(db.Integer, db.ForeignKey('MenuItems.MenuItemID'), nullable=False)
    PhotoPath = db.Column(db.String(500), nullable=False)
    IsPrimary = db.Column(db.Boolean, nullable=False, default=False)
    DisplayOrder = db.Column(db.Integer, nullable=False, default=0)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    menu_item = relationship('MenuItem', back_populates='photos')
    
    def __repr__(self):
        return f'<MenuPhoto {self.PhotoID}>'
    
    def to_dict(self):
        return {
            'id': self.PhotoID,
            'menu_item_id': self.MenuItemID,
            'photo_path': self.PhotoPath,
            'is_primary': self.IsPrimary,
            'display_order': self.DisplayOrder
        }

# ====================================================
# ORDER MODEL
# ====================================================
class Order(db.Model):
    __tablename__ = 'Orders'
    
    OrderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderNumber = db.Column(db.String(20), nullable=False, unique=True)
    TableID = db.Column(db.Integer, db.ForeignKey('RestaurantTables.TableID'), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=True)
    MobileNumber = db.Column(db.String(15), nullable=True)  # Optional mobile number
    OrderStatus = db.Column(db.String(20), nullable=False, default='Pending')
    OrderType = db.Column(db.String(20), nullable=False, default='DineIn')
    SubTotal = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    GSTAmount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    MembershipDiscount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    OfferDiscount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    TotalAmount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    SpecialInstructions = db.Column(db.String(500), nullable=True)
    KitchenNotes = db.Column(db.String(500), nullable=True)
    OrderPlacedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    OrderPreparedAt = db.Column(db.DateTime, nullable=True)
    OrderServedAt = db.Column(db.DateTime, nullable=True)
    OrderCompletedAt = db.Column(db.DateTime, nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    table = relationship('RestaurantTable', back_populates='orders')
    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    # Removed bills relationship - using Order as single source of truth
    order_offers = relationship('OrderOffer', back_populates='order', cascade='all, delete-orphan')
    # Removed feedback relationship - using standalone CustomerFeedback model
    
    def __repr__(self):
        return f'<Order {self.OrderNumber}>'
    
    def to_dict(self, include_items=False):
        data = {
            'id': self.OrderID,
            'order_number': self.OrderNumber,
            'table_id': self.TableID,
            'user_id': self.UserID,
            'mobile_number': self.MobileNumber,
            'order_status': self.OrderStatus,
            'order_type': self.OrderType,
            'sub_total': float(self.SubTotal),
            'gst_amount': float(self.GSTAmount),
            'membership_discount': float(self.MembershipDiscount),
            'offer_discount': float(self.OfferDiscount),
            'total_amount': float(self.TotalAmount),
            'order_placed_at': self.OrderPlacedAt.isoformat() if self.OrderPlacedAt else None,
            # Add formatted time fields for easy display
            'order_time': self.OrderPlacedAt.strftime('%H:%M:%S') if self.OrderPlacedAt else None,
            'order_date': self.OrderPlacedAt.strftime('%Y-%m-%d') if self.OrderPlacedAt else None,
            'order_datetime': self.OrderPlacedAt.strftime('%Y-%m-%d %H:%M:%S') if self.OrderPlacedAt else None
        }
        if include_items:
            data['items'] = [item.to_dict() for item in self.order_items]
        return data

# ====================================================
# ORDER ITEM MODEL
# ====================================================
class OrderItem(db.Model):
    __tablename__ = 'OrderItems'
    
    OrderItemID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('Orders.OrderID'), nullable=False)
    MenuItemID = db.Column(db.Integer, db.ForeignKey('MenuItems.MenuItemID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False, default=1)
    UnitPrice = db.Column(db.Numeric(10, 2), nullable=False)
    GSTPercentage = db.Column(db.Numeric(5, 2), nullable=False)
    GSTAmount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    ItemSubTotal = db.Column(db.Numeric(10, 2), nullable=False)
    SpecialInstructions = db.Column(db.String(500), nullable=True)
    ItemStatus = db.Column(db.String(20), nullable=False, default='Pending')
    SplitBillID = db.Column(db.Integer, nullable=True)  # For split bills
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    order = relationship('Order', back_populates='order_items')
    menu_item = relationship('MenuItem', back_populates='order_items')
    
    def __repr__(self):
        return f'<OrderItem {self.OrderItemID}>'
    
    def to_dict(self):
        return {
            'id': self.OrderItemID,
            'order_id': self.OrderID,
            'menu_item_id': self.MenuItemID,
            'menu_item_name': self.menu_item.ItemName if self.menu_item else None,
            'quantity': self.Quantity,
            'unit_price': float(self.UnitPrice),
            'gst_percentage': float(self.GSTPercentage),
            'gst_amount': float(self.GSTAmount),
            'item_sub_total': float(self.ItemSubTotal),
            'item_status': self.ItemStatus,
            'split_bill_id': self.SplitBillID
        }

# ====================================================
# BILL MODEL - DISABLED
# ====================================================
# Bill is now treated as a VIEW (order summary), not a database table
# Using Order as single source of truth for billing
# Model classes commented out to prevent SQLAlchemy initialization errors

# Bill model removed - using Order.to_dict() for bill display
# If you need the Bill table structure, it exists in database but is not used in code

# ====================================================
# BILL SPLIT MODEL - DISABLED  
# ====================================================
# BillSplit model disabled - not using separate Bill table

# BillSplit model removed - split bills not implemented in current version

# ====================================================
# OFFER MODEL
# ====================================================
class Offer(db.Model):
    __tablename__ = 'Offers'
    
    OfferID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OfferCode = db.Column(db.String(50), nullable=True, unique=True)
    OfferName = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.String(1000), nullable=True)
    DiscountType = db.Column(db.String(20), nullable=False)
    DiscountValue = db.Column(db.Numeric(10, 2), nullable=False)
    MinimumBillAmount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    MaximumDiscount = db.Column(db.Numeric(10, 2), nullable=True)
    ValidFrom = db.Column(db.DateTime, nullable=False)
    ValidTo = db.Column(db.DateTime, nullable=False)
    UsageLimit = db.Column(db.Integer, nullable=True)
    UsageCount = db.Column(db.Integer, nullable=False, default=0)
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    order_offers = relationship('OrderOffer', back_populates='offer')
    
    def __repr__(self):
        return f'<Offer {self.OfferName}>'
    
    def to_dict(self):
        return {
            'id': self.OfferID,
            'offer_code': self.OfferCode,
            'offer_name': self.OfferName,
            'description': self.Description,
            'discount_type': self.DiscountType,
            'discount_value': float(self.DiscountValue),
            'minimum_bill_amount': float(self.MinimumBillAmount),
            'maximum_discount': float(self.MaximumDiscount) if self.MaximumDiscount else None,
            'valid_from': self.ValidFrom.isoformat() if self.ValidFrom else None,
            'valid_to': self.ValidTo.isoformat() if self.ValidTo else None,
            'usage_limit': self.UsageLimit,
            'usage_count': self.UsageCount,
            'is_active': self.IsActive
        }

# ====================================================
# ORDER OFFER MODEL (Many-to-Many)
# ====================================================
class OrderOffer(db.Model):
    __tablename__ = 'OrderOffers'
    
    OrderOfferID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('Orders.OrderID'), nullable=False)
    OfferID = db.Column(db.Integer, db.ForeignKey('Offers.OfferID'), nullable=False)
    DiscountAmount = db.Column(db.Numeric(10, 2), nullable=False)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    order = relationship('Order', back_populates='order_offers')
    offer = relationship('Offer', back_populates='order_offers')
    
    def __repr__(self):
        return f'<OrderOffer {self.OrderOfferID}>'
    
    def to_dict(self):
        return {
            'id': self.OrderOfferID,
            'order_id': self.OrderID,
            'offer_id': self.OfferID,
            'discount_amount': float(self.DiscountAmount)
        }

# ====================================================
# FEEDBACK MODEL
# ====================================================
class Feedback(db.Model):
    __tablename__ = 'Feedback'
    
    FeedbackID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('Orders.OrderID'), nullable=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=True)
    MobileNumber = db.Column(db.String(15), nullable=False)
    Rating = db.Column(db.Integer, nullable=False)
    Comment = db.Column(db.String(1000), nullable=True)
    PhotoPath = db.Column(db.String(500), nullable=True)
    FoodQualityRating = db.Column(db.Integer, nullable=True)
    ServiceRating = db.Column(db.Integer, nullable=True)
    AmbienceRating = db.Column(db.Integer, nullable=True)
    IsApproved = db.Column(db.Boolean, nullable=False, default=False)
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    # Relationships - removed back_populates for feedback since Order no longer has feedback relationship
    order = relationship('Order')  # One-way relationship, no back_populates
    user = relationship('User', back_populates='feedbacks')
    
    def __repr__(self):
        return f'<Feedback {self.FeedbackID}>'
    
    def to_dict(self):
        return {
            'id': self.FeedbackID,
            'order_id': self.OrderID,
            'user_id': self.UserID,
            'mobile_number': self.MobileNumber,
            'rating': self.Rating,
            'comment': self.Comment,
            'photo_path': self.PhotoPath,
            'food_quality_rating': self.FoodQualityRating,
            'service_rating': self.ServiceRating,
            'ambience_rating': self.AmbienceRating,
            'is_approved': self.IsApproved,
            'created_at': self.CreatedAt.isoformat() if self.CreatedAt else None
        }

# ====================================================
# CUSTOMER FEEDBACK MODEL (Standalone - No Foreign Keys)
# ====================================================
class CustomerFeedback(db.Model):
    """
    Standalone customer feedback model
    NO foreign keys - simple feedback form
    Independent feedback system with star rating
    """
    __tablename__ = 'CustomerFeedback'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer, nullable=False)  # Star rating 1-5
    message = db.Column(db.Text, nullable=False)  # Feedback message
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CustomerFeedback {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ====================================================
# HOME SLIDE MODEL (Home Page Slider)
# ====================================================
class HomeSlide(db.Model):
    """
    Home page slider slides - fully controlled by admin panel
    Each slide links to a menu item (dish)
    """
    __tablename__ = 'HomeSlides'
    
    SlideID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(200), nullable=True)  # Optional custom title
    DishID = db.Column(db.Integer, db.ForeignKey('MenuItems.MenuItemID'), nullable=False)
    ImagePath = db.Column(db.String(500), nullable=False)
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    DisplayOrder = db.Column(db.Integer, nullable=False, default=0)
    BadgeText = db.Column(db.String(50), nullable=True)  # Optional custom badge
    CreatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    dish = relationship('MenuItem', foreign_keys=[DishID])
    
    def __repr__(self):
        return f'<HomeSlide {self.SlideID} - {self.Title or "Untitled"}>'
    
    def to_dict(self, include_dish=False):
        """Convert slide to dictionary"""
        data = {
            'id': self.SlideID,
            'title': self.Title,
            'dish_id': self.DishID,
            'image_path': self.ImagePath,
            'is_active': self.IsActive,
            'display_order': self.DisplayOrder,
            'badge_text': self.BadgeText,
            'created_at': self.CreatedAt.isoformat() if self.CreatedAt else None
        }
        
        if include_dish and self.dish:
            data['dish'] = self.dish.to_dict()
            # Add dish availability check
            data['dish_available'] = self.dish.IsAvailable and self.dish.IsActive
        
        return data