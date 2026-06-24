import winreg
# winreg - библиотека с регистрами для Windows

# Функция, которая находит программы и их версию и сохраняет в файл, сортируя его
def get_installed_software():
    software_list = [] # Лист ПО
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ] # Пути в которых ищем программы. В этих папках находятся большинство файлов, которые могут быть интересны
    seen_names = set() # Список с найденными именами

    for hkey, subkey in reg_paths:
        # hkey и subkay - переменные путей файлов
        # hkay - голова пути
        # subkay - Остальная часть
        try:
            with winreg.OpenKey(hkey, subkey) as key: # Открываем папку
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        key_name = winreg.EnumKey(key, i) # проходимся по каждому элементу в папке
                        with winreg.OpenKey(hkey, f"{subkey}\\{key_name}") as sub_key:
                            name = winreg.QueryValueEx(sub_key, "DisplayName")[0].strip() # Берем название программы как DisplayName
                            if name and name not in seen_names:
                                version = "N/A"
                                try:
                                    version = winreg.QueryValueEx(sub_key, "DisplayVersion")[0] # Берем версию программы как DisplayVersion
                                except: pass # Если программа находит на файл, который она не может считать, то переходит к след файлу
                                software_list.append({"name": name, "version": version}) # Добавляем в лист с ПО название и версию программы
                                seen_names.add(name) # Добавляем в список с найденными именами тек имя, чтобы не добавлять его несколько раз
                    except: continue
        except: continue
    return sorted(software_list, key=lambda x: x["name"].lower()) # Сохраняем результат в json файл и передаем в осн программу