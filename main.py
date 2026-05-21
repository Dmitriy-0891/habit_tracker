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
class Motivation(BaseModel):
    text: str
    author: str | None = None # автор модет отсутствовать
    

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
    if not data_file.exists():
        logging.warning(f'Нет привычек. Добавьте первую: python main.py add "Выучить Python"')
        return
    with open(data_file, "r") as f:
        lines = f.readlines()
        
        if not lines:
            logging.warning(f'Файл пуст')
            return
        
        logging.info(f'Список привычек (всего: {len(lines)}):')
        print('=' * 60)
        
        
        for i, line in enumerate(lines, 1):
                parts = line.strip().split(',', 2) # разделяем на 3 части
                
                if len(parts) == 3:
                    habit, timestamp, motivation = parts
                    logging.info(f'Найдена привычка: {habit} от {timestamp}')
                    logging.info(f'К ней прилагалась цитата: {motivation}')
                    
#Функция показа сегодняшних привычек
def show_today_habits():
    """Показывает привычки добавленные сегодня"""
    if not data_file.exists():
        logging.info(f'Нет привычек')
        return
    
    today = datetime.now().date()
    found = False
    
    logging.info(f'Привычки добавленные сегодня({today}):')
    
    with open(data_file, 'r') as f:
        for line in f:
            parts = line.strip().split(', ', 2)
            if len(parts) < 2:
                continue
            
            habit_name = parts[0]
            habit_time_str = parts[1]
            habit_quote = parts[2] if len(parts) > 2 else '(без цитаты)'
            
            try:
                habit_date = datetime.strptime(habit_time_str, '%Y-%m-%d %H:%M:%S.%f').date()
            except:
                habit_date = None
                
            if habit_date == today:
                print(f'{habit_name}')
                print(f'{habit_time_str}')
                print(f'{habit_quote[:200]}')
                print()
                found = True
                
    if not found:
        logging.info(f'Сегодня еще не добавлено ни одной привычки')
        
        
# =============Справка===============

def show_help():
    """показывает справку по командам"""
    print(""" 
                        ТРЕКЕР ПРИВЫЧЕК
                    с мотивирующими цитатами
                        
                        
    Доступные команды:
    
        python main.py add 'Название'           - Добавит привычку (с цитатой дня)
        python main.py list                     - Показать все привычки с цитатами
        python main.py today                    - Показать привычки за сегодня
        python main.py help                     - Показать эту справку
        
        
    СОВЕТ:
        Цитата дня берется с API quotable.io
        Если интернет отсутствует - используется резервная фраза.
        """)

        
        
if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'add':
        if len(sys.argv) < 3:
            print('Ошибка: укажите название привычки')
            print('Пример: python main.py add  "Выучить python"')
            
        else: 
            habit_name = sys.argv[2]
            add_habbit_with_motivation(habit_name)
            
    elif command == 'list':
        show_habbits()
        
    elif command == 'today':
        show_today_habits()
        
    elif command == 'help':
        show_help()
        
    else:
        print('Неизвестная комманда: {command}')
        show_help()
    