import sqlite3

import config


# создать ставку
def create_betrow(player, event_id, player_coef, player_bet, player_outcome):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()

        query = f'''
        INSERT INTO bets (player, event_id, player_coef, player_bet, player_outcome) VALUES (?, ?, ?, ?, ?)
                '''

        cursor.execute(query, (player, event_id, player_coef, player_bet, player_outcome))


# получить event_id через event name
def get_event_id(event_name):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        query = f'''
        SELECT event_id FROM events WHERE event_name = {event_name}
                '''
        cursor.execute(query)
        return cursor.fetchone()


# закрытие ставки
def close_bet(event_id):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        query = f"""
                UPDATE events SET bet_closed = 1 WHERE event_id = {event_id};
            """
        cursor.execute(query)
        return True


# закрыть ивент
def set_finished(event_id, outcome_result):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        query = f"""
                UPDATE events SET (finished, outcome_result) VALUES (?, ?) WHERE event_id = {event_id};
            """
        cursor.execute(query, (1, outcome_result))


# создать ивент
def create_eventrow(event_name, implied_probability, margin):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        if margin == 0:
            query = f"""
            INSERT INTO events (event_name, implied_probability) VALUES (?, ?)
                     """

            cursor.execute(query, (event_name, implied_probability))
            return True
        elif margin != 0:
            query = f"""
            INSERT INTO events (event_name, implied_probability, event_margin) VALUES (?, ?, ?)
                     """
            cursor.execute(query, (event_name, implied_probability, margin))
            return True
        else:
            return False


# получить информацию о юзере
def get_user_by_nickname(player, event_id):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        if event_id == '-':
            query = f'''SELECT * FROM bets WHERE (player, event_id) = (?, ?)'''
            cursor.execute(query, (player, event_id))
        else:
            query = f'''SELECT * FROM bets WHERE (player) = {player}'''
            cursor.execute(query)
        return cursor.fetchall()


def get_data_for_calculation(event_id):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        # todo доделать получение data из дб
        # return bets, bookie_knowledge, margin
