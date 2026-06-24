#Используем platform, чтобы работать с win/lin
import platform
import subprocess
import winreg

# Поиск ПО в зависимости от системы
def get_installed_software():
    system = platform.system()
    if system == "Windows":
        return _get_windows_software()
    elif system == "Linux":
        return _get_linux_software()
    return []

def _get_windows_software():
    software_list = []
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]
    seen_names = set()
    for hkey, subkey in reg_paths:
        try:
            with winreg.OpenKey(hkey, subkey) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        key_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(hkey, f"{subkey}\\{key_name}") as sub_key:
                            name = winreg.QueryValueEx(sub_key, "DisplayName")[0].strip()
                            if name and name not in seen_names:
                                version = "N/A"
                                try:
                                    version = winreg.QueryValueEx(sub_key, "DisplayVersion")[0]
                                except: pass
                                software_list.append({"name": name, "version": version})
                                seen_names.add(name)
                    except: continue
        except: continue
    return sorted(software_list, key=lambda x: x["name"].lower())

def _get_linux_software():
    software_list = []
    try:
        # Получаем список пакетов через dpkg
        output = subprocess.check_output(["dpkg-query", "-W", "-f=${Package} ${Version}\n"], text=True)
        for line in output.splitlines():
            parts = line.split(" ", 1)
            if len(parts) == 2:
                software_list.append({"name": parts[0], "version": parts[1]})
    except Exception:
        pass
    return sorted(software_list, key=lambda x: x["name"].lower())