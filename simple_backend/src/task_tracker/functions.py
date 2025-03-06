from fastapi import FastAPI
from pydantic import BaseModel
import json
from pathlib import Path


app = FastAPI()


# Код использующий оперативную память компьютера для хранения состояния

class Task(BaseModel):
    name_task: str
    status: str

data_base = {}
task_id = 1

@app.get('/tasks')
def get_tasks():
    return data_base

@app.post('/tasks', response_model=Task)
def create_task(task: Task):
    global task_id
    data_base.setdefault(
        task_id, {'name_task': task.name_task, 'status': task.status}
    )
    task_id += 1
    return task

@app.put('/tasks/{task_id}')
def update_task(task_id: int, new_info: Task):
    task = data_base.get(task_id)
    task['name_task'], task['status'] = new_info.name_task, new_info.status
    return task

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    data_base.pop(task_id)


# Код использующий json файл для хранения состояния

# task_id = 1


# data_file = Path('tasks.json')

# def write_data(data):
#     with open(data_file, 'w', encoding='utf-8') as file:
#         json.dump(data, file)

# def read_data():
#     with open(data_file, 'r', encoding='utf-8') as file:
#         try:
#             return json.load(file)
#         except json.JSONDecodeError:
#             return dict()

# @app.get('/tasks')
# def get_tasks():
#     return read_data()

# @app.post('/tasks', response_model=Task)
# def create_task(task: Task):
#     global task_id
#     tasks = read_data()
#     tasks.setdefault(task_id, task.dict())
#     write_data(tasks)
#     task_id += 1
#     return task

# @app.put('/tasks/{task_id}')
# def update_task(task_id: int, new_info: Task):
#     tasks = read_data()
#     tasks[str(task_id)] = {
#         "name_task": new_info.name_task, "status": new_info.status
#     }  
#     write_data(tasks)
#     return tasks[str(task_id)]

# @app.delete('/tasks/{task_id}')
# def delete_task(task_id: int):
#     tasks = read_data()
#     tasks.pop(str(task_id))
#     write_data(tasks)