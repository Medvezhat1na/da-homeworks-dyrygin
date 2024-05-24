import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('for_requests_of_news.db')
cursor = conn.cursor()

# Запрос 1: Выбрать все новости, в заголовке которых фигурирует слово "Смута" (вместе с падежами) в период с 28.04.2024
query1 = """
SELECT n.id, n.title, n.description, n.link, n.image_link, d.date
FROM news n
JOIN dates d ON n.date_id = d.id
WHERE n.title LIKE '%Смут%';
"""
cursor.execute(query1)
news_with_smuta = cursor.fetchall()

# Запрос 2: Подсчитать за каждый день выборки количество новостей, и количество новостей со словом "Смута"
query2 = """
SELECT d.date, COUNT(n.id) AS total_news,
       SUM(CASE WHEN n.title LIKE '%Смут%' THEN 1 ELSE 0 END) AS smuta_news
FROM dates d
LEFT JOIN news n ON n.date_id = d.id
GROUP BY d.date;
"""
cursor.execute(query2)
news_count_by_date = cursor.fetchall()

# Закрываем соединение с базой данных
conn.close()

# Сохранение результатов 1 запроса в файл
with open('news_with_smuta.txt', 'w', encoding='utf-8') as file:
    file.write("Новости, в заголовке которых фигурирует слово 'Смута':\n")
    for news in news_with_smuta:
        file.write(str(news) + '\n')

# Сохранение результатов 2 запроса в файл
with open('news_count_by_date.txt', 'w', encoding='utf-8') as file:
    file.write("Количество новостей и слов 'Смута' по дням:\n")
    for date_data in news_count_by_date:
        file.write(f"Дата: {date_data[0]}, Всего новостей: {date_data[1]}, Слов 'Смута': {date_data[2]}\n")

print("Результаты запросов сохранены в файлы 'news_with_smuta.txt' и 'news_count_by_date.txt'.")