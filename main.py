from starlette import concurrency
import sqlite3
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

DB_NAME = "tasks.db"


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM tasks")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Buy groceries", 0),
                ("Clean room", 0),
                ("Learn SQLite", 0),
            ],
    )
    conn.commit()
    conn.close()


init_db()

app = FastAPI()


@app.get("/")
def read_root():
    """Get API details."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health_check():
    """Check if server is running."""
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    """List all tasks."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": row["id"], "title": row["title"], "done": bool(row["done"])}
        for row in rows
    ]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get a single task by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return JSONResponse(
            status_code=404, content={"error": f"Task {task_id} not found"}
        )

    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


@app.post("/tasks")
def create_task(payload: dict):
    """Create a new task."""
    title = payload.get("title", "").strip()
    if not title:
        return JSONResponse(
            status_code=400, content={"error": "Title is missing or empty"}
        )

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, 0)", (title,))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    new_task = {"id": new_id, "title": title, "done": False}
    return JSONResponse(status_code=201, content=new_task)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: dict):
    """Update an existing task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return JSONResponse(
            status_code=404, content={"error": f"Task {task_id} not found"}
        )

    title = row["title"]
    done = bool(row["done"])

    if "title" in payload:
        new_title = str(payload["title"]).strip()
        if not new_title:
            conn.close()
            return JSONResponse(
                status_code=400, content={"error": "Title cannot be empty"}
            )
        title = new_title

    if "done" in payload:
        done = bool(payload["done"])

    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (title, int(done), task_id),
    )
    conn.commit()
    conn.close()

    return {"id": task_id, "title": title, "done": done}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return JSONResponse(
            status_code=404, content={"error": f"Task {task_id} not found"}
        )

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return Response(status_code=204)