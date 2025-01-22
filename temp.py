import sqlite3

# Подключение к базе данных (файл создается автоматически)
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS test_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

# Вставка данных
cursor.execute("INSERT INTO test_table (name) VALUES ('Test User')")
conn.commit()

# Вывод данных
cursor.execute("SELECT * FROM test_table")
print(cursor.fetchall())

conn.close()
