# AgroYantra – Complete User Guide

## Table of Contents
1. [Customer Guide](#customer-guide)
2. [Staff Guide](#staff-guide)
3. [Admin Guide](#admin-guide)
4. [User Roles & Permissions](#roles)

---

## 1. Customer Guide

### Creating an Account
1. Go to **agroyantra.com.np** and click **Get Started**
2. Fill in your name, phone, email, and password
3. Click **Create Account** — you are logged in immediately

### Browsing Products
- Use the **Products** menu or top search bar
- Filter by **Category** or **Availability** in the left sidebar
- Products show availability badges:
  - 🟢 **In Stock** — ready to ship
  - 🔵 **On Order** — procured on request
  - 🟣 **Overseas / Import** — international order, see lead time
- If no price is shown, click **Enquire** to contact us

### Adding to Cart & Checkout
1. Click **Add to Cart** on any orderable product
2. Go to **Cart** to review — adjust quantities with +/–
3. Click **Proceed to Checkout**
4. Fill your delivery address and review the order
5. Click **Place Order** — payment is **Cash on Delivery**

### Tracking Your Order
- Go to **My Account → My Orders**
- Order statuses: New → Confirmed → Processing → Dispatched → Delivered
- Delivered = COD collected by our team

### Contacting Us
- **Products/Enquiry**: Use the **Enquire** button on any product page
- **Projects/Consulting**: Go to **Contact** page and select your enquiry type
- Phone: +977-XXXXXXXXXX (Sun–Fri, 9AM–6PM)

---

## 2. Staff Guide

### Logging In
- Go to **/backend/** and log in with your staff credentials
- You must have **Staff** role assigned by the admin

### Staff Dashboard
Shows: total orders, new orders awaiting action, dispatched orders, revenue, product count, low stock alerts

### Managing Orders

**Order Statuses & What They Mean:**
| Status | Meaning | Action Required |
|--------|---------|-----------------|
| New | Customer placed order | Review and confirm |
| Confirmed | Order accepted | Prepare items |
| Processing | Being packed | Update when ready to ship |
| Dispatched | Out for delivery | Add vehicle/driver details |
| Delivered | Delivered + COD collected | No action |
| Cancelled | Order cancelled | No action |

**To update an order:**
1. Go to **Backend → Orders**
2. Click **Manage** on any order
3. Change status using the dropdown on the right
4. Add delivery details (vehicle number, driver, assign staff)
5. Click **Save**

### Printing Delivery Documents
1. Open any order in the backend
2. Click **Print Delivery Document** (top right)
3. A print-ready document opens in a new tab with:
   - Company header
   - Customer delivery address
   - Full itemized order list
   - COD collection amount
   - Signature fields for staff, driver, and customer
4. Click **🖨 Print Document**

### Managing Products (Backend View)
- Go to **Backend → Products** to see all products with status, availability, price visibility
- Click **Edit** to go to Django Admin to edit that product
- Click **Add Product** to create a new listing

### Gallery Management
- Go to **Django Admin → Gallery → Albums**
- Create albums (e.g., "Greenhouse Projects 2024")
- Add images inside each album with title and caption
- Images appear on the public **Gallery** page

---

## 3. Admin Guide (Full Access)

### Accessing Django Admin
- Go to **/admin/** with superuser credentials
- Full control over all models

### Creating Staff Accounts
1. Go to **/admin/accounts/account/add/**
2. Fill name, email, password
3. Set **Is Staff** = ✓
4. Set **Role** = staff
5. Click Save

### Product Management — Key Fields
| Field | Purpose |
|-------|---------|
| **Product Name** | Required. Must be unique. |
| **Slug** | Auto-fills. URL-safe identifier. |
| **Category** | Select or create in Django Admin |
| **Price** | Leave blank or set a value |
| **Show Price** | ✓ = show price on site. ✗ = show "Contact for Price" |
| **Discount Price** | Optional. Shows crossed-out original price if set |
| **Availability** | In Stock / On Order / Overseas / Out of Stock / Discontinued |
| **Overseas Lead Time** | e.g. "4–6 weeks" — shown on product page for import items |
| **Min Order Quantity** | Default 1. For bulk-only items, set higher |
| **Is Available** | ✓ = visible on site. ✗ = hidden (draft) |
| **Is Featured** | ✓ = shows "Featured" badge, appears first in listings |
| **Meta Title / Description / Keywords** | For SEO. Leave blank to auto-generate |
| **Specifications** | One spec per line in format "Power: 20HP" |

### SEO Tips
- Fill **Meta Title** (under 60 chars) and **Meta Description** (under 155 chars)
- Use keywords like: nepal, agritech, equipment name, sector
- Slug is auto-generated from product name — keep it clean

### Category Management
- Go to **/admin/categories/category/**
- Each category has: name, slug, description, optional image
- Categories appear in the product filter sidebar and homepage

### Gallery Management
- Go to **/admin/gallery/**
- Create **Albums** first (e.g., "Poultry Unit - Chitwan 2024")
- Add **Images** to each album with caption
- Set **Order** field to control display sequence
- Set **Is Active** = False to hide without deleting

---

## 4. User Roles & Permissions

| Role | Access |
|------|--------|
| **Customer** | Browse, cart, checkout, view own orders, edit own profile |
| **Staff** | All customer access + `/backend/` dashboard, manage orders, print delivery docs, view products & staff |
| **Admin / Superuser** | All of the above + Django `/admin/` full control over all data |

### Role Assignment
- Default on registration: **Customer**
- To make a user **Staff**: Django Admin → Accounts → [user] → Set `Is Staff = True`
- To make a user **Admin**: Set `Is Admin = True` and `Is Superadmin = True`

---

## Quick Reference

### URLs
| URL | Purpose |
|-----|---------|
| `/` | Homepage |
| `/products/` | Product catalogue |
| `/gallery/` | Project photo gallery |
| `/aboutus/` | About / Services |
| `/orders/my-orders/` | Customer order tracking |
| `/accounts/login/` | Login |
| `/backend/` | Staff dashboard |
| `/backend/orders/` | Order management |
| `/backend/orders/[NUM]/delivery-doc/` | Printable delivery document |
| `/admin/` | Django admin (admin only) |

### Common Tasks – Quick Steps
- **Add new product**: `/admin/products/product/add/`
- **Add category**: `/admin/categories/category/add/`
- **Add gallery album**: `/admin/gallery/galleryalbum/add/`
- **Create staff user**: `/admin/accounts/account/add/` → set is_staff=True
- **Print delivery doc**: Backend → Order → Print Delivery Document
- **Hide product price**: Edit product → uncheck "Show Price"
- **Mark as overseas**: Edit product → Availability = "Overseas / Import Order" → set Lead Time
