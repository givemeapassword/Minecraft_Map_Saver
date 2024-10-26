import os
import shutil
import psutil
import time


print("_______________________ЭТАП: ИНИЦИАЛИЗАЦИЯ ПУТЕЙ_______________________")
user_folder = os.path.expanduser("~") #определение пути до домашнего каталога пользователя
path = user_folder + "\AppData\Roaming\.minecraft\saves" #путь до папки с картами майнкрафт
print(f"Путь до папки с картами майнкрафт: {path}")

#информация о списке дисков
def get_drives_info():
    return {d.mountpoint: d for d in psutil.disk_partitions()}.keys()

#проверка наличия флешки
def check_flash():
    #начальный список устройств
    initial = get_drives_info()
    print(f"Список начальный устройств: {', '.join(initial)}")
    print("_______________________ЭТАП: ОЖИДАНИЕ УСТРОЙСТВА(5 сек)_______________________")
    #Ожидание 5 секунд
    for i in range(1, 6):
        time.sleep(1)
        print(f"Время ожидания: {i} ")

        #конечный список устройств
        dif = get_drives_info()

        #если появилось устройство
        if (len(initial) < len(dif)):
            print(f"Список конечный устройств: {', '.join(dif)}")
            return (dif - initial)
    return "error"

    
#копирование файлов
def copy_files():
    flash = "".join(check_flash())
    print("_______________________ЭТАП: КОПИРОВАНИЯ_______________________")
    #если устройство не появилось
    if (flash == "error"):
        print("_______________________ERROR: НЕТ ФЛЕШКИ_______________________")
        return
    else:
        #проверка наличия папки с картами
        print(os.path.join(flash,"MyMapsMinecraft"))
        path_maps = os.path.join(flash, "MyMapsMinecraft")
        if not os.path.exists(path_maps):
            os.makedirs(path_maps)
            print(f"Создание папки в {path_maps}")
        print(f"Папка с файлами: {path_maps}")
        #копирование файлов из исходной папки в папку флешки
        for filename in os.listdir(path):
            full_filename = os.path.join(path,filename)
            if (os.path.isdir(full_filename)):
                try:
                    shutil.copy(full_filename, path_maps)
                except PermissionError:
                    print(f"_______________________ERROR: НЕТ ПРАВ НА КОПИРОВАНИЕ ДИРЕКТОРИИ {full_filename}_______________________")
        print("_______________________УСПЕШНЫЙ КОНЕЦ_______________________")
    input("Нажмите Enter, чтобы выйти...")
        
if __name__ == "__main__":
    copy_files()