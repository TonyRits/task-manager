# 📝 Task Manager App

A full-stack Task Manager web application built with FastAPI backend and HTML/CSS/JS frontend.

## 🚀 Live Demo

- **Backend API**: https://task-manager-s8qq.onrender.com
- **API Docs**: https://task-manager-s8qq.onrender.com/docs

---

## 🧱 Tech Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI, SQLAlchemy, SQLite |
| Auth | JWT, bcrypt |
| Frontend | HTML, CSS, JavaScript |
| Testing | pytest |
| Deployment | Render |

---

## 📂 Project Structure

task-manager/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── utils.py
│   │   └── routers/
│   │       ├── auth.py
│   │       └── tasks.py
│   ├── tests/
│   │   └── test_tasks.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
└── frontend/
├── index.html
├── style.css
└── app.js

---

## ⚙️ Environment Variables

Create a `.env` file inside `backend/` folder:
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///./tasks.db

See `.env.example` for reference.

---

## 🛠️ How to Run Locally

### Backend

```bash
# 1. Go to backend folder
cd task-manager/backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
python -m uvicorn app.main:app --reload
```

- API runs at: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

### Frontend

Open `frontend/index.html` directly in your browser.

---

## 📌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register new user |
| POST | `/login` | Login and get JWT token |

### Tasks (🔒 Auth Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Create a task |
| GET | `/tasks/` | Get all tasks |
| GET | `/tasks/{id}` | Get specific task |
| PUT | `/tasks/{id}` | Update or complete task |
| DELETE | `/tasks/{id}` | Delete task |

### Query Parameters
GET /tasks/?completed=true    → completed tasks
GET /tasks/?completed=false   → pending tasks
GET /tasks/?page=1&limit=10   → pagination

---

## 🧪 Running Tests

```bash
cd task-manager/backend
python -m pytest tests/ -v
```

---

## 🐳 Docker

```bash
cd task-manager/backend
docker build -t task-manager .
docker run -p 8000:8000 task-manager
```

---

## 🚫 Important Notes

- Never commit `.env` file
- Use `.env.example` as reference
- All task routes are JWT protected
- Users can only access their own tasks