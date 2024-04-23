import sqlite3
import config


def create_tableevent():
    with sqlite3.connect(config.db_name) as conn:
        # Создание объекта курсора
        cursor = conn.cursor()
        create_events_table_query = f"""
        CREATE TABLE IF NOT EXISTS events (
            event_name STRING NOT NULL,
            event_margin REAL DEFAULT {0.1},
            implied_probability TEXT,
            outcome_result TEXT DEFAULT NULL,
            bet_closed INTEGER DEFAULT 0, 
            finished INTEGER DEFAULT 0
        );
        """
        # event_name - название ивента
        # event_margin - маржа брокера в долях, типо 0.1 == 10% маржи
        # implied_probability - цена ставки (win:1 lose:2 то есть расчет что, победа к поранжению шанс 1 к 2)
        # outcome_result - какая ставка выйграла
        # bet_closed - закрыт ли прием ставок
        # finished - закрыт ли ивент
        cursor.execute(create_events_table_query)


# create_tableevent()


def create_eventrow(event_name, implied_probability, margin):
    with sqlite3.connect(config.db_name) as conn:
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
        # player - никнейм поставившего
        # event_id - персональный айди у ивента
        # player_coef - коэфициент игрока во время его ставки
        # player_bet - поставленные деньги игрока
        # player_outcome - исход выбранный игроком
        # player_win - победил ли игрок?
        # payment_complete - совершена ли оплата от оргов?
        cursor.execute(create_bets_table_query)


# create_tablebet()


def create_betrow(player, event_id, player_coef, player_bet, player_outcome):
    with sqlite3.connect(config.db_name) as conn:
        # Создание объекта курсора
        cursor = conn.cursor()
        query = f'''
        INSERT INTO bets (player, event_id, player_coef, player_bet, player_outcome) VALUES (?, ?, ?, ?, ?)
                '''

        cursor.execute(query, (player, event_id, player_coef, player_bet, player_outcome))


# create_betrow("player", 1, 2.5, 1000, "win")


# create_eventrow("хуй_сосала", "{asdf:10 asdfas:20}", 0)


def get_data_for_calculation(event_id):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        query = f'''SELECT * FROM bets WHERE (player, event_id) = (?, ?)'''
        bets = cursor.execute(query, (player, event_id)).fetchall()

        return bets, bookie_knowledge, margin


from collections import defaultdict


def normalize_knowledge(bookie_knowledge):
    total = sum(bookie_knowledge.values())
    return {outcome: (knowledge / total) for outcome, knowledge in bookie_knowledge.items()}


def calculate_coefficients(bets, bookie_knowledge, margin):
    # Собираем информацию о всех ставках
    outcomes = set()
    total_amounts = {}
    for bet in bets:
        outcome, amount, _ = bet.split(':')
        outcomes.add(outcome)
        if outcome in total_amounts:
            total_amounts[outcome] += float(amount)
        else:
            total_amounts[outcome] = float(amount)

    # Нормализуем знания букмекера
    bookie_info = {k: float(v) for k, v in (item.split(':') for item in bookie_knowledge.split())}
    normalized_knowledge = normalize_knowledge(bookie_info)

    # Рассчитываем коэффициенты для каждого исхода
    total_bet_amount = sum(total_amounts.values())
    odds = {}
    for outcome in outcomes:
        # Если на исход ещё не ставили, коэффициент рассчитывается только на основе знаний букмекера и маржи
        if outcome not in total_amounts:
            odds[outcome] = 1 / (normalized_knowledge[outcome] * (1 - margin))
        else:
            # Если есть ставки, корректируем коэффициенты, учитывая уже сделанные ставки
            odds[outcome] = (total_bet_amount / total_amounts[outcome]) / (normalized_knowledge[outcome] * (1 - margin))

    # Рассчитываем ожидаемую прибыль букмекера
    bookie_profit = {}
    for outcome, total_amount in total_amounts.items():
        # Прибыль букмекера равна сумме ставок за вычетом выплат по коэффициентам
        # Применяем маржу к общему пулу ставок
        payout = total_amount * odds[outcome]
        bookie_profit[outcome] = total_bet_amount * margin - payout

    return odds, bookie_profit


bets_example = ["win:1000:1.9", "lose:500:2.3", "draw:200:3.1"]
bookie_knowledge_example = "win:1 lose:1 draw:1"
margin_example = 0.1

coefficients, bookie_profit = calculate_coefficients(bets_example, bookie_knowledge_example, margin_example)
print("Коэффициенты для следующей ставки:", coefficients)
print("Ожидаемая прибыль букмекера при каждом исходе:", bookie_profit)
