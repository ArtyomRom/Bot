import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config_data import Config, load_config_data
from handlers import user_handlers, other_hendlers
from keyboards.main_menu import set_main_menu
from environs import Env
# Инициализируем логгер
logger = logging.getLogger(__name__)

# Функция конфигурации и запуска бота
async def main():
    # Конфигурация логирования
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Конфигурация бота
    config = load_config_data()

    # Инициализируем бот и диспетчер

    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML)
              )
    dp = Dispatcher()

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # # Регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_hendlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())

