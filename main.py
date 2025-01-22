import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from database import search_answer, search_pdf_content  # Подключаем новые функции

# Вставьте ваш токен
API_TOKEN = "7888051694:AAGLYPL0UYtX_WrdrNcJ0vr5RNVbtdIrVx4"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот-ассистент для художников по свету. Вы можете задать мне вопрос или загрузить PDF-файл.")

@dp.message_handler(content_types=["document"])
async def handle_document(message: types.Message):
    """Обрабатывает загруженные PDF-файлы."""
    if message.document.mime_type == "application/pdf":
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        file_name = message.document.file_name

        # Скачивание файла
        await bot.download_file(file_path, file_name)

        # Загрузка в базу данных
        save_pdf_to_db(file_name)

        await message.reply(f"Файл {file_name} загружен и проанализирован!")
    else:
        await message.reply("Я принимаю только PDF-файлы.")

@dp.message_handler()
async def handle_question(message: types.Message):
    """Обрабатывает текстовые запросы, включая поиск по PDF."""
    text_query = message.text

    # Сначала ищем в базе знаний
    response = search_answer(text_query)
    
    # Если ничего не найдено, ищем в PDF
    if response == "Извините, я не нашел ответа на этот вопрос.":
        response = search_pdf_content(text_query)

    await message.reply(response)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
