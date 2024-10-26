import os
import shutil
import psutil
import time

print("!!!ВЫТАЩИТЕ ФЛЕШКУ И ВСТАВЬТЕ ЗАНОВО ВО ВРЕМЯ ОТСЧЕТА!!!")
time.sleep(1)
print("_______________________ЭТАП: ИНИЦИАЛИЗАЦИЯ ПУТЕЙ_______________________")
time.sleep(1)
user_folder = os.path.expanduser("~") #определение пути до домашнего каталога пользователя
path = os.path.join(user_folder, "AppData", "Roaming", ".minecraft", "saves") #путь до папки с картами майнкрафт
print(f"Путь до папки с картами майнкрафт: {path}")

#информация о списке дисков
def get_drives_info():
    return {d.mountpoint: d for d in psutil.disk_partitions()}.keys()

#проверка наличия флешки
def check_flash():
    #начальный список устройств
    initial = get_drives_info()
    print(f"Список начальный устройств: {', '.join(initial)}")
    print("_______________________ЭТАП: ОЖИДАНИЕ УСТРОЙСТВА(10 сек)_______________________")
    #Ожидание 5 секунд
    for i in range(1, 11):
        time.sleep(1)
        print(f"Время ожидания: {i}")

        #конечный список устройств
        dif = get_drives_info()

        #если появилось устройство
        if (len(initial) < len(dif)):
            print(f"Список конечный устройств: {', '.join(dif)}")
            return (dif - initial)
        elif(len(initial) > len(dif)):
            print(f"Не та последовательность шагов!!!")
    return "error"


def copy_directory(src, dst,filename,total_files,i):
    try:
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"Копирование {filename}: {(i + 1) / total_files * 100:.2f}% завершено")
    except PermissionError:
        print(f"_______________________ERROR: НЕТ ПРАВ НА КОПИРОВАНИЕ ДИРЕКТОРИИ {src}_______________________")
    
    
#копирование файлов
def copy_files():
    flash = "".join(check_flash())
    print("_______________________ЭТАП: КОПИРОВАНИЯ_______________________")
    #если устройство не появилось
    if (flash == "error"):
        print("_______________________ERROR: НЕТ ФЛЕШКИ_______________________")
        return input("Нажмите Enter, чтобы выйти...")
    else:
        #проверка наличия папки с картами
        path_maps = os.path.join(flash, "MyMapsMinecraft")
        if not os.path.exists(path_maps):
            os.makedirs(path_maps)
            print(f"Создание папки в {path_maps}")
        print(f"Папка с файлами: {path_maps}")

        # получение списка файлов для копирования
        files = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        total_files = len(files)

        #копирование файлов из исходной папки в папку флешки
        for i, filename in enumerate(files):
            full_filename = os.path.join(path,filename)
            copy_directory(full_filename, os.path.join(path_maps, filename),filename,total_files,i)

        print("_______________________УСПЕШНЫЙ КОНЕЦ_______________________")
    return input("Нажмите Enter, чтобы выйти...")
        
if __name__ == "__main__":
    copy_files()