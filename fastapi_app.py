from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Повышенное №8 — Pydantic-схема входных данных."""

    title: str = Field(min_length=1, max_length=200)
    completed: bool = False


class Task(TaskCreate):
    """Pydantic-схема задачи с идентификатором."""

    id: int


app = FastAPI(
    title="Лабораторная работа №6",
    description="Вариант 8: параметры, REST API и Pydantic",
)

_tasks: list[Task] = [
    Task(id=1, title="Изучить FastAPI", completed=True),
    Task(id=2, title="Сделать лабораторную работу", completed=False),
]
_next_id = 3


@app.get("/hello")
def hello(name: str) -> dict[str, str]:
    """Среднее №8 — FastAPI принимает параметр и отвечает."""
    return {"message": f"Привет, {name}!"}


@app.get("/tasks", response_model=list[Task])
def get_tasks() -> list[Task]:
    """Среднее №10 — получить список задач."""
    return _tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate) -> Task:
    """Среднее №10 + повышенное №8 — создание задачи через Pydantic."""
    global _next_id

    new_task = Task(id=_next_id, **task.model_dump())
    _tasks.append(new_task)
    _next_id += 1
    return new_task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    for task in _tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskCreate) -> Task:
    for index, task in enumerate(_tasks):
        if task.id == task_id:
            updated = Task(id=task_id, **data.model_dump())
            _tasks[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict[str, str]:
    for index, task in enumerate(_tasks):
        if task.id == task_id:
            del _tasks[index]
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")
