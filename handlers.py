"""Модуль с обработчиками команд Telegram бота."""

from telegram import Update
from telegram.ext import ContextTypes
import storage as st


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start.

    Отправляет пользователю приветствие и список доступных команд.

    Args:
        update: Объект с данными о сообщении от Telegram.
        context: Контекст команды.
    """
    await update.message.reply_text(
        "👋 Привет! Я бот для списка дел.\n\n"
        "📌 Команды:\n"
        "/add задача — добавить задачу\n"
        "/list — показать список\n"
        "/done номер — отметить выполненной\n"
        "/delete номер — удалить задачу"
    )


async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /add.

    Добавляет новую задачу в список пользователя.

    Args:
        update: Объект с данными о сообщении от Telegram.
        context: Контекст команды, содержит текст задачи.
    """
    user_id = str(update.effective_user.id)
    task_text = " ".join(context.args)

    if not task_text:
        await update.message.reply_text("❌ Пример: /add Купить хлеб")
        return

    tasks = st.load_tasks()
    user_tasks = st.get_user_tasks(tasks, user_id)
    user_tasks.append({"title": task_text, "done": False})
    st.save_user_tasks(tasks, user_id, user_tasks)

    await update.message.reply_text(f"✅ Добавлено: {task_text}")


async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /list.

    Показывает все задачи пользователя с нумерацией и статусом выполнения.

    Args:
        update: Объект с данными о сообщении от Telegram.
        context: Контекст команды.
    """
    user_id = str(update.effective_user.id)
    tasks = st.load_tasks()
    user_tasks = st.get_user_tasks(tasks, user_id)

    if not user_tasks:
        await update.message.reply_text("📭 Список дел пуст")
        return

    message = "📋 Ваш список дел:\n\n"
    for i, task in enumerate(user_tasks, 1):
        status = "✅" if task["done"] else "❌"
        message += f"{i}. {status} {task['title']}\n"

    await update.message.reply_text(message)


async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /done.

    Отмечает задачу по номеру как выполненную.

    Args:
        update: Объект с данными о сообщении от Telegram.
        context: Контекст команды, содержит номер задачи.
    """
    user_id = str(update.effective_user.id)

    try:
        task_num = int(context.args[0]) - 1
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Пример: /done 1")
        return

    tasks = st.load_tasks()
    user_tasks = st.get_user_tasks(tasks, user_id)

    if 0 <= task_num < len(user_tasks):
        user_tasks[task_num]["done"] = True
        st.save_user_tasks(tasks, user_id, user_tasks)
        await update.message.reply_text("✅ Задача отмечена выполненной!")
    else:
        await update.message.reply_text("❌ Неверный номер задачи")


async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /delete.

    Удаляет задачу по номеру из списка пользователя.

    Args:
        update: Объект с данными о сообщении от Telegram.
        context: Контекст команды, содержит номер задачи.
    """
    user_id = str(update.effective_user.id)

    try:
        task_num = int(context.args[0]) - 1
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Пример: /delete 1")
        return

    tasks = st.load_tasks()
    user_tasks = st.get_user_tasks(tasks, user_id)

    if 0 <= task_num < len(user_tasks):
        deleted = user_tasks.pop(task_num)
        st.save_user_tasks(tasks, user_id, user_tasks)
        await update.message.reply_text(f"🗑 Удалено: {deleted['title']}")
    else:
        await update.message.reply_text("❌ Неверный номер задачи")