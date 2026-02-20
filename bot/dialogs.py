from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime

from api_client import APIClient


# create or update task
class TaskFormSG(StatesGroup):
    ask_title = State()
    ask_description = State()
    ask_tags = State()
    ask_due_date = State()


async def save_title(
    message: Message,
    widget,
    manager: DialogManager,
):
    manager.dialog_data["title"] = message.text
    await manager.next()


async def save_description(message: Message, widget, manager: DialogManager):
    manager.dialog_data["description"] = message.text
    await manager.next()


async def save_tags(message: Message, widget, manager: DialogManager):
    tags = [tag.strip() for tag in message.text.lower().split(",") if tag.strip()]
    manager.dialog_data["tags"] = tags
    await manager.next()


async def save_due_date(message: Message, widget, manager: DialogManager):
    dt = datetime.strptime(message.text, "%d-%m-%Y")
    dt = dt.replace(hour=0, minute=0, second=0)
    iso_date = dt.isoformat()
    mode = manager.start_data.get("mode")

    user_id = message.from_user.id
    api = APIClient(user_id)

    try:
        if mode == "create":
            api.create_task(
                title=manager.dialog_data["title"],
                description=manager.dialog_data["description"],
                tags=manager.dialog_data["tags"],
                due_date=iso_date,
            )
            await message.answer("Задача создана ✅")

        elif mode == "edit":
            api.update_task(
                manager.dialog_data["task_id"],
                {
                    "title": manager.dialog_data["title"],
                    "description": manager.dialog_data.get("description", ""),
                    "due_date": manager.dialog_data["due_date"],
                },
            )
            await message.answer("Задача обновлена ✅")

    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

    await manager.done()


add_task_dialog = Dialog(
    Window(
        Const("Введите название задачи:"),
        MessageInput(save_title),
        state=TaskFormSG.ask_title,
    ),
    Window(
        Const("Введите описание задачи:"),
        MessageInput(save_description),
        state=TaskFormSG.ask_description,
    ),
    Window(
        Const("Введите тэг (через запятую):"),
        MessageInput(save_tags),
        state=TaskFormSG.ask_tags,
    ),
    Window(
        Const("Введите дату выполнениня в формате dd-mm-YYYY:"),
        MessageInput(save_due_date),
        state=TaskFormSG.ask_due_date,
    ),
)
