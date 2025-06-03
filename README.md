# 🛒 Simple E-commerce App

A simple backend system for an e-commerce application. This project demonstrates the core concepts of building a RESTful API for an online store, including:

- User authentication
- Product management
- Shopping carts
- Order processing

---

## 🚀 Technologies Used

| Area                  | Tools/Technologies                       |
|-----------------------|------------------------------------------|
| **Framework**         | FastAPI                                  |
| **Database**          | SQLAlchemy, PostgreSQL, AsyncPG, Pydantic |
| **Caching**           | Redis, AioRedis                          |
| **Rate Limiting**     | SlowAPI                                  |
| **Security / JWT**    | Bcrypt, Authlib (JWT)                    |
| **Testing**           | PyTest                                   |
| **Reverse Proxy**     | Nginx                                    |
| **Containerization**  | Docker, Docker Compose                   |
| **Migrations**        | Alembic                                  |
| **Monitoring / Logs** | Prometheus, Grafana                      |

---

## 📦 Deployment

1. **Install Docker**  
   Make sure Docker and Docker Compose are installed on your system.

2. **Build and Run Containers**
   ```bash
   docker compose up --build
