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
    logging.info(f"Добавлены привычки: 1){name}; 2){name_2}") 
    with open(data_file, 'a') as  f:
        f.write(f'{name}, {name_2} - {datetime.now()}\n')


def show_habbits():
    if data_file.exists():
        with open(data_file, "r") as f:
            for line in f:
                habit_name = line.split('-')[0]
                logging.info(f'Найдены привычки: {habit_name}')
    else:
        logging.warning(f'Файл с привычками не найден')
            
        
        
if __name__ == '__main__':
    add_habbit('прочитать 10 страниц', 'изучить слепую печать на qwerty-клавиатуре')
    show_habbits()