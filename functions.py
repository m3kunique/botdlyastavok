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










