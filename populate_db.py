import sqlite3

# Подключение к базе данных
conn = sqlite3.connect("knowledge_base.db")
cursor = conn.cursor()

# Данные для базы знаний
data = [
    ("Общие сведения", "Что такое Avolites Titan?", "Avolites Titan - это одна из ведущих операционных систем для управления светом."),
    ("Команды", "Как создать новую сцену в GrandMA?", "Используйте команду 'Store' и выберите нужный пресет."),
    ("Ошибки", "Почему HOG не подключается к DMX?", "Проверьте соединение и убедитесь, что выбран правильный DMX-канал.")
]

# Добавление данных в базу
cursor.executemany("INSERT INTO knowledge (category, question, answer) VALUES (?, ?, ?)", data)

conn.commit()
conn.close()

print("База данных успешно заполнена!")
