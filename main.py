from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Finish API", "done": False},
    {"id": 3, "title": "Read documentation", "done": True}
]

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
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get a single task by its ID."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.post("/tasks")
def create_task(payload: dict):
    """Create a new task."""
    title = payload.get("title", "").strip()
    
    if not title:
        return JSONResponse(status_code=400, content={"error": "Title is missing or empty"})
    
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    
    return JSONResponse(status_code=201, content=new_task)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: dict):
    """Update an existing task."""
    for task in tasks:
        if task["id"] == task_id:
            if "title" in payload:
                title = str(payload["title"]).strip()
                if not title:
                    return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
                task["title"] = title
            
            if "done" in payload:
                task["done"] = bool(payload["done"])
                
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task."""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            return Response(status_code=204)
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})