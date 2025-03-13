import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from cloudflare import CloudflareAI
from jsonbin import JsonBinStorage

load_dotenv()

app = FastAPI()

API_KEY = os.getenv('API_KEY')
BIN_ID = os.getenv('BIN_ID')

# TaskTracker через ООП


class Task(BaseModel):
    name_task: str
    status: str


class TaskTracker:
    def __init__(self, storage, ai):
        self.storage = storage
        self.ai = ai

    def get_tasks(self):
        return self.storage.read_data()

    def create_task(self, task: Task):
        ai_solution = self.ai.get_solution(task.name_task)
        task_with_solution = Task(
            name_task=f'{task.name_task}\n\n Решение:\n{ai_solution}',
            status=task.status,
        )
        self.storage.write_data(task_with_solution)

    def delete_task(self, task_id):
        self.storage.delete_data(task_id)

    def change_task(self, task_id, new_info):
        self.storage.update_data(task_id, new_info)


# json_storage = JsonStorage(Path('tasks.json'))
# tracker = TaskTracker(json_storage)


# jsonbin_storage= JsonBinStorage(API_KEY, BIN_ID)
# tracker = TaskTracker(jsonbin_storage)


account_id_CF = os.getenv('ACCOUNT_ID_CLOUDFLARE')
api_token_CF = os.getenv('API_TOKEN_CLOUDFLARE')
model_CF = '@cf/meta/llama-3.1-8b-instruct'
cloudflare = CloudflareAI(account_id_CF, api_token_CF, model_CF)

jsonbin_storage = JsonBinStorage(API_KEY, BIN_ID)
tracker = TaskTracker(jsonbin_storage, cloudflare)


@app.get('/tasks')
def get_tasks():
    return tracker.get_tasks()


@app.post('/tasks', response_model=Task)
def create_task(task: Task):
    tracker.create_task(task)
    return task


@app.put('/tasks/{task_id}')
def update_task(task_id: int, new_info: Task):
    tracker.change_task(task_id, new_info)
    return new_info


@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    tracker.delete_task(task_id)
    return {'status': 'Задача удалена'}
