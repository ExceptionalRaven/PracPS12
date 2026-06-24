import requests
#Отправка данных
def send_json_to_server(data, url):
    try:
        #Добавлен таймаут в 10 секунд, чтобы уменьшить риск зависания
        response = requests.post(url, json=data, timeout=10)
        return response.status_code in [200, 201], response.text
    except Exception as e:
        return False, str(e)