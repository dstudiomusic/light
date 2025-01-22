def search_pdf_content(query):
    """Ищет совпадения в загруженных PDF-файлах."""
    conn = sqlite3.connect("knowledge_base.db")
    cursor = conn.cursor()

    cursor.execute("SELECT filename, content FROM pdf_files WHERE content LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()

    conn.close()

    if results:
        response = "Вот что я нашел:\n\n"
        for result in results[:3]:  # Ограничение на 3 результата
            response += f"📄 В файле {result[0]} найдено:\n{result[1][:500]}...\n\n"
        return response
    else:
        return "Извините, в загруженных PDF я не нашел информацию по вашему запросу."
import sqlite3

def search_answer(question):
    """Ищет ответ на вопрос в таблице knowledge."""
    conn = sqlite3.connect("knowledge_base.db")  # Подключение к базе данных
    cursor = conn.cursor()  # Создание курсора

    # Выполнение SQL-запроса
    cursor.execute("SELECT answer FROM knowledge WHERE question LIKE ?", ('%' + question + '%',))
    result = cursor.fetchone()  # Получение результата

    conn.close()  # Закрытие соединения

    # Возврат результата или сообщение об отсутствии ответа
    return result[0] if result else "Извините, я не нашел ответа на этот вопрос."

def create_pdf_table():
    """Создаёт таблицу для хранения PDF-файлов."""
    conn = sqlite3.connect("knowledge_base.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pdf_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()

# Вызовите функцию, если таблица ещё не была создана
create_pdf_table()

