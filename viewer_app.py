#Надо будет сделать интерфейс для просмотра данных с бд, но у меня не получилось
import sqlite3
import json


def view_data():
    conn = sqlite3.connect('software_data.db')
    cursor = conn.cursor()

    # Получаем все данные
    cursor.execute("SELECT id, pc_name, software_data FROM inventory")
    rows = cursor.fetchall()

    for row in rows:
        print(f"--- ID: {row[0]} | ПК: {row[1]} ---")
        software = json.loads(row[2])  # Превращаем JSON-строку обратно в список
        for item in software:
            print(f"  {item['name']} ({item['version']})")
        print("\n")

    conn.close()


if __name__ == "__main__":
    view_data()
# import tkinter as tk
# from tkinter import ttk
# import sqlite3
# import json
# import os
#
# # Получаем путь к папке, где лежит сам скрипт viewer_app.py
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, 'software_data.db')
#
# def load_data():
#     # Очищаем таблицу перед загрузкой
#     for item in tree.get_children():
#         tree.delete(item)
#
#     try:
#         conn = sqlite3.connect(db_path)
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, pc_name, software_data, timestamp FROM inventory ORDER BY id DESC")
#         rows = cursor.fetchall()
#
#         for row in rows:
#             # Превращаем JSON-строку в список для отображения количества программ
#             software_list = json.loads(row[2])
#             tree.insert("", "end", values=(row[0], row[1], len(software_list), row[3]))
#         conn.close()
#     except sqlite3.OperationalError:
#         print("База данных не найдена. Сначала соберите и отправьте данные.")
#
#
# # Настройка главного окна
# root = tk.Tk()
# root.title("Просмотр базы данных ПО")
# root.geometry("600x400")
#
# # Создаем таблицу
# columns = ("id", "pc", "count", "date")
# tree = ttk.Treeview(root, columns=columns, show="headings")
#
# tree.heading("id", text="ID")
# tree.heading("pc", text="Имя ПК")
# tree.heading("count", text="Кол-во ПО")
# tree.heading("date", text="Дата/Время")
#
# tree.column("id", width=50)
# tree.column("count", width=80)
# tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
#
# # Кнопка обновления
# btn_refresh = ttk.Button(root, text="Обновить список", command=load_data)
# btn_refresh.pack(pady=5)
#
# load_data()  # Загрузка при старте
# root.mainloop()