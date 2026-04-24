from strategies.base_strategy import BettingStrategy

class PercentageStrategy(BettingStrategy):
    def __init__(self, percentage):
        self.percentage = percentage  # e.g. 0.05 for 5%

    def calculate_bet(self, current_stake, last_outcome=None):
        return max(1, current_stake * self.percentage)
