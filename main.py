import psycopg2
import queries as q
from psycopg2 import sql
from create import create_db
from seed import seed_db

def main():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="mysecretpassword",
            host="localhost",
            port="5432",
        )

        cur = conn.cursor()

        create_db(conn, cur)
        seed_db(conn, cur)

        # Отримати всі завдання певного користувача.
        print(q.get_tasks_by_user(cur, 1))

        # Вибрати завдання за певним статусом.
        print(q.get_tasks_by_status(cur, "in progress"))

        # Оновити статус конкретного завдання.
        print(q.update_task_status(conn, cur, 1, "completed"))

        # Отримати список користувачів, які не мають жодного завдання.
        print(q.get_users_without_tasks(cur))

        # Додати нове завдання для конкретного користувача.
        print(q.add_task(conn, cur, "Add new task", "Article review", 1, 1))

        # Отримати всі завдання, які ще не завершено.
        print(q.get_incomplete_tasks(cur))

        # Видалити конкретне завдання.
        print(q.delete_task(conn, cur, 9))

        # Знайти користувачів з певною електронною поштою.
        print(q.find_users_by_email(cur, "random.net"))

        # Оновити ім'я користувача.
        print(q.update_user_name(conn, cur, 13, "Amend user name"))

        # Отримати кількість завдань для кожного статусу.
        print(q.count_tasks_by_status(cur))

        # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
        print(q.get_tasks_by_email_domain(cur, "example.com"))

        # Отримати список завдань, що не мають опису.
        print(q.get_tasks_without_description(cur))

        # Вибрати користувачів та їхні завдання, які є у статусі.
        print(q.get_users_and_tasks(cur, "in progress"))

        # Отримати користувачів та кількість їхніх завдань.
        print(q.get_users_with_task_counts(cur))

    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        # Handle connection error
    finally:
        # It's good practice to close the cursor and connection in a finally block.
        # This ensures they're always closed, even if an error occurs.
        if 'cur' in locals():  # Check if 'cur' is defined before trying to close it.
            cur.close()
        if 'conn' in locals():  # Check if 'conn' is defined before trying to close it.
            conn.close()

if __name__ == "__main__":
    main()



