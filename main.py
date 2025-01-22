import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from pdf_processor import save_pdf_to_db

API_TOKEN = "ВАШ_ТОКЕН"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Загрузите PDF-файл, чтобы я обработал его и добавил в базу данных.")

@dp.message(content_types=["document"])
async def handle_document(message: types.Message):
    """Обработка загруженных PDF-файлов."""
    if message.document.mime_type == "application/pdf":
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_name = message.document.file_name

        # Скачивание файла
        await bot.download_file(file_info.file_path, file_name)

        # Сохранение в базу данных
        save_pdf_to_db(file_name)

        await message.reply(f"Файл {file_name} успешно загружен и проанализирован!")
    else:
        await message.reply("Пожалуйста, загрузите только PDF-файлы.")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

@dp.message_handler()
async def handle_message(message: types.Message):
    query = message.text

    # Сначала ищем в базе знаний
    response = search_answer(query)

    # Если не найдено, ищем в PDF
    if response == "Извините, я не нашел ответа на этот вопрос.":
        response = search_pdf_content(query)

    await message.reply(response)
