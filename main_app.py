import tkinter as tk # Здесь используем tkinter как UI
from tkinter import ttk, messagebox
import json # Подтягиваем две другие часто программы
import scanner
import sender
import socket #Подключаем socket, чтобы правильно определять какой сокет надо использовать

SERVER_URL = "https://webhook.site/12733338-6dc8-4665-85dd-287af93260ed"  # Ссылка на мой webhook, куда приходят запросы


def run_scan(): # проходим по программам и добавляем их в список
    status_label.config(text="Поиск...") #В окне программы пишем что идет поиск
    root.update()

    # Получаем список программ
    data = scanner.get_installed_software()
    pc_name = socket.gethostname()

    # Создаем структуру для JSON
    final_data = {
        "pc_name": pc_name,
        "software": data
    }

    # Имя файла
    file_name = f"{pc_name}_software.json"

    # Сохраняем в файл
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        #Ставим ensure_ascii=False, чтобы программа нормально воспринимала кириллицу

    listbox.delete(0, tk.END)  # Очищаем старые данные
    for item in data:  # Проходимся по списку data
        listbox.insert(tk.END, f"{item['name']} (версия: {item['version']})")

    status_label.config(text=f"Найдено: {len(data)}. Сохранено как {file_name}")
def run_send():
    pc_name = socket.gethostname()
    file_name = f"{pc_name}_software.json"

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)

        status_label.config(text="Отправка...")
        success, response = sender.send_json_to_server(data, SERVER_URL)

        if success:
            messagebox.showinfo("Успех", "Данные отправлены на сервер!")
        else:
            messagebox.showerror("Ошибка", f"Не удалось отправить: {response}")
    except FileNotFoundError:
        messagebox.showwarning("Ошибка", f"Файл {file_name} не найден! Сначала соберите данные.")

    status_label.config(text="Готово")


# UI
root = tk.Tk()
root.title("Software Manager")
root.geometry("400x450")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Button(frame, text="1. Найти программы", command=run_scan).pack(fill=tk.X, pady=5)
ttk.Button(frame, text="2. Отправить на сервер", command=run_send).pack(fill=tk.X, pady=5)

status_label = tk.Label(root, text="Ожидание...")
status_label.pack()

listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()