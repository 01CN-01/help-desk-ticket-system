🛠️ Help Desk Ticket System  
Python | SQLite | SQL | Authentication | Role-Based Access | Logging

A backend-focused **CLI Help Desk Ticket System** built with **Python** and **SQLite**.  
The application demonstrates real-world backend fundamentals including **user authentication**, **secure password hashing**, **role-based access control**, **SQL CRUD operations**, and **defensive error handling**.

This project is designed to showcase skills relevant to **junior software developer / backend developer roles**.

---

## 🔍 Project Overview

The Help Desk Ticket System allows users to register, log in, and manage support tickets through a command-line interface.

The system enforces **ownership rules and permissions** to ensure:
- Standard users can only manage their **own tickets**
- Staff/Admin users can manage **all tickets**
- Data access is restricted and validated at both the **application** and **database** level

All data is persisted using SQLite, with a focus on **secure queries** and **reliable backend logic**.

---

## ✅ Key Features

### 🔐 User Authentication & Roles
- User registration and login
- Secure password hashing using **bcrypt**
- Role-based access control:
  - **User** – create, view, edit, and delete own tickets
  - **Staff/Admin** – manage all tickets

---

### 🎫 Ticket Management (CRUD)
- Create support tickets
- View tickets:
  - Own tickets (User)
  - All tickets (Staff/Admin)
- Edit tickets with ownership validation
- Delete tickets safely using `cursor.rowcount` verification
- Automatic ticket timestamps via SQLite

---

### 🗄️ Database & SQL
- SQLite database with persistent storage
- Parameterised SQL queries to prevent SQL injection
- Secure `UPDATE` and `DELETE` operations using:
  - `WHERE` constraints
  - Row-count validation to confirm successful operations
- Ownership and permission checks enforced at query level

---

### 🛡️ Logging & Error Handling
- Application logging for key actions:
  - User login
  - Ticket creation
  - Ticket updates
  - Ticket deletion
- Centralised input validation for:
  - Integers
  - Email format
  - Password strength
- Defensive programming to handle:
  - Invalid input
  - Non-existent records
  - Permission violations
- Prevents crashes and inconsistent application state

---

## 🧱 Tech Stack
- **Python 3**
- **SQLite**
- **SQL**
- **bcrypt**
- **Command Line Interface (CLI)**

---

## 🗄️ Database Schema

### Users Table
| Column     | Description                    |
|------------|--------------------------------|
| studentid  | Primary key                    |
| firstname  | User first name                |
| lastname   | User last name                 |
| email      | Login email                    |
| password   | Hashed password                |
| role       | User / Staff                   |

---

### Tickets Table
| Column      | Description                          |
|-------------|--------------------------------------|
| ticketid    | Primary key                          |
| created_by  | User ID (foreign key)                |
| subject     | Ticket subject                       |
| description | Ticket description                   |
| created_at  | Auto-generated timestamp             |

---

## ▶️ Running the Project

1. Ensure Python 3 is installed
2. Install dependencies:
```bash
pip install bcrypt
