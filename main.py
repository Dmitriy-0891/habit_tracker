# main.py
import logging
from pathlib import Path
from datetime import datetime

# Натсраиваю логирование (вместо print())
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', force=True)

data_file = Path("habits.txt")

def add_habbit(name: str):
    """Добавляет привычку в файл"""
    logging.info(f"Добавлена привычка: {name}") 
    with open(data_file, 'a') as  f:
        f.write(f'{name}, {datetime.now()}\n')
        
if __name__ == '__main__':
    add_habbit('прочитать 10 страниц')
    print('программа завершила работу')