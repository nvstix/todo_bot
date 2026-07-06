"""Главный модуль для запуска Telegram бота."""

from telegram.ext import Application, CommandHandler
import handlers
import storage as st

TOKEN = "__"  # ⚠️ ВСТАВЬТЕ СВОЙ ТОКЕН ОТ BOTFATHER


def main() -> None:
    """Запускает бота."""
    # Загружаем задачи при старте (проверка, что файл существует)
    st.load_tasks()
    print("🤖 Бот запущен...")

    # Создаём приложение
    app = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("add", handlers.add_task))
    app.add_handler(CommandHandler("list", handlers.list_tasks))
    app.add_handler(CommandHandler("done", handlers.done_task))
    app.add_handler(CommandHandler("delete", handlers.delete_task))

    # Запускаем бота
    app.run_polling()


if __name__ == "__main__":
    main()
