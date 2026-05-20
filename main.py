# main.py
import requests 
from pydantic import BaseModel, Field, field_validator
from pathlib import Path
from datetime import datetime
import sys
import urllib3
import logging
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
class Motivation(BaseModel):
    text: str
    author: str | None = None # автор модет отсутствовать
    
    
    @field_validator('text', mode = 'before')
    @classmethod
    def trim_text(cls, v: str) -> str:
        if not isinstance(v, str):
            v = str(v)
        max_len = 200
        return v[:max_len]
        

def get_motivation() -> str:
    """Получает  мотивирующую фразу с бесплатного API"""
    try:
        # Отключаем предупреждения (необязательно, но убирает шум)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Использует публичные API с цитатами
        response = requests.get('https://api.quotable.io/random', timeout = 5, verify = False)
        data = response.json()
        
        #pydantic проверит, что пришло именно то, что мы ждем
        quote = Motivation(text = data['content'], author = data.get('author'))
        
        return f'Цитата дня: {quote.text} - {quote.author if quote.author else "Неизвестен"}'
    
    except Exception as e:
        logging.error(f'Не удалось получить цитату: {e}')
        return 'Продолжай в том же духе!'
         

def add_habbit_with_motivation(name: str):
    """Добавляет привычку в файл"""
    logging.info(f"Добавлена привычка: {name}") 
    with open(data_file, 'a') as  f:
        f.write(f'{name}, {datetime.now()}, {get_motivation()}\n')


def show_habbits():
    # показывает все привычки с мотивацией
    if data_file.exists():
        with open(data_file, "r") as f:
            for line in f:
                parts = line.strip().split(',', 2) # разделяем на 3 части
                if len(parts) == 3:
                    habit, timestamp, motivation = parts
                    logging.info(f'Найдена привычка: {habit} от {timestamp}')
                    logging.info(f'К ней прилагалась цитата: {motivation}')
    else:
        logging.warning(f'Файл с привычками не найден')
            
        
        
if __name__ == '__main__':
    add_habbit_with_motivation('прочитать 10 страниц')
    show_habbits()