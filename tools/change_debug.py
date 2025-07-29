from pathlib import Path

import settings


def change_debug_value(file_path, new_value):
    try:
        # Открываем файл, читаем и обновляем его в одном проходе
        with open(file_path, 'r+') as file:
            lines = file.readlines()
            # Перезаписываем файл с новым значением debug
            file.seek(0)
            file.writelines(f'debug={new_value}\n' if line.startswith('debug=') else line for line in lines)

        print(f"debug value has been changed to {new_value}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Пример использования
plugins_path = Path(r'C:\Users\Zebaro\AppData\Roaming\HotSpot\StreamDock\plugins')

domain_parts = settings.DOMAIN.split('.')
reversed_parts = domain_parts[::-1]
name_list = settings.NAME.split()
pascal_name = name_list[0].lower() + ''.join(word.capitalize() for word in name_list[1:])
reversed_parts.append(pascal_name)
reversed_parts.append('sdPlugin')
folder_name = '.'.join(reversed_parts)

config_file_path = plugins_path / folder_name / 'plugin' / "config.json"
print(config_file_path)

# change_debug_value(config_file_path, '0')  # Меняем debug на 0
