import sqlite3
import config


def create_tableevent():
    with sqlite3.connect(config.db_name) as conn:
        # Создание объекта курсора
        cursor = conn.cursor()
        create_events_table_query = f"""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name STRING NOT NULL,
            event_margin REAL DEFAULT {0.1},
            implied_probability TEXT,
            outcome_result TEXT DEFAULT NULL,
            finished INTEGER DEFAULT 0
        );
        """

        cursor.execute(create_events_table_query)


create_tableevent()


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


# create_eventrow("event_name", "{win:1 lose:2}", 0)


def create_tablebet():
    with sqlite3.connect(config.db_name) as conn:
        # Создание объекта курсора
        cursor = conn.cursor()
        create_bets_table_query = f"""
                CREATE TABLE IF NOT EXISTS bets (
                    player TEXT NOT NULL,
                    event_id INTEGER,
                    player_coef REAL,
                    player_bet INTEGER,
                    player_outcome STRING,
                    player_win INTEGER DEFAULT {0},
                    payment_complete INTEGER DEFAULT {0},
                    FOREIGN KEY(event_id) REFERENCES events(event_id)            
                );
                """

        cursor.execute(create_bets_table_query)


create_tablebet()


def create_betrow(player, event_id, player_coef, player_bet, player_outcome):
    with sqlite3.connect(config.db_name) as conn:
        # Создание объекта курсора
        cursor = conn.cursor()
        query = f'''
        INSERT INTO bets (player, event_id, player_coef, player_bet, player_outcome) VALUES (?, ?, ?, ?, ?)
                '''

        cursor.execute(query,(player, event_id, player_coef, player_bet, player_outcome))


# create_betrow("player", 1, 2.5, 1000, "win")


# create_eventrow("хуй_сосала", "{asdf:10 asdfas:20}", 0)
