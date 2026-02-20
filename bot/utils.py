from datetime import datetime


async def format_tasks(tasks):
    text = ""

    for t in tasks:
        task_id = t.get("id", "")
        tags = ", ".join(t.get("tags", []))
        created_raw = t.get("created_at", "")
        due_raw = t.get("due_date", "")
        status = "✅" if t.get("completed", False) else "❌"
        description = t.get("description", "")

        try:
            created = (
                datetime.fromisoformat(created_raw).strftime("%d-%m-%Y")
                if created_raw
                else "не указано"
            )
        except ValueError:
            created = created_raw

        try:
            due_date = (
                datetime.fromisoformat(due_raw).strftime("%d-%m-%Y")
                if due_raw
                else "не указана"
            )
        except ValueError:
            due_date = due_raw

        text += (
            f"• {t['title']}\n"
            f"\tID: {task_id}\n"
            f"\tСоздано: {created}\n"
            f"\tДата исполнения: {due_date or 'не указана'}\n"
            f"\tТеги: {tags or 'нет'}\n"
            f"\tОписание: {description}\n"
            f"\tВыполнено: {status}\n\n"
        )

    return text
