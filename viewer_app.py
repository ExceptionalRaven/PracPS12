import tkinter as tk
from tkinter import ttk
import sqlite3
import json
import os

# Путь к БД
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'software_data.db')

# Debug на случай если файл БД не найден
if not os.path.exists(db_path):
    print(f"ОШИБКА: Файл БД не найден по пути: {db_path}")
else:
    print(f"Файл БД найден: {db_path}")

def show_details(event):
    # Открывает окно с подробным списком ПО для выбранного ПК
    selected_item = tree.selection()
    if not selected_item:
        return

    item_data = tree.item(selected_item)
    record_id = item_data['values'][0]

    # Создаем новое окно
    detail_window = tk.Toplevel(root)
    detail_window.title(f"Детали записи ID: {record_id}")
    detail_window.geometry("400x500")

    # Список ПО
    tree_detail = ttk.Treeview(detail_window, columns=("name", "ver"), show="headings")
    tree_detail.heading("name", text="Название")
    tree_detail.heading("ver", text="Версия")
    tree_detail.column("name", width=250)
    tree_detail.column("ver", width=100)
    tree_detail.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Загрузка данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT software_data FROM inventory WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        software_list = json.loads(row[0])
        for app in software_list:
            tree_detail.insert("", "end", values=(app['name'], app['version']))


def load_data():
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Можно будет здесь добавить try/except в будущем, но сейчас он убран для дебага
    cursor.execute("SELECT id, pc_name, software_data, timestamp FROM inventory ORDER BY id DESC")
    rows = cursor.fetchall()

    print(f"Найдено записей в БД: {len(rows)}")  # Debug

    for row in rows:
        software_list = json.loads(row[2])
        tree.insert("", "end", values=(row[0], row[1], len(software_list), row[3]))
    conn.close()

# Интерфейс
root = tk.Tk()
root.title("Просмотр базы данных ПО")
root.geometry("600x400")

columns = ("id", "pc", "count", "date")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("id", text="ID")
tree.heading("pc", text="Имя ПК")
tree.heading("count", text="Кол-во ПО")
tree.heading("date", text="Дата/Время")
tree.column("id", width=50)
tree.column("count", width=80)
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Привязываем двойной клик к функции просмотра деталей
tree.bind("<Double-1>", show_details)

ttk.Button(root, text="Обновить список", command=load_data).pack(pady=5)

load_data()
root.mainloop()