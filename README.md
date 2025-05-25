# Resume Analyzer API (FastAPI)

A microservice built with **FastAPI** that analyzes resumes (PDF/DOCX) and extracts skills. This project demonstrates modern backend practices and applies the **12-Factor App** principles.

---

## 👨‍💻 Tech Stack Used

<p align="center">
  <img src="https://img.shields.io/badge/-FastAPI-009688?logo=fastapi&logoColor=white&style=for-the-badge" />
  <img src="https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=fff&style=for-the-badge" />
  <img src="https://img.shields.io/badge/-Pydantic-0A0A0A?logo=pydantic&logoColor=white&style=for-the-badge" />
  <img src="https://img.shields.io/badge/-SQLAlchemy-CC0000?logo=sqlalchemy&logoColor=white&style=for-the-badge" />
  <img src="https://img.shields.io/badge/-AsyncIO-3776AB?logo=python&logoColor=white&style=for-the-badge" />
  <img src="https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white&style=for-the-badge" />
  <img src="https://img.shields.io/badge/-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white&style=for-the-badge" />
  <img src="https://img.shields.io/badge/-pytest-0A0A0A?logo=pytest&logoColor=white&style=for-the-badge" />

</p>

---

## 🚀 Features

- 📄 Upload PDF or DOCX resumes
- 🧠 Analyze resume content to extract:
  - Detected skills
  - Word/sentence count
- 🔄 Background processing using FastAPI’s `BackgroundTasks`
- ⚡ Async endpoints and DB operations
- 🧪 Pytest-based test coverage
- 🐳 Dockerized with optional Docker Compose
- 📋 CI/CD with GitHub Actions
- ✅ Clean architecture using FastAPI routers & dependencies
- 🧾 Follows 12-Factor principles

---


## 📁 Project Structure

```
resume-analyzer-fastapi/
│
├── app/                 
│   ├── core/                # Config, logging, dependencies
│   ├── services/            # Business logic: parsing, analysis
│   ├── models/              # Pydantic and ORM models
│   ├── db/                  # DB session and setup
│   └── main.py              # FastAPI entry point
│
├── tests/                   # Pytest test cases
├── .env                     # Environment variables
├── Dockerfile
├── docker-compose.yml       
├── requirements.txt
├── .github/workflows/       # GitHub Actions
└── README.md
```

---

## ⚙️ Setup & Run

### 🔧 Prerequisites

- Python 3.10+
- Docker (for containerized setup)

### 🐍 Local Setup (Without Docker)

```bash
# 1. Clone the repo
git clone https://github.com/kar137/Resume-Analyzer-FastAPI.git
cd Resume-Analyzer-FastAPI

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example env

# 5. Run the app
uvicorn app.main:app --reload
```

### 🐳 Docker Setup

```bash
# Build and run using Docker Compose
docker-compose up --build
```

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📥 API Endpoints

| Method | Endpoint         | Description                  |
|--------|------------------|------------------------------|
| POST   | `/upload/`       | Upload a resume for analysis |
| GET    | `/result/{analysis_id}`   | Fetch analyzed data by ID    |

Open Swagger Docs at:  
**`http://localhost:8000/docs`**

---

## 🧪 FastAPI Concepts Used

✅ Dependency Injection  
✅ Background Tasks  
✅ Pydantic Settings & Models  
✅ Routers  
✅ Custom Exceptions  
✅ Middleware  
✅ Async DB Calls  
✅ Event Handlers (`startup`, `shutdown`)

---

## 📦 12-Factor Implementation Highlights

| Principle         | Implementation                                                  |
|------------------|------------------------------------------------------------------|
| Config           | `.env` + `pydantic.BaseSettings`                                 |
| Dependencies     | Defined in `requirements.txt`                                    |
| Backing services | Docker Compose                              |
| Dev/prod parity  | Docker enables consistent environments                           |
| Logs             | Configurable logging using Python `logging` module               |
| Admin processes  | CLI scripts or FastAPI endpoints (e.g., DB init, cache clear)    |

---

## 📸 Demo

https://youtu.be/GumG3kizIaI
---

## 👨‍💻 Author

**Karan Bista**  
[GitHub](https://github.com/kar137) • [LinkedIn](https://www.linkedin.com/in/karan-bista-6200242a1/)

---

## 📝 License
None
