FastAPI Internship – Assignment 1

This repository contains the solution for FastAPI Internship – Day 1 Assignment.
The assignment demonstrates basic API development using FastAPI, including filtering, searching, and summarizing product data.

---

📌 Project Overview

A simple E-commerce Store API built using FastAPI.

The API allows users to:

- View all products
- Filter products by category
- View only in-stock products
- Get a store summary
- Search products by name
- View cheapest and most expensive products (Bonus)

---

 Technologies Used

- Python
- FastAPI
- Uvicorn
- Swagger UI (for API testing)

---

📂 Project Structure

YOUR_UNIQUE_INTERNID_FASTAPI
└── ASSIGNMENT 1
    ├── main.py
    ├── Q1_Output.png
    ├── Q2_Output.png
    ├── Q3_Output.png
    ├── Q4_Output.png
    ├── Q5_Output.png
    └── Bonus_Output.png

---

 API Endpoints

## 1️ Get All Products

Endpoint

GET /products

Returns the complete product list and total count.

---

##  2️ Filter Products by Category

Endpoint

GET /products/category/{category_name}

Example:

/products/category/Electronics

Returns only products belonging to that category.

---

## 3️ Show In-Stock Products

Endpoint

GET /products/instock

Returns only products that are currently available in stock.

---

## 4️ Store Summary

Endpoint

GET /store/summary

Returns:

- Total number of products
- Number of products in stock
- Number of products out of stock
- List of product categories

---

## 5️ Search Products

Endpoint

GET /products/search/{keyword}

Example:

/products/search/mouse

Search is case-insensitive.

---

⭐ Bonus Endpoint

Cheapest & Most Expensive Products

Endpoint

GET /products/deals

Returns:

- Best deal (lowest price)
- Premium pick (highest price)

---

##  Running the Project from Scratch

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git

2. Navigate to Project Folder

cd YOUR_REPOSITORY_NAME/ASSIGNMENT\ 1

3. Install Required Packages

pip install fastapi uvicorn

4. Run the Server

uvicorn main:app --reload

---

🌐 API Documentation

After running the server, open:

Swagger UI:

http://127.0.0.1:8000/docs

All API endpoints can be tested directly from Swagger UI.

---

## Screenshots

Output screenshots for each task are included in the ASSIGNMENT 1 folder as required for submission.
