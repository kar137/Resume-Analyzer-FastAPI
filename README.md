# Resume Analyzer API (FastAPI)

A microservice built with **FastAPI** that analyzes resumes (PDF/DOCX), extracts skills, and provides career insights using NLP techniques. This project demonstrates modern backend practices and applies the **12-Factor App** principles.

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

## 🏗️ Tech Stack

- **Python** + **FastAPI**
- **Pydantic** for config & data validation
- **SQLAlchemy** (async DB)
- **Docker**, **GitHub Actions**, **pytest**, **pre-commit**

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
├── pre-commit-config.yaml
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


---

## 👨‍💻 Author

**Karan Bista**  
[GitHub](https://github.com/kar137) • [LinkedIn](https://www.linkedin.com/in/karan-bista-6200242a1/)

---

## 📝 License
None
