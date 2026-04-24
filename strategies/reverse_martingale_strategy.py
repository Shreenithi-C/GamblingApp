from strategies.base_strategy import BettingStrategy

class ReverseMartingaleStrategy(BettingStrategy):
    def __init__(self, base_amount):
        self.base_amount = base_amount
        self.current_bet = base_amount

    def calculate_bet(self, current_stake, last_outcome=None):
        if last_outcome == "WIN":
            self.current_bet *= 2
        elif last_outcome == "LOSS":
            self.current_bet = self.base_amount
        return min(self.current_bet, current_stake)
