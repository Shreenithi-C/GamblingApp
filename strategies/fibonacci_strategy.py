from strategies.base_strategy import BettingStrategy

class FibonacciStrategy(BettingStrategy):
    def __init__(self, base_amount):
        self.base_amount = base_amount
        self.sequence = [1, 1]
        self.index = 0

    def calculate_bet(self, current_stake, last_outcome=None):
        if last_outcome == "LOSS":
            self.index += 1
            if self.index >= len(self.sequence):
                self.sequence.append(self.sequence[-1] + self.sequence[-2])
        elif last_outcome == "WIN":
            self.index = max(0, self.index - 2)

        bet = self.base_amount * self.sequence[self.index]
        return min(bet, current_stake)
