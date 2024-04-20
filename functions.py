import sqlite3
import config
from collections import defaultdict


def calculate_coefficients(bets, bookie_knowledge, margin):
    # Нормализация bookie_knowledge, если сумма вероятностей не равна 100%
    bookie_knowledge_sum = sum(bookie_knowledge.values())
    if bookie_knowledge_sum != 100:
        bookie_knowledge = {outcome: (probability / bookie_knowledge_sum * 100)
                            for outcome, probability in bookie_knowledge.items()}

    outcome_amounts = defaultdict(float)
    for bet in bets:
        name, outcome, bet_amount = bet.split(':')
        outcome_amounts[outcome] += float(bet_amount)

    total_staked = sum(outcome_amounts.values())

    coefficients = {}
    for outcome, amount in outcome_amounts.items():
        bookie_probability = bookie_knowledge[outcome] / 100
        true_probability = amount / total_staked
        adjusted_probability = true_probability * bookie_probability
        bookie_odds = adjusted_probability / (1 - margin)
        coefficient = 1 / bookie_odds
        coefficients[outcome] = round(coefficient, 2)

    return coefficients
# пример выполнения функции
# bets = [
#     "player1:win:1000",
#     "player2:lose:800","player1:win:1000",
#     "player2:lose:800","player1:win:1000",
#     "player2:lose:800","player1:win:1000",
#     "player2:lose:800","player1:win:1000",
#     "player2:lose:800","player1:win:1000",
#     "player2:lose:800","player1:win:1000",
# ]
#
# # Знания букмекера о вероятностях исходов, которые могут не совсем равняться 100%
# bookie_knowledge = {
#     "win": 100,
#     "lose": 50,
#     # Пропорция не равна 100%, функция нормализует эти значения
# }
# coefficients = calculate_coefficients(bets, bookie_knowledge, margin)
# for outcome, coefficient in coefficients.items():
#     print(f"Outcome: {outcome}, Coefficient: {coefficient}")


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
            win_lose TEXT CHECK(win_lose IN ('win', 'lose')) NOT NULL,
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


def calculate_coefficient(win, lose, margin):
    if lose == 0:
        return 1
    win_with_margin = win * (1 + margin)
    return round((win_with_margin + lose) / win_with_margin, 2)


def f_CalculationCoefs(winlose, margin):
    bookmaker_margin = margin/100  # 10% маржа

    win_amount = 0
    lose_amount = 0

    # todo ввод данных и количество исходов

    if winlose:
        return calculate_coefficient(win_amount, lose_amount, bookmaker_margin)
    else:
        return calculate_coefficient(lose_amount, win_amount, bookmaker_margin)



