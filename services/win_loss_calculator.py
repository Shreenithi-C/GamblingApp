import random
from models.game_result import GameResult
from utils.enums import OddsType

# Outcome Strategies
class RandomOutcomeStrategy:
    def determine_outcome(self, probability: float):
        return "WIN" if random.random() < probability else "LOSS"

class WeightedProbabilityStrategy:
    def __init__(self, house_edge: float = 0.05):
        self.house_edge = house_edge

    def determine_outcome(self, probability: float):
        adjusted_prob = max(0, probability - self.house_edge)
        return "WIN" if random.random() < adjusted_prob else "LOSS"

# Statistics
class WinLossStatistics:
    def __init__(self):
        self.total_wins = 0
        self.total_losses = 0
        self.total_winnings = 0
        self.total_loss_amount = 0
        self.current_streak = 0
        self.longest_win_streak = 0
        self.longest_loss_streak = 0

    def record_result(self, outcome, amount):
        if outcome == "WIN":
            self.total_wins += 1
            self.total_winnings += amount
            self.current_streak = self.current_streak + 1 if self.current_streak >= 0 else 1
            self.longest_win_streak = max(self.longest_win_streak, self.current_streak)
        else:
            self.total_losses += 1
            self.total_loss_amount += amount
            self.current_streak = self.current_streak - 1 if self.current_streak <= 0 else -1
            self.longest_loss_streak = min(self.longest_loss_streak, self.current_streak)

    def summary(self):
        total = self.total_wins + self.total_losses
        win_rate = self.total_wins / total if total > 0 else 0
        return {
            "Wins": self.total_wins,
            "Losses": self.total_losses,
            "Win Rate": round(win_rate, 2),
            "Total Winnings": self.total_winnings,
            "Total Losses": self.total_loss_amount,
            "Longest Win Streak": self.longest_win_streak,
            "Longest Loss Streak": abs(self.longest_loss_streak)
        }

# Running Totals
class RunningTotals:
    def __init__(self, initial_stake):
        self.balance_history = [initial_stake]
        self.net_profit = 0

    def record(self, new_stake):
        self.balance_history.append(new_stake)
        self.net_profit = new_stake - self.balance_history[0]

    def summary(self):
        return {
            "Final Balance": self.balance_history[-1],
            "Net Profit": self.net_profit,
            "Balance History": self.balance_history
        }

# WinLossCalculator Service
class WinLossCalculator:
    @staticmethod
    def calculate_winnings(bet_amount, odds_type: OddsType, odds_value, outcome):
        if outcome == "LOSS":
            return 0
        if odds_type == OddsType.FIXED:
            return bet_amount * odds_value
        elif odds_type == OddsType.PROBABILITY_BASED:
            return bet_amount * (1 / odds_value)
        elif odds_type == OddsType.AMERICAN:
            if odds_value > 0:
                return bet_amount * (odds_value / 100)
            else:
                return bet_amount * (100 / abs(odds_value))
        elif odds_type == OddsType.DECIMAL:
            return bet_amount * (odds_value - 1)
        return 0

    @staticmethod
    def play_game(gambler_id, bet_amount, stake_before, strategy, odds_type, odds_value,
                  statistics: WinLossStatistics, totals: RunningTotals):
        # Determine outcome
        probability = odds_value if odds_type == OddsType.PROBABILITY_BASED else 0.5
        outcome = strategy.determine_outcome(probability)

        # Calculate winnings
        winnings = WinLossCalculator.calculate_winnings(bet_amount, odds_type, odds_value, outcome)
        stake_after = stake_before + winnings if outcome == "WIN" else stake_before - bet_amount

        # Save result
        result = GameResult(gambler_id, bet_amount, odds_type.value, odds_value,
                            outcome, winnings, stake_before, stake_after)
        result.save_to_db()

        # Update stats
        statistics.record_result(outcome, winnings if outcome == "WIN" else bet_amount)
        totals.record(stake_after)

        return result
