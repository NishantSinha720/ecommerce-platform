# E-Commerce Order & Inventory Management Platform

**Built by Nishant Sinha**

A full-stack e-commerce platform for product management, inventory, orders, analytics, demand forecasting, and AI-powered services.

## Tech Stack

React • Django • Django REST Framework • FastAPI • MySQL • Redis • Celery • Pandas • scikit-learn • RAG • Ollama • LangGraph • Docker • Nginx

## Features

- JWT Authentication
- Product & Category Management
- Warehouse & Inventory Management
- Stock Reservation & Release
- Cart & Order Management
- Analytics & Demand Forecasting
- AI / RAG Services
- Redis & Celery Background Processing
- React + Vite Frontend
- Dockerized Deployment

## Architecture

``text
React + Vite
     ↓
   Nginx
     ↓
Django REST Framework
     ├── MySQL
     ├── Redis + Celery
     └── Orders / Inventory / Analytics

FastAPI
     ├── AI
     ├── RAG
     └── Ollama
``

## Quick Start

``powershell
docker compose up -d --build
``

## Application

Frontend: http://localhost/

Login: http://localhost/login

FastAPI: http://localhost/api/v1/status/

AI: http://localhost/api/v1/ai/status

## Demo Login

Username: nishant
Password: nishant123

## Author

**Nishant Sinha**

GitHub: https://github.com/NishantSinha720

Repository: https://github.com/NishantSinha720/ecommerce-platform

## License

Educational and portfolio project.
