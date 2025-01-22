import fitz  # PyMuPDF
import sqlite3
import os

def extract_text_from_pdf(pdf_path):
    """Извлекает текст из PDF-файла."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()

def save_pdf_to_db(pdf_path):
    """Сохраняет текст из PDF в базу данных."""
    filename = os.path.basename(pdf_path)
    content = extract_text_from_pdf(pdf_path)

    conn = sqlite3.connect("knowledge_base.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pdf_files (filename, content) VALUES (?, ?)", (filename, content))
    conn.commit()
    conn.close()

    print(f"Файл {filename} успешно загружен в базу данных!")

# Пример использования
pdf_path = "example.pdf"  # Укажите путь к вашему PDF-файлу
save_pdf_to_db(pdf_path)
