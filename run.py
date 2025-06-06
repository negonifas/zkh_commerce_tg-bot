import sys
import os
import asyncio
from dotenv import load_dotenv  # Для использования os.getenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger  # Импортируем Loguru

from app.handlers import user_reg, violation
from app.pagination import go_paginator

# Настройка Loguru
# Вывод логов в консоль с цветами и форматированием
logger.remove()  # Удаляем стандартный вывод Loguru, чтобы переопределить его
logger.add(
    sys.stdout,  # Консольный вывод
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    # level="INFO",  # Минимальный уровень логов
    level="DEBUG",  # Минимальный уровень логов
    colorize=True,  # Включение цветов
)

# Логирование в файл с ротацией
logger.add(
    "./bot_logs/app.log",  # Относительный путь # Имя файла
    rotation="10 MB",  # Ротация при достижении 10 MB
    compression="zip",  # Сжатие старых логов
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",  # Минимальный уровень логов для файла
    colorize=True,
)

# Основная функция запуска бота
async def main() -> None:
    load_dotenv()
    bot = Bot(
        token=os.getenv('TOKEN'),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    dp = Dispatcher(storage=MemoryStorage())

    # Роутеры для обработки команд
    dp.include_routers(
        user_reg.router,
        violation.router,
        go_paginator.router,
    )
    logger.info("Бот начал работу")  # Сообщение при старте бота
    # await dp.start_polling(bot)  # Запускаем бота
    # await dp.start_polling(bot, skip_updates=True)  # Запускаем бота с пропуском обновлений, решаем локально
    await dp.start_polling(bot, drop_pending_updates=True)  # Запускаем бота с пропуском обновлений, решает на сервере


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Выход из приложения")  # Используем Loguru для вывода сообщений
