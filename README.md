# 🍽️ Catering Reservation and Ordering System

A Django-based web application that allows customers to reserve catering services, place food orders, and admins to manage the menu and orders efficiently.

## 🔧 Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Database**: SQLite3
- **Editor**: Atom
- **Authentication**: Django Auth with Role-based Login (Admin / Customer)

---

## 👥 User Roles

### 1. Customer
- Register/Login
- View Menu Items (Food/Drinks)
- Add Items to Cart
- Place and Track Orders
- Make and Manage Reservations
- View/Edit Profile
- Cancel Orders/Reservations
- Payment Integration (UI/Flow Ready)

### 2. Admin
- Custom Dashboard (Not Django Admin)
- Add/Edit/Delete Menu Items
- View All Orders and Reservations
- Upload Product Details with Image and Description

---

## 📁 Folder Structure
shreecatering/ ├── catering_app/ │ ├── templates/ │ │ ├── customer/ │ │ ├── admin/ │ ├── static/ │ │ ├── css/ │ │ ├── js/ ├── db.sqlite3 ├── manage.py


```bash
git clone https://github.com/yourusername/shreecatering.git
cd shreecatering
python manage.py runserver




🧪 Test Cases (Sample)
Test Scenario	Steps to Reproduce	Expected Outcome
Login with valid credentials	1. Go to Login page
2. Enter valid username & password
3. Click Login	User is redirected to their respective dashboard
Add item to cart	1. Login as Customer
2. Browse menu
3. Click "Add to Cart" on any item	Item is added to cart and cart count updates
Place order	1. Go to Cart
2. Click on “Place Order” button	Order is saved and listed under "My Orders"
Admin edits item	1. Login as Admin
2. Go to "View Menu"
3. Click Edit on an item, update	Updated info is shown in customer menu view
