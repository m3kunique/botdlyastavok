import sqlite3

import config


def create_betrow(player, event_id, player_coef, player_bet, player_outcome):
    with sqlite3.connect(config.db_name) as conn:
        # Создание объекта курсора
        cursor = conn.cursor()
        query = f'''
        INSERT INTO bets (player, event_id, player_coef, player_bet, player_outcome) VALUES (?, ?, ?, ?, ?)
                '''

        cursor.execute(query, (player, event_id, player_coef, player_bet, player_outcome))


def create_eventrow(event_name, implied_probability, margin):
    with sqlite3.connect(config.db_name) as conn:
        # Создание объекта курсора
        cursor = conn.cursor()
        if margin == 0:
            query = f"""
            INSERT INTO events (event_name, implied_probability) VALUES (?, ?)
                     """

            cursor.execute(query, (event_name, implied_probability))
        else:
            query = f"""
            INSERT INTO events (event_name, implied_probability, event_margin) VALUES (?, ?, ?)
                     """
            cursor.execute(query, (event_name, implied_probability, margin))


def get_user_by_nickname(player, event_id):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM bets WHERE (player, event_id) = (?, ?)", (player, event_id))
        return cursor.fetchone()
