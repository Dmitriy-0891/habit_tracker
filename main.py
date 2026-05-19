# main.py
import requests 
from pydantic import BaseModel
import logging
from pathlib import Path
from datetime import datetime
import sys
import urllib3
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

# Модель для проверки данных API
class Dog_Image(BaseModel):
    message: str
    status: str 
    

def get_url_dog_image() -> str:
    """Получает ссылку на картинку собаки с бесплатного API"""
    try:
        # Отключаем предупреждения (необязательно, но убирает шум)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Использует публичные API с цитатами
        response = requests.get('https://dog.ceo/api/breeds/image/random', timeout = 5, verify = False)
        data = response.json()
        
        #pydantic проверит, что пришло именно то, что мы ждем
        quote = Dog_Image(message = data['message'], status = data.get('status'))
        
        return f'Картинка собаки дня: {quote.message}'
    
    except Exception as e:
        logging.error(f'Не удалось получить ссылку: {e}')
        return 'Все собаки хороши по своему!'
         

def add_habbit_with_dog_image(name: str):
    """Добавляет привычку в файл"""
    logging.info(f"Добавлена привычка: {name}") 
    with open(data_file, 'a') as  f:
        f.write(f'{name}, {datetime.now()}, {get_url_dog_image()}\n')


def show_habbits():
    # показывает все привычки с мотивацией
    if data_file.exists():
        with open(data_file, "r") as f:
            for line in f:
                parts = line.strip().split(',', 2) # разделяем на 3 части
                if len(parts) == 3:
                    habit, timestamp, dog_image = parts
                    logging.info(f'Найдена привычка: {habit} от {timestamp}')
                    logging.info(f'К ней прилагалась ссылка: {dog_image}')
    else:
        logging.warning(f'Файл с привычками не найден')
            
        
        
if __name__ == '__main__':
    add_habbit_with_dog_image('прочитать 10 страниц')
    show_habbits()