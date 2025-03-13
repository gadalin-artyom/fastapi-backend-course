import json


class JsonStorage:
    def __init__(self, file_path):
        self.file_path = file_path
        self.task_id = 1

    def _get_next_id(self):
        tasks = self.read_data()
        current_id = map(int, tasks.keys())
        return max(current_id, default=0) + 1

    def _save_tasks(self, tasks):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(tasks, file)

    def write_data(self, data):
        tasks = self.read_data()
        tasks[str(self.task_id)] = data.dict()
        self._save_tasks(tasks)
        self.task_id = self._get_next_id()

    def read_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return dict()

    def delete_data(self, id):
        tasks = self.read_data()
        del tasks[str(id)]
        self._save_tasks(tasks)

    def update_data(self, task_id, new_data):
        tasks = self.read_data()
        tasks[str(task_id)] = new_data.dict()
        self._save_tasks(tasks)
