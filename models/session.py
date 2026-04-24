from enum import Enum
from datetime import datetime
from services.betting_service import BettingService
from models.stake_management import StakeTransaction
from utils.enums import TransactionType

class SessionStatus(Enum):
    INITIALIZED = "INITIALIZED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ENDED_WIN = "ENDED_WIN"
    ENDED_LOSS = "ENDED_LOSS"
    ENDED_MANUAL = "ENDED_MANUAL"

class SessionEndReason(Enum):
    UPPER_LIMIT = "UPPER_LIMIT"
    LOWER_LIMIT = "LOWER_LIMIT"
    MANUAL = "MANUAL"
    TIMEOUT = "TIMEOUT"

class SessionParameters:
    def __init__(self, upper_limit, lower_limit, min_bet, max_bet, max_games, max_duration, default_probability=0.5):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.max_games = max_games
        self.max_duration = max_duration  # in minutes
        self.default_probability = default_probability

class GameRecord:
    def __init__(self, game_number, amount, outcome, stake_before, stake_after, strategy="Manual"):
        self.game_number = game_number
        self.amount = amount
        self.outcome = outcome
        self.stake_before = stake_before
        self.stake_after = stake_after
        self.strategy = strategy
        self.timestamp = datetime.now()

class GamingSession:
    def __init__(self, gambler_id, parameters: SessionParameters):
        self.gambler_id = gambler_id
        self.parameters = parameters
        self.status = SessionStatus.INITIALIZED
        self.start_time = None
        self.end_time = None
        self.records = []
        self.total_games = 0
        self.wins = 0
        self.losses = 0

    def start(self):
        self.status = SessionStatus.ACTIVE
        self.start_time = datetime.now()
        print(f"🎮 Session started for gambler {self.gambler_id}")

    def play_game(self, amount, probability=None, current_stake=0, strategy_name="Manual"):
        if self.status != SessionStatus.ACTIVE:
            print("Session not active!")
            return None

        # Validate bet amount
        if amount < self.parameters.min_bet or amount > self.parameters.max_bet:
            print("Bet amount outside allowed limits")
            return None

        prob = probability if probability else self.parameters.default_probability
        outcome, new_stake = BettingService.place_single_bet(self.gambler_id, amount, prob, current_stake, strategy="Manual")

        # Save transaction with strategy info
        tx_type = TransactionType.BET_WIN if outcome == "WIN" else TransactionType.BET_LOSS
        tx = StakeTransaction(self.gambler_id, amount, tx_type, strategy_name)
        tx.save_to_db()

        # Track in session
        record = GameRecord(self.total_games+1, amount, outcome, current_stake, new_stake, strategy_name="Manual")
        self.records.append(record)
        self.total_games += 1
        if outcome == "WIN":
            self.wins += 1
        else:
            self.losses += 1

        # Auto-end conditions
        if new_stake >= self.parameters.upper_limit:
            self.end(SessionEndReason.UPPER_LIMIT)
        elif new_stake <= self.parameters.lower_limit:
            self.end(SessionEndReason.LOWER_LIMIT)
        elif self.total_games >= self.parameters.max_games:
            self.end(SessionEndReason.TIMEOUT)

        return outcome, new_stake

    def pause(self):
        if self.status == SessionStatus.ACTIVE:
            self.status = SessionStatus.PAUSED
            print("Session paused")

    def resume(self):
        if self.status == SessionStatus.PAUSED:
            self.status = SessionStatus.ACTIVE
            print("Session resumed")

    def end(self, reason=SessionEndReason.MANUAL):
        if reason == SessionEndReason.UPPER_LIMIT:
            self.status = SessionStatus.ENDED_WIN
        elif reason == SessionEndReason.LOWER_LIMIT:
            self.status = SessionStatus.ENDED_LOSS
        else:
            self.status = SessionStatus.ENDED_MANUAL
        self.end_time = datetime.now()
        print(f"🏁 Session ended: {reason.value}")

    def summary(self):
        print(f"\n=== Session Summary for Gambler {self.gambler_id} ===")
        print(f"Status: {self.status.value}")
        print(f"Games Played: {self.total_games}, Wins: {self.wins}, Losses: {self.losses}")

        # Aggregate by strategy
        strategy_stats = {}
        for r in self.records:
            if r.strategy not in strategy_stats:
                strategy_stats[r.strategy] = {"wins": 0, "losses": 0, "total": 0}
            strategy_stats[r.strategy]["total"] += 1
            if r.outcome == "WIN":
                strategy_stats[r.strategy]["wins"] += 1
            else:
                strategy_stats[r.strategy]["losses"] += 1

        print("\n Strategy Breakdown:")
        for strategy, stats in strategy_stats.items():
            print(f"{strategy} → Wins: {stats['wins']} | Losses: {stats['losses']} | Total Bets: {stats['total']}")

        # Detailed records
        print("\n Game Records:")
        for r in self.records:
            print(f"Game {r.game_number}: {r.outcome} | Stake {r.stake_before} → {r.stake_after} | Strategy: {r.strategy} | Time: {r.timestamp}")
