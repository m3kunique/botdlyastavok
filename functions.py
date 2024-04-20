import sqlite3
import config
from collections import defaultdict

def calculate_coefficients(bets, bookie_knowledge, margin):
    """
    Рассчитывает коэффициенты для каждого исхода на основе ставок, знаний букмекера и маржи.

    :param bets: список ставок в формате "имя:исход:сумма"
    :param bookie_knowledge: словарь знаний букмекера об исходах (вероятности не обязательно суммируются в 100%)
    :param margin: маржа букмекера
    :return: словарь коэффициентов для каждого исхода
    """
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

def delete_table(table_name):
    """
    Удаляет таблицу из базы данных.

    :param table_name: имя таблицы для удаления
    """
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        sql_query = f"DROP TABLE IF EXISTS {table_name}"

        try:
            if check_table_exists(table_name):
                cursor.execute(sql_query)
                print(f"Таблица {table_name} успешно удалена.")
            else:
                print(f"Таблица '{table_name}' не найдена в базе данных '{config.db_name}'.")
        except sqlite3.Error as e:
            print(f"Произошла ошибка: {e}")

def check_table_exists(table_name):
    """
    Проверяет наличие таблицы в базе данных.

    :param table_name: имя проверяемой таблицы
    :return: True если таблица существует, иначе False
    """
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = cursor.fetchone()
        return bool(table_exists)

def create_table(table_name):
    """
    Создает таблицу в базе данных если она не существует.

    :param table_name: имя создаваемой таблицы
    """
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
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
            if check_table_exists(table_name):
                print("Таблица уже создана")
            else:
                cursor.execute(create_table_query)
        except sqlite3.Error as e:
            print(f"Произошла ошибка: {e}")

def calculate_coefficient(win, lose, margin):
    """
    Рассчитывает коэффициент для одного исхода.

    :param win: сумма ставок на выигрыш
    :param lose: сумма ставок на проигрыш
    :param margin: маржа букмекера
    :return: коэффициент для исхода
    """
    if lose == 0:
        return 1
    win_with_margin = win * (1 + margin)
    return round((win_with_margin + lose) / win_with_margin, 2)

def f_CalculationCoefs(winlose, margin):
    """
    Функция для расчета коэффициентов, используя маржу букмекера.

    :param winlose: исход (True для выигрыша, False для проигрыша)
    :param margin: процент маржи
    :return: коэффициент для указанного исхода
    """
    bookmaker_margin = margin/100  # Преобразование процента в десятичное число

    win_amount = 0  # todo добавить логику ввода суммы
    lose_amount = 0  # todo добавить логику ввода суммы

    if winlose:
        return calculate_coefficient(win_amount, lose_amount, bookmaker_margin)
    else:
        return calculate_coefficient(lose_amount, win_amount, bookmaker_margin)
