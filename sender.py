import requests # Библиотека, чтобы указать серверу, что передаем json
import json

def send_json_to_server(data, url):
    try:
        # Используем метод post
        response = requests.post(url, json=data) # передаем данные, чтобы перевести их в json
        return response.status_code == 200 or response.status_code == 201, response.text # выводим 200 или 201 если запрос прошел успешно
    except Exception as e:
        return False, str(e) # False если нет

# Программа которая использовалась при debug'ге
# import requests
# import json
#
#
# def send_json_to_server(data, url):
#     try:
#         print(f"DEBUG: Пытаюсь отправить данные на {url}")  # Видно в консоли
#         # Добавляем таймаут, чтобы не ждать вечно
#         response = requests.post(url, json=data, timeout=10)
#
#         print(f"DEBUG: Код ответа сервера: {response.status_code}")
#         print(f"DEBUG: Ответ сервера: {response.text}")
#
#         return response.status_code in [200, 201], response.text
#     except Exception as e:
#         print(f"DEBUG: Ошибка в sender: {e}")
#         return False, str(e)