# Task API

A simple CRUD API for managing tasks built with FastAPI.

## How to Run

1. Install dependencies (FastAPI and Uvicorn):
   ```bash
   pip install fastapi uvicorn
   ```
2. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

---

## Endpoints

| Method | Path | Description |
| :--- | :--- | :--- |
| **GET** | `/` | Get API details |
| **GET** | `/health` | Check if server is running |
| **GET** | `/tasks` | List all tasks |
| **GET** | `/tasks/{task_id}` | Get a single task by its ID |
| **POST** | `/tasks` | Create a new task |
| **PUT** | `/tasks/{task_id}` | Update an existing task |
| **DELETE** | `/tasks/{task_id}` | Delete a task |

---

## Example Usage

### Get a single task

**Command (Bash/zsh):**
```bash
curl -i http://localhost:8000/tasks/1
```

**Command (PowerShell):**
```powershell
Invoke-RestMethod -Uri http://localhost:8000/tasks/1
```

**Response:**
```http
HTTP/1.1 200 OK
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
```

### Create a task

**Command (Bash/zsh):**
```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Clean room"}'
```

**Command (PowerShell):**
```powershell
Invoke-RestMethod -Uri http://localhost:8000/tasks -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"title":"Clean room"}'
```