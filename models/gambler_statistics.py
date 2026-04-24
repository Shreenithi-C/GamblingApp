class GamblerStatistics:
    def __init__(self, total_bets, wins, losses, total_amount_wagered, total_amount_won, total_amount_lost):
        self.total_bets = total_bets
        self.wins = wins
        self.losses = losses
        self.total_amount_wagered = total_amount_wagered
        self.total_amount_won = total_amount_won
        self.total_amount_lost = total_amount_lost

    @property
    def win_rate(self):
        return (self.wins / self.total_bets * 100) if self.total_bets > 0 else 0

    @property
    def net_profit(self):
        return self.total_amount_won - self.total_amount_lost

    @property
    def average_bet(self):
        return (self.total_amount_wagered / self.total_bets) if self.total_bets > 0 else 0
