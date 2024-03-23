import psycopg2
from psycopg2 import sql

def get_tasks_by_user(cur, user_id):
    # Отримати всі завдання певного користувача за його user_id
    try:
        cur.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error getting tasks by user: {e}")
        return None

def get_tasks_by_status(cur, status_name):
    # Вибрати завдання за певним статусом за допомогою підзапиту
    try:
        cur.execute(
            "SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = %s)",
            (status_name,)
        )
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error getting tasks by status: {e}")
        return None

def update_task_status(conn, cur, task_id, new_status_name):
    # Оновити статус конкретного завдання на 'in progress'
    try:
        cur.execute(
            "UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s",
            (new_status_name, task_id)
        )
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error updating task status: {e}")
        conn.rollback()

def get_users_without_tasks(cur):
    # Отримати список користувачів, які не мають жодного завдання
    try:
        cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)")
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error getting users without tasks: {e}")
        return None

def add_task(conn, cur, title, description, status_id, user_id):
    # Додати нове завдання для конкретного користувача
    try:
        cur.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id)
        )
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error adding task: {e}")
        conn.rollback()

def get_incomplete_tasks(cur):
    # Отримати всі завдання, які ще не завершено
    try:
        cur.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed')")
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error getting incomplete tasks: {e}")
        return None

def delete_task(conn, cur, task_id):
    # Видалити конкретне завдання за його id
    try:
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error deleting task: {e}")
        conn.rollback()

def find_users_by_email(cur, email_part):
    # Знайти користувачів з певною електронною поштою
    try:
        cur.execute("SELECT * FROM users WHERE email LIKE %s", ('%' + email_part + '%',))
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error finding users by email: {e}")
        return None

def update_user_name(conn, cur, user_id, new_fullname):
    # Оновити ім'я користувача
    try:
        cur.execute("UPDATE users SET fullname = %s WHERE id = %s", (new_fullname, user_id))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error updating user name: {e}")
        conn.rollback()

def count_tasks_by_status(cur):
    # Отримати кількість завдань для кожного статусу
    try:
        cur.execute("SELECT status.name, COUNT(tasks.id) FROM status LEFT JOIN tasks ON status.id = tasks.status_id GROUP BY status.name")
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error counting tasks by status: {e}")
        return None

def get_tasks_by_email_domain(cur, email_domain):
    # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
    try:
        cur.execute(
            "SELECT tasks.* FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.email LIKE %s",
            ('%' + email_domain,)
        )
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error getting tasks by email domain: {e}")
        return None

def get_tasks_without_description(cur):
    # Отримати список завдань, що не мають опису
    try:
        cur.execute("SELECT * FROM tasks WHERE description IS NULL OR description = ''")
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error getting tasks without description: {e}")
        return None

def get_users_and_tasks_in_progress(cur):
    # Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
    try:
        cur.execute(
            "SELECT users.*, tasks.* FROM users INNER JOIN tasks ON users.id = tasks.user_id INNER JOIN status ON tasks.status_id = status.id WHERE status.name = 'in progress'"
        )
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error getting users and tasks in progress: {e}")
        return None

def get_users_with_task_counts(cur):
    # Отримати користувачів та кількість їхніх завдань
    try:
        cur.execute(
            "SELECT users.fullname, COUNT(tasks.id) FROM users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.fullname"
        )
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error getting users with task counts: {e}")
        return None
