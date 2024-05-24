import sqlite3
import requests
from bs4 import BeautifulSoup

# Подключение к базе данных
conn = sqlite3.connect('10_pages_of_news.db')
cursor = conn.cursor()

# Создание таблицы news
cursor.execute("""
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    link TEXT,
    image_link TEXT,
    date_id INTEGER,
    FOREIGN KEY (date_id) REFERENCES dates(id)
);
""")

# Создание таблицы dates 
cursor.execute("""
CREATE TABLE IF NOT EXISTS dates (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL
);
""")

# Базовый URL сайта
base_url = 'https://4pda.to/page/'

# Проходим по страницам от 1 до 10(так как запросы с 28.04)
for page_number in range(1, 11):
    # Формируем URL для каждой страницы
    url = f'{base_url}{page_number}/'
    
    # Отправляем GET-запрос на сайт
    response = requests.get(url)

    # Проверяем, что запрос был успешным
    if response.status_code == 200:
        # Парсим HTML-страницу
        soup = BeautifulSoup(response.text, 'html.parser')
           
        news_articles = soup.find_all('article')
        
        # Проходим по всем новостям и извлекаем нужные поля
        for article in news_articles:
            # Извлекаем заголовок новости
            title_element = article.find('h2')
            if title_element is not None:
                title = title_element.text.strip()
            else:
                title = None

            # Извлекаем описание новости
            description_element = article.find('p')
            if description_element is not None:
                description = description_element.text.strip()
            else:
                description = None
            
            # Извлекаем ссылку на новость
            link_element = article.find('a')
            if link_element is not None:
                link = link_element.get('href')
            else:
                link = None
            
            # Извлекаем ссылку на картинку
            image_element = article.find('img')
            if image_element is not None:
                image_link = image_element.get('src')
            else:
                image_link = None

            # Извлекаем дату
            date_element = article.find('em', class_='date')
            if date_element is not None:
                date = date_element.text.strip()
            else:
                date = None
            
            # Проверяем, что заголовок, ссылка и дата существуют, прежде чем сохранять
            if title and link and date:
                # Получаем идентификатор даты из таблицы dates или создаем новую запись
                cursor.execute('SELECT id FROM dates WHERE date = ?', (date,))
                date_id_result = cursor.fetchone()
                if date_id_result is not None:
                    date_id = date_id_result[0]
                else:
                    cursor.execute('INSERT INTO dates (date) VALUES (?)', (date,))
                    date_id = cursor.lastrowid

                # Сохраняем извлеченные данные в базу данных
                cursor.execute('''
                INSERT INTO news (title, description, link, image_link, date_id)
                VALUES (?, ?, ?, ?, ?)
                ''', (title, description, link, image_link, date_id))
                conn.commit()
    else:
        print(f'Не удалось получить доступ к сайту на странице {page_number}')

# Закрываем соединение с базой данных
conn.close()