# main.py
import logging
import sys
from pathlib import Path
from datetime import datetime

# настраиваем корневой лог, который будет выводиться на консоль
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

# Создаём обработчик для файла app.log
file_handler = logging.FileHandler('app.log')
# Указываем уровень логирования
file_handler.setLevel(logging.INFO)
# указываем формат лога
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))


# Получаем корневой логгер и добавляем файловый обработчик
root_logger = logging.getLogger()
root_logger.addHandler(file_handler)

data_file = Path("habits.txt")

def add_habbit(name: str, name_2: str):
    """Добавляет привычку в файл"""
    logging.info(f"Добавлена привычка: {name}; {name_2}") 
    with open(data_file, 'a') as  f:
        f.write(f'{name}, {name_2} {datetime.now()}\n')
        
if __name__ == '__main__':
    add_habbit('прочитать 10 страниц', 'изучить слепую печать на qwerty-клавиатуре')