# 🛒 E-Commerce Order & Inventory Management Platform

A full-stack **E-Commerce Order and Inventory Management Platform** designed to manage products, categories, warehouses, inventory, carts, orders, analytics, demand forecasting, and AI-powered assistance.

The platform combines **React, Django REST Framework, FastAPI, MySQL, Redis, Celery, Machine Learning, RAG, Ollama, LangGraph, Docker, and Nginx** into a scalable application architecture.

---

## 🚀 Project Overview

This project provides an end-to-end e-commerce management system where users can:

* Authenticate securely using JWT
* Browse and manage products
* Manage product categories
* Maintain warehouse inventory
* Reserve and release stock
* Add products to carts
* Create and manage orders
* Analyze sales and inventory data
* Forecast product demand using Machine Learning
* Interact with AI-powered services
* Ask questions using RAG-based AI assistance
* Run background tasks using Celery
* Deploy the complete application using Docker

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │   React + Vite UI   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       Nginx         │
                         │   Reverse Proxy     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌───────────────────┐           ┌───────────────────┐
          │ Django REST API   │           │     FastAPI       │
          │                   │           │   AI Services     │
          └─────────┬─────────┘           └─────────┬─────────┘
                    │                               │
          ┌─────────┼──────────┐             ┌──────┼────────┐
          │         │          │             │      │        │
          ▼         ▼          ▼             ▼      ▼        ▼
       MySQL     Redis      Celery         RAG   LangGraph Ollama
          │
          ▼
   Products / Orders
   Inventory / Users
   Analytics
```

---

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* JavaScript
* HTML5
* CSS3

### Backend

* Python
* Django
* Django REST Framework
* FastAPI
* JWT Authentication

### Database

* MySQL

### Background Processing

* Redis
* Celery

### Data & Machine Learning

* Pandas
* NumPy
* Scikit-learn
* Demand Forecasting
* Analytics

### Generative AI

* RAG
* LangGraph
* Ollama
* LLM-based AI services

### DevOps

* Docker
* Docker Compose
* Nginx

---

# ✨ Features

## 🔐 Authentication

* JWT-based authentication
* User login and registration
* Protected API endpoints
* Token-based authorization

---

## 📦 Product Management

* Create products
* Update products
* Delete products
* View product details
* Product categories
* Product search and filtering

---

## 🏭 Warehouse & Inventory Management

The inventory module manages stock across warehouses.

Features include:

* Warehouse management
* Stock tracking
* Inventory updates
* Stock reservation
* Stock release
* Low-stock monitoring
* Inventory availability checks

### Example Flow

```text
Customer places order
        ↓
Check available stock
        ↓
Reserve inventory
        ↓
Create order
        ↓
Confirm order
        ↓
Update inventory
```

---

# 🛒 Cart & Order Management

Users can:

* Add products to cart
* Remove products from cart
* Update quantities
* View cart
* Place orders
* Track order status

### Order Flow

```text
Product
   ↓
Cart
   ↓
Order
   ↓
Inventory Validation
   ↓
Stock Reservation
   ↓
Order Confirmation
```

---

# 📊 Analytics

The platform provides analytics for business and operational insights.

Example metrics:

* Total orders
* Revenue
* Product sales
* Inventory levels
* Order volume
* Product performance
* Warehouse performance
* Customer activity

Pandas is used for data processing and analytics.

---

# 📈 Demand Forecasting

Machine Learning is used to estimate future product demand based on historical sales data.

### Forecasting Flow

```text
Historical Sales Data
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
ML Model
        ↓
Demand Prediction
        ↓
Inventory Planning
```

This can help identify products that may require additional stock.

---

# 🤖 AI & RAG Services

The project includes an AI service built using **FastAPI, RAG, LangGraph, and Ollama**.

Users can interact with the AI service to ask questions related to available application or business data.

### RAG Architecture

```text
User Question
      ↓
FastAPI
      ↓
Query Processing
      ↓
Retriever
      ↓
Relevant Context
      ↓
LLM / Ollama
      ↓
Generated Response
```

RAG helps the system generate responses based on relevant application data rather than relying only on the model's existing knowledge.

---

# 🧠 LangGraph

LangGraph is used to structure AI workflows as a sequence of connected steps.

Example:

```text
User Query
    ↓
Understand Query
    ↓
Retrieve Data
    ↓
Process Context
    ↓
Generate Response
    ↓
Return Answer
```

This approach makes the AI workflow easier to control and extend.

---

# ⚡ Redis & Celery

Redis is used as a fast in-memory data store and message broker.

Celery handles long-running or asynchronous tasks in the background.

Example background tasks:

* Data processing
* Analytics generation
* Forecasting
* AI-related processing
* Scheduled jobs

```text
Django
   ↓
Create Background Task
   ↓
Redis
   ↓
Celery Worker
   ↓
Process Task
```

---

# 🔌 API Architecture

The application separates normal business APIs from AI services.

### Django REST API

Handles:

```text
Authentication
Products
Categories
Inventory
Warehouses
Cart
Orders
Analytics
```

### FastAPI

Handles:

```text
AI Services
RAG
LLM Integration
AI Status
```

---

# 🐳 Docker Deployment

The complete application is containerized using Docker.

Typical services include:

```text
Frontend
Backend
FastAPI
MySQL
Redis
Celery
Nginx
```

This makes the project easier to run consistently across different environments.

---

# 🚀 Quick Start

## Prerequisites

Install:

* Docker
* Docker Compose
* Git

---

## Clone Repository

```bash
git clone https://github.com/NishantSinha720/ecommerce-platform.git

cd ecommerce-platform
```

---

## Start Application

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

---

# 🌐 Application URLs

### Frontend

```text
http://localhost/
```

### Login

```text
http://localhost/login
```

### FastAPI Status

```text
http://localhost/api/v1/status/
```

### AI Service Status

```text
http://localhost/api/v1/ai/status
```

---

# 🔑 Demo Credentials

```text
Username: nishant
Password: nishant123
```

> For production deployments, credentials should always be stored securely using environment variables or a secrets manager.

---

# 📁 High-Level Project Structure

```text
ecommerce-platform/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── ...
│
├── backend/
│   ├── users/
│   ├── products/
│   ├── inventory/
│   ├── orders/
│   ├── analytics/
│   └── ...
│
├── ai/
│   ├── rag/
│   ├── agents/
│   ├── models/
│   └── ...
│
├── docker/
│
├── nginx/
│
├── docker-compose.yml
│
├── requirements.txt
│
└── README.md
```

---

# 🔄 End-to-End Request Flow

A typical user request follows this architecture:

```text
User
 ↓
React
 ↓
Nginx
 ↓
Django REST API
 ↓
Business Logic
 ↓
MySQL
 ↓
Response
 ↓
React UI
```

For AI requests:

```text
User
 ↓
React
 ↓
Nginx
 ↓
FastAPI
 ↓
RAG / LangGraph
 ↓
Ollama / LLM
 ↓
AI Response
 ↓
React
```

---

# 🔒 Security

The project includes:

* JWT authentication
* Protected API endpoints
* Environment-based configuration
* Dockerized services
* Nginx reverse proxy

For production, additional security measures such as HTTPS, secure secrets management, rate limiting, monitoring, and database backups should be configured.

---

# 📌 Key Learning Areas

This project demonstrates practical experience with:

* Full-stack application development
* REST API development
* Django & FastAPI
* SQL database design
* Authentication
* Inventory management
* Order processing
* Background task processing
* Redis & Celery
* Data analytics
* Machine Learning
* Demand forecasting
* RAG pipelines
* LLM integration
* LangGraph workflows
* Docker
* Nginx
* Scalable application architecture

---

# 🔮 Future Improvements

Possible future enhancements include:

* Payment gateway integration
* Elasticsearch-based product search
* Real-time order tracking
* Recommendation system
* Advanced demand forecasting
* Kubernetes deployment
* Cloud deployment
* Monitoring with Prometheus/Grafana
* Role-based access control
* Advanced AI agents
* Automated inventory replenishment

---

# 👨‍💻 Author

**Nishant Sinha**

Python Developer | Data Science | Generative AI | Backend Development

GitHub: https://github.com/NishantSinha720

Repository: https://github.com/NishantSinha720/ecommerce-platform

---

# 📄 License

This project is intended for **educational and portfolio purposes**.
