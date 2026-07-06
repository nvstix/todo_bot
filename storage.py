"""Модуль для работы с хранением задач в JSON файле."""

import json
from typing import Dict, List, Any

FILE_NAME = "tasks.json"


def load_tasks() -> Dict[str, List[Dict[str, Any]]]:
    """Загружает задачи из JSON файла.

    Returns:
        Dict: Словарь, где ключ — ID пользователя, значение — список задач.
              Каждая задача: {"title": str, "done": bool}
    """
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_tasks(tasks: Dict[str, List[Dict[str, Any]]]) -> None:
    """Сохраняет задачи в JSON файл.

    Args:
        tasks: Словарь с задачами пользователей.
    """
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def get_user_tasks(tasks: Dict[str, List[Dict[str, Any]]], user_id: str) -> List[Dict[str, Any]]:
    """Возвращает список задач конкретного пользователя.

    Args:
        tasks: Словарь со всеми задачами.
        user_id: ID пользователя Telegram.

    Returns:
        List[Dict]: Список задач пользователя.
    """
    return tasks.get(user_id, [])


def save_user_tasks(
    tasks: Dict[str, List[Dict[str, Any]]],
    user_id: str,
    user_tasks: List[Dict[str, Any]]
) -> None:
    """Сохраняет задачи для конкретного пользователя.

    Args:
        tasks: Словарь со всеми задачами (будет изменён).
        user_id: ID пользователя Telegram.
        user_tasks: Новый список задач пользователя.
    """
    tasks[str(user_id)] = user_tasks
    save_tasks(tasks)