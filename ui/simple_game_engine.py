from ui.game_status_display import GameStatusDisplay
from ui.interactive_menu import InteractiveMenu
from ui.session_summary import SessionSummary
from services.win_loss_calculator import (
    WinLossCalculator, RandomOutcomeStrategy,
    WinLossStatistics, RunningTotals
)
from utils.enums import OddsType

class SimpleGameEngine:
    def __init__(self, gambler_name, initial_stake):
        self.gambler_name = gambler_name
        self.current_stake = initial_stake
        self.statistics = WinLossStatistics()
        self.totals = RunningTotals(initial_stake)

    def play_round(self):
        GameStatusDisplay.display_current_status(self.gambler_name, self.current_stake)

        bet_amount = InteractiveMenu.prompt_for_bet_amount()
        odds_type = OddsType.FIXED
        odds_value = 2  # simple fixed odds demo
        strategy = RandomOutcomeStrategy()

        result = WinLossCalculator.play_game(
            gambler_id=1, bet_amount=bet_amount, stake_before=self.current_stake,
            strategy=strategy, odds_type=odds_type, odds_value=odds_value,
            statistics=self.statistics, totals=self.totals
        )

        self.current_stake = result.stake_after
        GameStatusDisplay.display_game_outcome(result.outcome, bet_amount, self.current_stake)

    def end_session(self):
        SessionSummary.display_session_summary(self.gambler_name, self.statistics, self.totals)
