-- ====================================================
-- RESTAURANT BILLING & POS SYSTEM
-- SQLite Database Schema
-- Production-Ready, Normalized Structure
-- ====================================================

-- ====================================================
-- 1. MEMBERSHIPS TABLE
-- ====================================================
CREATE TABLE Memberships (
    MembershipID INTEGER PRIMARY KEY AUTOINCREMENT,
    MembershipName TEXT NOT NULL UNIQUE,
    DiscountPercentage NUMERIC(5,2) NOT NULL DEFAULT 0.00,
    MinimumOrderAmount NUMERIC(10,2) DEFAULT 0.00,
    IsActive INTEGER NOT NULL DEFAULT 1 CHECK(IsActive IN (0, 1)),
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL,
    CHECK (DiscountPercentage >= 0 AND DiscountPercentage <= 100),
    CHECK (MinimumOrderAmount >= 0)
);

-- ====================================================
-- 2. USERS TABLE (Guest + Registered)
-- ====================================================
CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    MobileNumber TEXT NOT NULL UNIQUE,
    FullName TEXT NULL,
    Email TEXT NULL,
    PhotoPath TEXT NULL,
    MembershipID INTEGER NULL,
    IsGuest INTEGER NOT NULL DEFAULT 1 CHECK(IsGuest IN (0, 1)),
    IsActive INTEGER NOT NULL DEFAULT 1 CHECK(IsActive IN (0, 1)),
    OTP TEXT NULL,
    OTPExpiry TIMESTAMP NULL,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL,
    FOREIGN KEY (MembershipID) REFERENCES Memberships(MembershipID),
    CHECK (LENGTH(TRIM(MobileNumber)) >= 10)
);

-- ====================================================
-- 3. ADMINS TABLE
-- ====================================================
CREATE TABLE Admins (
    AdminID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,
    PasswordHash TEXT NOT NULL,
    FullName TEXT NOT NULL,
    Email TEXT NULL,
    MobileNumber TEXT NULL,
    IsSuperAdmin INTEGER NOT NULL DEFAULT 0 CHECK(IsSuperAdmin IN (0, 1)),
    IsActive INTEGER NOT NULL DEFAULT 1 CHECK(IsActive IN (0, 1)),
    LastLogin TIMESTAMP NULL,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL
);

-- ====================================================
-- 4. RESTAURANT TABLES TABLE
-- ====================================================
CREATE TABLE RestaurantTables (
    TableID INTEGER PRIMARY KEY AUTOINCREMENT,
    TableNumber TEXT NOT NULL UNIQUE,
    Capacity INTEGER NOT NULL DEFAULT 4,
    Status TEXT NOT NULL DEFAULT 'Free' CHECK(Status IN ('Free', 'Occupied', 'Reserved', 'Maintenance')),
    GroupID INTEGER NULL,
    QRCodePath TEXT NULL,
    CurrentOrderID INTEGER NULL,
    Notes TEXT NULL,
    IsActive INTEGER NOT NULL DEFAULT 1 CHECK(IsActive IN (0, 1)),
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL,
    CHECK (Capacity > 0 AND Capacity <= 20)
);

-- ====================================================
-- 5. TABLE RESERVATIONS TABLE
-- ====================================================
CREATE TABLE TableReservations (
    ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
    TableID INTEGER NOT NULL,
    UserID INTEGER NULL,
    MobileNumber TEXT NOT NULL,
    CustomerName TEXT NOT NULL,
    ReservationDate TIMESTAMP NOT NULL,
    ReservationTime TIME NOT NULL,
    NumberOfGuests INTEGER NOT NULL,
    Status TEXT NOT NULL DEFAULT 'Pending' CHECK(Status IN ('Pending', 'Confirmed', 'Cancelled', 'Completed')),
    SpecialRequests TEXT NULL,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL,
    FOREIGN KEY (TableID) REFERENCES RestaurantTables(TableID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    CHECK (NumberOfGuests > 0)
);

-- ====================================================
-- 6. MENU ITEMS TABLE
-- ====================================================
CREATE TABLE MenuItems (
    MenuItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemName TEXT NOT NULL,
    ItemCode TEXT NULL UNIQUE,
    Description TEXT NULL,
    Category TEXT NOT NULL,
    Price NUMERIC(10,2) NOT NULL,
    GSTPercentage NUMERIC(5,2) NOT NULL DEFAULT 5.00,
    PreparationTime INTEGER NULL,
    IsVegetarian INTEGER NOT NULL DEFAULT 0 CHECK(IsVegetarian IN (0, 1)),
    IsVegan INTEGER NOT NULL DEFAULT 0 CHECK(IsVegan IN (0, 1)),
    IsSpicy INTEGER NOT NULL DEFAULT 0 CHECK(IsSpicy IN (0, 1)),
    IsAvailable INTEGER NOT NULL DEFAULT 1 CHECK(IsAvailable IN (0, 1)),
    IsActive INTEGER NOT NULL DEFAULT 1 CHECK(IsActive IN (0, 1)),
    DisplayOrder INTEGER NULL DEFAULT 0,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL,
    CHECK (Price >= 0),
    CHECK (GSTPercentage >= 0 AND GSTPercentage <= 100),
    CHECK (PreparationTime IS NULL OR PreparationTime >= 0)
);

-- ====================================================
-- 7. MENU PHOTOS TABLE (Multiple images per item)
-- ====================================================
CREATE TABLE MenuPhotos (
    PhotoID INTEGER PRIMARY KEY AUTOINCREMENT,
    MenuItemID INTEGER NOT NULL,
    PhotoPath TEXT NOT NULL,
    IsPrimary INTEGER NOT NULL DEFAULT 0 CHECK(IsPrimary IN (0, 1)),
    DisplayOrder INTEGER NOT NULL DEFAULT 0,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (MenuItemID) REFERENCES MenuItems(MenuItemID) ON DELETE CASCADE
);

-- ====================================================
-- 8. ORDERS TABLE
-- ====================================================
CREATE TABLE Orders (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderNumber TEXT NOT NULL UNIQUE,
    TableID INTEGER NOT NULL,
    UserID INTEGER NULL,
    MobileNumber TEXT NOT NULL,
    OrderStatus TEXT NOT NULL DEFAULT 'Pending' CHECK(OrderStatus IN ('Pending', 'Preparing', 'Ready', 'Served', 'Completed', 'Cancelled')),
    OrderType TEXT NOT NULL DEFAULT 'DineIn' CHECK(OrderType IN ('DineIn', 'Takeaway', 'Delivery')),
    SubTotal NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    GSTAmount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    MembershipDiscount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    OfferDiscount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    TotalAmount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    SpecialInstructions TEXT NULL,
    KitchenNotes TEXT NULL,
    OrderPlacedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    OrderPreparedAt TIMESTAMP NULL,
    OrderServedAt TIMESTAMP NULL,
    OrderCompletedAt TIMESTAMP NULL,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL,
    FOREIGN KEY (TableID) REFERENCES RestaurantTables(TableID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    CHECK (SubTotal >= 0 AND GSTAmount >= 0 AND TotalAmount >= 0)
);

-- ====================================================
-- 9. ORDER ITEMS TABLE
-- ====================================================
CREATE TABLE OrderItems (
    OrderItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderID INTEGER NOT NULL,
    MenuItemID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL DEFAULT 1,
    UnitPrice NUMERIC(10,2) NOT NULL,
    GSTPercentage NUMERIC(5,2) NOT NULL,
    GSTAmount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    ItemSubTotal NUMERIC(10,2) NOT NULL,
    SpecialInstructions TEXT NULL,
    ItemStatus TEXT NOT NULL DEFAULT 'Pending' CHECK(ItemStatus IN ('Pending', 'Preparing', 'Ready', 'Served', 'Cancelled')),
    SplitBillID INTEGER NULL,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (MenuItemID) REFERENCES MenuItems(MenuItemID),
    CHECK (Quantity > 0),
    CHECK (UnitPrice >= 0)
);

-- ====================================================
-- 10. BILLS TABLE
-- ====================================================
CREATE TABLE Bills (
    BillID INTEGER PRIMARY KEY AUTOINCREMENT,
    BillNumber TEXT NOT NULL UNIQUE,
    OrderID INTEGER NOT NULL,
    TableID INTEGER NOT NULL,
    UserID INTEGER NULL,
    MobileNumber TEXT NOT NULL,
    BillDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    SubTotal NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    GSTAmount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    MembershipDiscount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    OfferDiscount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    TotalAmount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    PaymentMethod TEXT NULL,
    PaymentStatus TEXT NOT NULL DEFAULT 'Pending' CHECK(PaymentStatus IN ('Pending', 'Paid', 'Partial', 'Refunded')),
    PaidAmount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    IsSplitBill INTEGER NOT NULL DEFAULT 0 CHECK(IsSplitBill IN (0, 1)),
    SplitBillID INTEGER NULL,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (TableID) REFERENCES RestaurantTables(TableID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    CHECK (SubTotal >= 0 AND GSTAmount >= 0 AND TotalAmount >= 0 AND PaidAmount >= 0)
);

-- ====================================================
-- 11. BILL SPLITS TABLE (For split bill tracking)
-- ====================================================
CREATE TABLE BillSplits (
    SplitBillID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderID INTEGER NOT NULL,
    SplitNumber INTEGER NOT NULL,
    UserID INTEGER NULL,
    MobileNumber TEXT NOT NULL,
    SubTotal NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    GSTAmount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    TotalAmount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    PaymentStatus TEXT NOT NULL DEFAULT 'Pending',
    PaidAmount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    CHECK (SubTotal >= 0 AND GSTAmount >= 0 AND TotalAmount >= 0)
);

-- ====================================================
-- 12. OFFERS TABLE
-- ====================================================
CREATE TABLE Offers (
    OfferID INTEGER PRIMARY KEY AUTOINCREMENT,
    OfferCode TEXT NULL UNIQUE,
    OfferName TEXT NOT NULL,
    Description TEXT NULL,
    DiscountType TEXT NOT NULL CHECK(DiscountType IN ('Percentage', 'FixedAmount')),
    DiscountValue NUMERIC(10,2) NOT NULL,
    MinimumBillAmount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    MaximumDiscount NUMERIC(10,2) NULL,
    ValidFrom TIMESTAMP NOT NULL,
    ValidTo TIMESTAMP NOT NULL,
    UsageLimit INTEGER NULL,
    UsageCount INTEGER NOT NULL DEFAULT 0,
    IsActive INTEGER NOT NULL DEFAULT 1 CHECK(IsActive IN (0, 1)),
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL,
    CHECK (DiscountValue >= 0),
    CHECK (MinimumBillAmount >= 0),
    CHECK (ValidTo > ValidFrom)
);

-- ====================================================
-- 13. ORDER OFFERS TABLE (Many-to-Many: Orders & Offers)
-- ====================================================
CREATE TABLE OrderOffers (
    OrderOfferID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderID INTEGER NOT NULL,
    OfferID INTEGER NOT NULL,
    DiscountAmount NUMERIC(10,2) NOT NULL,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (OfferID) REFERENCES Offers(OfferID),
    CHECK (DiscountAmount >= 0)
);

-- ====================================================
-- 14. FEEDBACK TABLE
-- ====================================================
CREATE TABLE Feedback (
    FeedbackID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderID INTEGER NULL,
    UserID INTEGER NULL,
    MobileNumber TEXT NOT NULL,
    Rating INTEGER NOT NULL,
    Comment TEXT NULL,
    PhotoPath TEXT NULL,
    FoodQualityRating INTEGER NULL,
    ServiceRating INTEGER NULL,
    AmbienceRating INTEGER NULL,
    IsApproved INTEGER NOT NULL DEFAULT 0 CHECK(IsApproved IN (0, 1)),
    IsActive INTEGER NOT NULL DEFAULT 1 CHECK(IsActive IN (0, 1)),
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    CHECK (Rating >= 1 AND Rating <= 5),
    CHECK (FoodQualityRating IS NULL OR (FoodQualityRating >= 1 AND FoodQualityRating <= 5)),
    CHECK (ServiceRating IS NULL OR (ServiceRating >= 1 AND ServiceRating <= 5)),
    CHECK (AmbienceRating IS NULL OR (AmbienceRating >= 1 AND AmbienceRating <= 5))
);

-- ====================================================
-- INDEXES FOR PERFORMANCE
-- ====================================================
CREATE INDEX IX_Users_MobileNumber ON Users(MobileNumber);
CREATE INDEX IX_Users_MembershipID ON Users(MembershipID);
CREATE INDEX IX_RestaurantTables_Status ON RestaurantTables(Status);
CREATE INDEX IX_RestaurantTables_GroupID ON RestaurantTables(GroupID);
CREATE INDEX IX_Orders_TableID ON Orders(TableID);
CREATE INDEX IX_Orders_UserID ON Orders(UserID);
CREATE INDEX IX_Orders_OrderStatus ON Orders(OrderStatus);
CREATE INDEX IX_Orders_OrderPlacedAt ON Orders(OrderPlacedAt);
CREATE INDEX IX_OrderItems_OrderID ON OrderItems(OrderID);
CREATE INDEX IX_OrderItems_MenuItemID ON OrderItems(MenuItemID);
CREATE INDEX IX_OrderItems_ItemStatus ON OrderItems(ItemStatus);
CREATE INDEX IX_Bills_OrderID ON Bills(OrderID);
CREATE INDEX IX_Bills_TableID ON Bills(TableID);
CREATE INDEX IX_Bills_BillDate ON Bills(BillDate);
CREATE INDEX IX_MenuItems_Category ON MenuItems(Category);
CREATE INDEX IX_MenuItems_IsAvailable ON MenuItems(IsAvailable);
CREATE INDEX IX_TableReservations_ReservationDate ON TableReservations(ReservationDate);
CREATE INDEX IX_TableReservations_Status ON TableReservations(Status);

-- ====================================================
-- DEFAULT DATA INSERTION
-- ====================================================

-- Insert default membership types
INSERT INTO Memberships (MembershipName, DiscountPercentage, MinimumOrderAmount) VALUES
('Silver', 5.00, 500.00),
('Gold', 10.00, 1000.00),
('Platinum', 15.00, 2000.00);

-- Insert default admin (password should be hashed in application)
-- Username: admin, Password: admin123 (to be hashed)
-- Note: Update this password hash with actual bcrypt hash in application
INSERT INTO Admins (Username, PasswordHash, FullName, IsSuperAdmin) VALUES
('admin', 'PLACEHOLDER_HASH', 'System Administrator', 1);

-- ====================================================
-- END OF SCHEMA
-- ====================================================
