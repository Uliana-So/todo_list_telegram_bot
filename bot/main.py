import logging
import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram_dialog import setup_dialogs, DialogManager, StartMode
from dotenv import load_dotenv

from api_client import APIClient
from dialogs import add_task_dialog, TaskFormSG
from utils import format_tasks

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(add_task_dialog)

USER_TASKS = {}


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я ToDo Bot.\n"
        "Команды:\n"
        "/tasks - показать задачи\n"
        "/add - добавить задачу\n"
        "/edit - изменить задачу\n"
        "/delete - удалить задачу"
    )


@dp.message(Command("tasks"))
async def cmd_tasks(message: Message):
    user_id = message.from_user.id
    api = APIClient(user_id)
    tasks = api.get_tasks()

    if not tasks:
        await message.answer("У тебя пока нет задач.")
        return

    USER_TASKS[user_id] = tasks

    all_tags = set()
    for t in tasks:
        for tag in t.get("tags", []):
            all_tags.add(tag.lower())

    buttons = [
        InlineKeyboardButton(text=tag, callback_data=f"filter_{tag}")
        for tag in sorted(all_tags)
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[buttons[i : i + 3] for i in range(0, len(buttons), 3)]
    )

    text = await format_tasks(tasks)
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query(F.data.startswith("filter_"))
async def filter_by_tag_callback(query: CallbackQuery, dialog_manager: DialogManager):
    _, tag = query.data.split("_")
    user_id = query.from_user.id

    tasks = USER_TASKS.get(user_id, [])
    filtered_tasks = [
        t for t in tasks if tag in [tg.lower() for tg in t.get("tags", [])]
    ]

    if not filtered_tasks:
        await query.message.edit_text(f"Задач с тегом '{tag}' нет.", reply_markup=None)
        await query.answer()
        return

    text = await format_tasks(filtered_tasks)
    await query.message.edit_text(text, reply_markup=None)
    await query.answer()


@dp.message(Command("add"))
async def cmd_add(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        TaskFormSG.ask_title,
        mode=StartMode.RESET_STACK,
        data={"mode": "create"},
    )


@dp.message(Command("edit"))
async def cmd_edit(message: Message, dialog_manager: DialogManager):
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Укажи ID задачи: /edit ID")
        return

    task_id = parts[1]

    await dialog_manager.start(
        TaskFormSG.ask_title,
        data={
            "mode": "edit",
            "task_id": task_id,
        },
    )


@dp.message(Command("delete"))
async def cmd_delete(message: Message):
    parts = message.text.split()

    if len(parts) != 2:
        await message.answer("Укажи ID задачи: /delete ID")
        return

    task_id = parts[1]

    api = APIClient(message.from_user.id)

    try:
        api.delete_task(task_id)
        await message.answer("Задача удалена ✅")

    except Exception as e:
        await message.answer(f"Ошибка удаления: {e}")


if __name__ == "__main__":
    setup_dialogs(dp)
    asyncio.run(dp.start_polling(bot))
