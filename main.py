import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Document
from pdf_processor import save_pdf_to_db  # Убедитесь, что у вас есть эта функция

API_TOKEN = "7888051694:AAGLYPL0UYtX_WrdrNcJ0vr5RNVbtdIrVx4"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание объектов бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()  # Диспетчер событий

# Обработчик команды /start
@dp.message(commands=["start"])
async def start_command(message: Message):
    await message.reply("Привет! Отправьте мне PDF-файл, чтобы я добавил его в базу данных.")

# Обработчик документов (PDF)
@dp.message(Document())
async def handle_document(message: types.Message):
    if message.document.mime_type == "application/pdf":
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_name = message.document.file_name

        # Скачивание файла
        await bot.download_file(file_info.file_path, file_name)

        # Сохранение в базу данных
        save_pdf_to_db(file_name)

        await message.reply(f"Файл {file_name} успешно загружен и добавлен в базу данных!")
    else:
        await message.reply("Пожалуйста, загрузите только PDF-файлы.")

# Запуск polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
