from flask import Flask, request, jsonify
import sqlite3
import json
import os
import sys

app = Flask(__name__)

# Универсальное определение пути к БД
def get_db_path():
    # Если запущено как .exe (через PyInstaller), берем папку с .exe
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        # Если запущено как .py, берем папку со скриптом
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'software_data.db')

DB_NAME = get_db_path()

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
    data = request.json
    pc_name = data.get('pc_name')
    software_list = json.dumps(data.get('software'))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Явно указываем поля для вставки
    cursor.execute("INSERT INTO inventory (pc_name, software_data) VALUES (?, ?)",
                   (pc_name, software_list))
    conn.commit()
    conn.close()

    return jsonify({"message": "Данные успешно сохранены!"}), 201


if __name__ == '__main__':
    init_db()
    app.run(port=5000)