#Используем tkinter как UI
import tkinter as tk
from tkinter import ttk, messagebox
import json
import socket
# Подтягиваем два две других программы
import scanner
import sender

#Порт сервера на который приходят запросы
SERVER_URL = "http://127.0.0.1:5000/upload"

#Функция поиска приложений на ПК
def run_scan():
    status_label.config(text="Поиск...")
    root.update()

    data = scanner.get_installed_software()
    pc_name = socket.gethostname()
    final_data = {"pc_name": pc_name, "software": data}
    file_name = f"{pc_name}_software.json"

    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

    listbox.delete(0, tk.END)
    for item in data:
        listbox.insert(tk.END, f"{item['name']} ({item['version']})")
    status_label.config(text=f"Найдено: {len(data)}. Сохранено.")

# Отправляем найденные приложения и их версии
def run_send():
    pc_name = socket.gethostname()
    file_name = f"{pc_name}_software.json"
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
        status_label.config(text="Отправка...")
        success, response = sender.send_json_to_server(data, SERVER_URL)
        if success:
            messagebox.showinfo("Успех", "Данные отправлены!")
        else:
            messagebox.showerror("Ошибка", f"Не удалось: {response}")
    except FileNotFoundError:
        messagebox.showwarning("Ошибка", "Сначала соберите данные.")
    status_label.config(text="Готово")


root = tk.Tk()
root.title("Software Scanner")
root.geometry("400x450")
ttk.Button(root, text="1. Найти программы", command=run_scan).pack(fill=tk.X, pady=5)
ttk.Button(root, text="2. Отправить на сервер", command=run_send).pack(fill=tk.X, pady=5)
status_label = tk.Label(root, text="Ожидание...")
status_label.pack()
listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
root.mainloop()