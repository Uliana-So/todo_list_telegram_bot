import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("BACKEND_API_URL")


class APIClient:
    def __init__(self, telegram_id: int):
        self.client = httpx.Client(
            base_url=API_URL,
            headers={"X-Telegram-ID": str(telegram_id)},
            timeout=10,
        )

    def get_tasks(self, tag=None):
        response = self.client.get("tasks/")
        response.raise_for_status()
        tasks = response.json()

        if tag:
            tasks = [
                t for t in tasks if tag in [tg.lower() for tg in t.get("tags", [])]
            ]
        return tasks

    def create_task(self, title, description="", tags=None, due_date=""):
        payload = {
            "title": title,
            "description": description,
            "tags": tags or [],
            "due_date": due_date,
        }
        response = self.client.post("tasks/", json=payload)
        response.raise_for_status()
        return response.json()

    def update_task(self, task_id, payload):
        response = self.client.patch(f"tasks/{task_id}/", json=payload)
        response.raise_for_status()
        return response.json()

    def delete_task(self, task_id):
        response = self.client.delete(f"tasks/{task_id}/")
        response.raise_for_status()
