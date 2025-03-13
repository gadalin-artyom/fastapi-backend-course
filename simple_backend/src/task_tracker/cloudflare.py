
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL_CLOUDFLARE = 'https://api.cloudflare.com/client/v4/accounts/'


class CloudflareAI:
    def __init__(self, account_id, api_token, model):
        self.account_id = account_id
        self.api_token = api_token
        self.model = model
        self.url = (
            BASE_URL_CLOUDFLARE + f'{self.account_id}/ai/run/' + self.model
        )
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
        }

    def get_solution(self, task_text: str) -> str:
        payload = {
            'model': self.model,
            'messages': [
                {'role': 'system', 'content': 'Мой ассистент'},
                {
                    'role': 'user',
                    'content': f'Расскажи как решить задачу: {task_text}',
                },
            ],
        }

        response = requests.post(self.url, headers=self.headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            return result['result']['response']
        else:
            return f'Ошибка запроса: {response.text}'
