from flask import Flask, request, jsonify
import sqlite3
import json

# Создаем файл бд
app = Flask(__name__)
DB_NAME = "software_data.db"


# Инициализация базы данных
def init_db():
    # Подключаемся к файлу БД
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    #В БД создаем таблицу inventory с колонками
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS inventory
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       pc_name
                       TEXT,
                       software_data
                       TEXT,
                       timestamp
                       DATETIME
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   ''')
    conn.commit()
    conn.close()

#Блок приема данных
#Ждем данные от метода POST
@app.route('/upload', methods=['POST'])
def upload_data():
    #Извлекаем данные и групперуем их
    data = request.json
    pc_name = data.get('pc_name')
    software_list = json.dumps(data.get('software'))  # Сохраняем список как JSON-строку

    #Подключаемся к БД и сохраняем данные
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (pc_name, software_data) VALUES (?, ?)", (pc_name, software_list))
    conn.commit()
    conn.close()

    return jsonify({"message": "Данные успешно сохранены!"}), 201


if __name__ == '__main__':
    init_db()
    app.run(port=5000)