Для разработчиков:
SoftwareScanner — Программа для сбора списка установленного ПО
Возможности
- Автоматическое сканирование установленного ПО
- Поддержка Windows и Linux
- Простой графический интерфейс
- Сохранение результатов в JSON файл
- Отправка данных на сервер (webhook)
  
  
Для запуска программы необходимо иметь 
- Python 3.8+
- Windows или Linux
- pip install requests tkinter (tkinter обычно уже есть в стандартной установке Python)

1. Установите PyInstaller:

pip install pyinstaller

2. Перейдите в папку проекта и выполните команду:

pyinstaller --onefile --windowed --name SoftwareScanner main_app.py

--onefile — один exe-файл
--windowed — без консоли (чисто окно программы)
--name SoftwareScanner — имя exe

Готовый файл появится в папке dist/SoftwareScanner.exe.
Важно для Windows:

Антивирусы (Windows Defender и др.) могут ругаться на exe от PyInstaller. Попросите пользователя добавить исключение или используйте --noconsole.
Можно добавить иконку: --icon myicon.ico

3. Настройка сервера 

Проект использует webhook (например, webhook.site, make.com, n8n, свой сервер и т.д.)
Рекомендуемые варианты:
Быстрый тест — https://webhook.site (бесплатно, сразу видно данные).
Свой сервер — любой endpoint, который принимает POST с JSON.

В main_app.py просто замените SERVER_URL на нужный адрес.
Пример данных, которые приходят:
{
  "pc_name": "DESKTOP-ABC123",
  "software": [
    {"name": "Google Chrome", "version": "126.0.6478.114"},
    ...
  ]
}

4. Как работает программа для пользователя

Запускает SoftwareScanner.exe
Нажимает кнопку «1. Найти программы» → идёт сканирование (может занять 10–30 сек)
Нажимает кнопку «2. Отправить на сервер» → данные улетают на webhook
JSON-файл также сохраняется рядом с exe (имя компьютера + _software.json)
