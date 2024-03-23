import psycopg2
import os

# Визначення поточного місцезнаходження файлу
current_file_location = os.path.abspath("create_db.sql")

def create_db(conn, cur):
    # Перевірка існування файлу SQL
    if os.path.exists(current_file_location):
        with open(current_file_location, "r") as f:
            sql = f.read()
        try:
            # Виконання SQL команди з файлу для створення структури БД
            cur.execute(sql)
            conn.commit()
        except psycopg2.Error as e:
            # Обробка помилок при створенні таблиць
            print("Помилка при створенні таблиць:", e)
            conn.rollback()
    else:
        # Якщо файл не знайдено, виведення повідомлення про це
        print(f"Файл {current_file_location} не знайдено.")
