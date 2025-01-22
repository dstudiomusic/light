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
