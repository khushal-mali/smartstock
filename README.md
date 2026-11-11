# SmartStock – Inventory Management System

**SmartStock** is a full-stack web-based Inventory Management System built specifically for small retail shops and warehouses, implemented according to the **BCA Semester V Project Synopsis** submitted to **Uttaranchal University**.

---

## 🌟 Key Features (Mapped to Synopsis Modules)

1. **Module 1: Authentication & Role-Based Access Control (RBAC)**
   - Secure login using JSON Web Tokens (JWT) and `bcrypt` password hashing.
   - Dual-role permissions: **Admin** (full management) and **Staff** (sales billing and restocking).
   - Dedicated User Management panel for Admins.

2. **Module 2: Product & Supplier Directory**
   - Unique SKU tracking, categories, unit prices, and customizable **reorder levels**.
   - Supplier records with direct phone numbers and emails for easy reordering.
   - Real-time stock status pills (`In Stock` vs `Low Stock`).

3. **Module 3: Purchases & Restocking (Stock Inflow)**
   - Multi-item purchase order entry.
   - Atomic database transactions (`prisma.$transaction`) that automatically increment warehouse inventory levels.
   - Complete historical log of purchase orders with itemized breakdowns.

4. **Module 4: Sales Billing & Invoicing (Stock Outflow)**
   - Interactive Point-of-Sale (POS) counter.
   - Pre-sale stock validation (blocks sales if requested quantity exceeds available stock).
   - Atomic database transactions that deduct quantities and assign sequential tax invoices (`INV-YYYYMM-XXXX`).
   - Printable tax invoice generator with company header and totals.

5. **Module 5: Real-Time Alerts & Audit Reports**
   - **Dashboard**: Live metrics on total inventory valuation, catalog items, revenue, and active low-stock alerts.
   - **4 Tabbed Reports**:
     1. *Stock Summary Report*: Detailed stock quantities and total monetary valuation per product.
     2. *Low-Stock Report*: Identifies all items at or below reorder levels with supplier contact info.
     3. *Purchases Report*: Procurements filterable by date range.
     4. *Sales Report*: Revenue and invoices filterable by date range.
   - One-click "Print / Export PDF" for all reports.

---

## 🛠️ Technology Stack

* **Frontend**: Next.js 14+ (App Router), React 19, Tailwind CSS, Lucide Icons, Axios.
* **Backend**: NestJS REST API, TypeScript, Class-Validator, Passport JWT.
* **Database**: PostgreSQL 18.
* **ORM**: Prisma 6 (Schema, Migrations, Seed, Client).

---

## 🚀 Quick Start Guide

### 1. Prerequisites
* Node.js (v18+)
* PostgreSQL running locally on `localhost:5432`

### 2. Database Setup & Seeding
From the `backend/` directory:
```bash
cd backend
npm install
npx prisma migrate dev --name init
npx prisma db seed
```

### 3. Run the Backend API Server
```bash
cd backend
npm run start:dev
# Or production build:
npm run start:prod
```
*API Base URL*: `http://localhost:5000/api`

### 4. Run the Frontend Client
```bash
cd frontend
npm install
npm run dev
# Or production build:
npm run build
npm run start
```
*Web App URL*: `http://localhost:3000`

---

## 🔑 Demo Credentials

| Role | Email Address | Password | Permissions |
|---|---|---|---|
| **Admin** | `admin@smartstock.com` | `admin123` | Full Access (Products, Users, Reports, Restock, POS) |
| **Staff** | `staff@smartstock.com` | `staff123` | Sales Billing (POS), Purchase Entry, Inventory Views |

*(Quick-fill demo buttons are also provided directly on the Login screen for testing).*

