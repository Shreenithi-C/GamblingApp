from utils.db_connection import DBConnection

class GameResult:
    def __init__(self, gambler_id, bet_amount, odds_type, odds_value,
                 outcome, winnings, stake_before, stake_after):
        self.gambler_id = gambler_id
        self.bet_amount = bet_amount
        self.odds_type = odds_type
        self.odds_value = odds_value
        self.outcome = outcome
        self.winnings = winnings
        self.stake_before = stake_before
        self.stake_after = stake_after

    def save_to_db(self):
        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO game_result (gambler_id, bet_amount, odds_type, odds_value,
                                     outcome, winnings, stake_before, stake_after)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (self.gambler_id, self.bet_amount, self.odds_type,
              self.odds_value, self.outcome, self.winnings,
              self.stake_before, self.stake_after))
        conn.commit()
        cursor.close()
        db.close()

    def __str__(self):
        return (f"GameResult: Outcome={self.outcome}, Bet={self.bet_amount}, "
                f"Winnings={self.winnings}, Stake Before={self.stake_before}, "
                f"Stake After={self.stake_after}, Odds={self.odds_type} {self.odds_value}")
