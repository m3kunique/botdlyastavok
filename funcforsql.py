import sqlite3

import config


def delete_table(table_name):
    # Подключение к базе данных
    with sqlite3.connect(config.db_name) as conn:
        # Создание объекта курсора
        cursor = conn.cursor()

        # SQL команда для удаления таблицы
        sql_query = f"DROP TABLE IF EXISTS {table_name}"

        try:
            # Выполнение команды
            if check_table_exists(table_name):
                cursor.execute(sql_query)
                print(f"Таблица {table_name} успешно удалена.")
            else:
                print(f"Таблица '{table_name}' не найдена в базе данных '{config.db_name}'.")
        except sqlite3.Error as e:
            print(f"Произошла ошибка: {e}")


def check_table_exists(table_name):
    # Подключение к базе данных
    with sqlite3.connect(config.db_name) as conn:
        # Создание объекта курсора
        cursor = conn.cursor()

        # SQL команда для проверки существования таблицы
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")

        # Получение результата запроса
        table_exists = cursor.fetchone()
        if table_exists:
            return True
        else:
            return False


def create_table(table_name):
    with sqlite3.connect(config.db_name) as conn:
        # Создание объекта курсора
        cursor = conn.cursor()

        # SQL команда для создания таблицы
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            nickname TEXT NOT NULL,
            win_lose TEXT NOT NULL,
            amount INTEGER NOT NULL,
            coef REAL NOT NULL
        );
        """

        try:
            # Выполнение команды
            if check_table_exists(table_name):
                print("Таблица уже Создана")
            else:
                cursor.execute(create_table_query)

        except sqlite3.Error as e:
            print(f"Произошла ошибка: {e}")


def get_user_by_nickname(nickname, table_name):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE nickname = ?", (nickname,))
        return cursor.fetchone()


def get_nicknames_by_win_lose(table_name, win_lose):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT nickname FROM {table_name} WHERE win_lose = ?", (win_lose,))
        return cursor.fetchall()
