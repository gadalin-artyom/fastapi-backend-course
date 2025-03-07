import json
from pathlib import Path


class JsonStorage:
    def __init__(self):
        self.file_path = Path('tasks.json')
        self.task_id = 1

    def _get_next_id(self):
        tasks = self.read_data()
        current_id = map(int, tasks.keys())
        return max(current_id, default=0) + 1

    def write_data(self, data):
        tasks = self.read_data()
        tasks[str(self.task_id)] = data.dict()
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(tasks, file)
        self.task_id = self._get_next_id()

    def read_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return dict()

    def delete_data(self, id):
        tasks = self.read_data()
        del tasks[str(id)]
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(tasks, file)

    def update_data(self, task_id, new_data):
        tasks = self.read_data()
        tasks[str(task_id)] = new_data.dict()
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(tasks, file)
