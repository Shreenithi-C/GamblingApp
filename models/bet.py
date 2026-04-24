import random
from utils.db_connection import DBConnection

class Bet:
    def __init__(self, gambler_id, amount, probability):
        if not (0 <= probability <= 1):
            raise ValueError("Probability must be between 0 and 1")
        self.gambler_id = gambler_id
        self.amount = amount
        self.probability = probability
        self.outcome = None
        self.stake_before = None
        self.stake_after = None

    def place_bet(self, current_stake):
        self.stake_before = current_stake
        if random.random() <= self.probability:
            self.outcome = "WIN"
            self.stake_after = current_stake + self.amount
        else:
            self.outcome = "LOSS"
            self.stake_after = current_stake - self.amount
        self.save_to_db()
        return self.outcome, self.stake_after

    def save_to_db(self):
        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()
        query = """
        INSERT INTO bet (gambler_id, amount, probability, outcome)
        VALUES (%s, %s, %s, %s)
        """
        values = (self.gambler_id, self.amount, self.probability, self.outcome)
        cursor.execute(query, values)
        conn.commit()
        print(f"Bet saved: Gambler {self.gambler_id}, Amount {self.amount}, Outcome {self.outcome}")
        db.close()
