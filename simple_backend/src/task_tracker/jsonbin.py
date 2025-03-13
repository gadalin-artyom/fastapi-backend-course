import requests
from pydantic import BaseModel


class JsonBinStorage:
    def __init__(self, api_key: str, bin_id: str):
        self.api_key = api_key
        self.bin_id = bin_id
        self.url = f'https://api.jsonbin.io/v3/b/{self.bin_id}'
        self.headers = {
            'X-Master-Key': self.api_key,
            'Content-Type': 'application/json',
        }
        self.task_id = self._get_next_id()

    def _get_next_id(self):
        tasks = self.read_data()
        current_id = map(int, tasks.keys())
        return max(current_id, default=0) + 1

    def _save_data(self, tasks):
        response = requests.put(self.url, headers=self.headers, json=tasks)
        response.raise_for_status()

    def read_data(self):
        response = requests.get(self.url, headers=self.headers)
        data = response.json().get('record', {})
        return data if isinstance(data, dict) else {}

    def write_data(self, data: BaseModel):
        tasks = self.read_data()
        tasks[str(self.task_id)] = data.dict()
        self._save_data(tasks)
        self.task_id = self._get_next_id()

    def delete_data(self, id):
        tasks = self.read_data()
        del tasks[str(id)]
        self._save_data(tasks)

    def update_data(self, task_id, new_data: BaseModel):
        tasks = self.read_data()
        tasks[str(task_id)] = new_data.dict()
        self._save_data(tasks)
