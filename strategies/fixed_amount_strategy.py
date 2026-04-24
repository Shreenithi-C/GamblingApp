from strategies.base_strategy import BettingStrategy

class FixedAmountStrategy(BettingStrategy):
    def __init__(self, fixed_amount):
        self.fixed_amount = fixed_amount

    def calculate_bet(self, current_stake, last_outcome=None):
        return min(self.fixed_amount, current_stake)
