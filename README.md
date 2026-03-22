# 📚 FastAPI Library Book Management System

## 🚀 Project Overview

This project is a **Library Book Management System Backend API** built using **FastAPI**. It allows users to manage books, borrow and return them, and perform advanced operations like search, filtering, sorting, and pagination.

---

## 🎯 Features

### 📖 Book Management

* Get all books
* Get book by ID
* Add new book
* Update book details
* Delete book

### 👤 Borrowing System

* Borrow a book
* Return a book
* Maintain borrow records

### 🔄 Workflow System

* Queue system for unavailable books
* Automatic reassignment when book is returned

### 🔍 Advanced Features

* Search books by keyword
* Filter books by genre/author
* Sort books
* Pagination
* Combined browse API

---

## 🛠️ Technologies Used

* FastAPI
* Python
* Pydantic
* Uvicorn

---

## 📂 Project Structure

project/
│── main.py
│── requirements.txt
│── README.md
│── screenshots/

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

git clone https://github.com/your-username/fastapi-library-book-management.git
cd fastapi-library-book-management

### 2️⃣ Install Dependencies

pip install -r requirements.txt

### 3️⃣ Run Server

uvicorn main:app --reload

### 4️⃣ Open API Docs

http://127.0.0.1:8000/docs

---

## 📸 Screenshots

All API endpoints are tested using Swagger UI.
Screenshots are available in the **screenshots/** folder.

---

## 📊 API Endpoints

* GET APIs (Home, Books, Summary)
* POST APIs (Add Book, Borrow)
* PUT APIs (Update Book)
* DELETE APIs (Delete Book)
* Workflow APIs (Queue, Return)
* Advanced APIs (Search, Filter, Sort, Pagination)

---

## 🎓 Learning Outcomes

* Built REST APIs using FastAPI
* Implemented CRUD operations
* Designed multi-step workflows
* Applied data validation using Pydantic
* Implemented search, sorting, and pagination

---

## 🙌 Acknowledgment

Grateful for the learning opportunity at **Innomatics Research Labs**.

---

## 📬 Contact

For any queries, feel free to connect.
