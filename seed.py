from faker import Faker
import psycopg2
import random

def seed_db(conn, cur):
    fake = Faker()
    used_emails = set()  # Set to keep track of already used emails

    # Створення 150 фейкових користувачів
    while len(used_emails) < 150:
        fullname = fake.name()  # Генерація повного імені
        email = fake.email()  # Try to generate a unique email
        if email in used_emails:
            continue  # Skip this iteration if the email is already used
        used_emails.add(email)  # Add the new unique email to the set

        try:
            # Вставка даних користувача в таблицю users
            cur.execute(
                "INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email)
            )
            conn.commit()
        except psycopg2.Error as e:
            print("Помилка при заповненні даних (додавання користувача):", e)
            conn.rollback()

    # Статуси для завдань
    statuses = ["new", "in progress", "completed"]
    for status in statuses:
        try:
            # Вставка статусів в таблицю status
            cur.execute("INSERT INTO status (name) VALUES (%s)", (status,))
            conn.commit()
        except psycopg2.Error as e:
            print("Помилка при заповненні даних (додавання статусу):", e)
            conn.rollback()

    # Створення 150 завдань з випадковими статусами і користувачами
    for _ in range(150):
        title = fake.sentence()  # Генерація назви завдання
        description = fake.text()  # Генерація опису завдання
        status_id = random.randint(1, len(statuses))  # Вибір випадкового статусу
        user_id = random.randint(1, 150)  # Вибір випадкового користувача
        try:
            # Вставка завдання в таблицю tasks
            cur.execute(
                "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                (title, description, status_id, user_id),
            )
            conn.commit()
        except psycopg2.Error as e:
            print("Помилка при заповненні даних (додавання завдання):", e)
            conn.rollback()
