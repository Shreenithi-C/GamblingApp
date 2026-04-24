from utils.db_connection import DBConnection
from utils.enums import TransactionType
import datetime

# 1. StakeTransaction Class

class StakeTransaction:
    def __init__(self, gambler_id, amount, transaction_type, strategy=None, balance_after=None, bet_id=None):
        self.gambler_id = gambler_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.strategy = strategy
        self.balance_after = balance_after
        self.bet_id = bet_id
        self.timestamp = datetime.datetime.now()

    def save_to_db(self):
        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO stake_transaction (gambler_id, amount, transaction_type, strategy, balance_after, bet_id, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (self.gambler_id, self.amount, self.transaction_type.value, self.strategy, self.balance_after, self.bet_id, self.timestamp))

        conn.commit()
        cursor.close()
        db.close()

        print(f"Transaction {self.transaction_type.name} of {self.amount} saved for gambler {self.gambler_id} using {self.strategy or 'N/A'} strategy")

# 3. StakeBoundary Class

class StakeBoundary:
    def __init__(self, min_stake, max_stake):
        self.min_stake = min_stake
        self.max_stake = max_stake

    def check_boundary(self, current_stake):
        warnings = []
        if current_stake < self.min_stake:
            warnings.append("⚠️ Stake below minimum limit!")
        elif current_stake < self.min_stake * 1.2:
            warnings.append("⚠️ Stake approaching minimum limit.")

        if current_stake > self.max_stake:
            warnings.append("⚠️ Stake exceeded maximum limit!")
        elif current_stake > self.max_stake * 0.8:
            warnings.append("⚠️ Stake approaching maximum limit.")

        return warnings

# 4. StakeMonitor Class

class StakeMonitor:
    def __init__(self, initial_stake):
        self.initial_stake = initial_stake
        self.current_stake = initial_stake
        self.peak_stake = initial_stake
        self.low_stake = initial_stake
        self.history = []

    def record_change(self, new_stake):
        self.current_stake = new_stake
        self.peak_stake = max(self.peak_stake, new_stake)
        self.low_stake = min(self.low_stake, new_stake)
        self.history.append((datetime.datetime.now(), new_stake))

    def volatility(self):
        return (self.peak_stake - self.low_stake) / self.initial_stake if self.initial_stake > 0 else 0

# 5. StakeHistoryReport Class

class StakeHistoryReport:
    @staticmethod
    def generate(gambler_id):
        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()

        print(f"\n=== Stake History Report for Gambler {gambler_id} ===")

        # --- Stake Transactions ---
        cursor.execute("""
            SELECT transaction_type, amount, balance_after, timestamp, strategy
            FROM stake_transaction
            WHERE gambler_id = %s
            ORDER BY timestamp
        """, (gambler_id,))
        stake_rows = cursor.fetchall()

        print("\n--- Stake Transactions ---")
        total_win = total_loss = total_bets = 0
        for r in stake_rows:
            tx_type = r[0].upper() if r[0] else ""
            print(f"{r[3]} | {tx_type} | Amount: {r[1]} | Balance After: {r[2]} | Strategy: {r[4] or 'Manual'}")

            if tx_type == TransactionType.BET_WIN.value.upper():
                total_win += float(r[1])
                total_bets += 1
            elif tx_type == TransactionType.BET_LOSS.value.upper():
                total_loss += float(r[1])
                total_bets += 1

        net_profit = total_win - total_loss
        print(f"\nStake Summary: Total Bets={total_bets}, Wins={total_win}, Losses={total_loss}, Net Profit={net_profit}")

        # Game Results ---
        cursor.execute("""
            SELECT bet_amount, odds_type, odds_value, outcome, winnings,
                   stake_before, stake_after, timestamp
            FROM game_result
            WHERE gambler_id = %s
            ORDER BY timestamp
        """, (gambler_id,))
        game_rows = cursor.fetchall()

        print("\n--- Game Results ---")
        game_wins = game_losses = 0
        total_winnings = total_losses = 0
        for g in game_rows:
            print(f"{g[7]} | Outcome={g[3]} | Bet={g[0]} | Odds={g[1]} {g[2]} | "
                  f"Winnings={g[4]} | Stake Before={g[5]} | Stake After={g[6]}")

            if g[3] == "WIN":
                game_wins += 1
                total_winnings += float(g[4])
            else:
                game_losses += 1
                total_losses += float(g[0])

        total_games = game_wins + game_losses
        win_rate = round(game_wins / total_games, 2) if total_games > 0 else 0
        print(f"\nGame Summary: Games={total_games}, Wins={game_wins}, Losses={game_losses}, "
              f"Win Rate={win_rate}, Total Winnings={total_winnings}, Total Losses={total_losses}, "
              f"Net Profit={total_winnings - total_losses}")

        cursor.close()
        db.close()

# 6. StakeManagementService

class StakeManagementService:
    @staticmethod
    def initialize_stake(gambler_id, initial_amount):
        tx = StakeTransaction(gambler_id, initial_amount, TransactionType.INITIAL_STAKE, balance_after=initial_amount)
        tx.save_to_db()
        return initial_amount

    @staticmethod
    def process_bet(gambler_id, amount, outcome, current_stake, strategy=None, bet_id=None):
        if outcome == "WIN":
            new_stake = current_stake + amount
            tx_type = TransactionType.BET_WIN
        else:
            new_stake = current_stake - amount
            tx_type = TransactionType.BET_LOSS

        tx = StakeTransaction(gambler_id, amount, tx_type, strategy=strategy, balance_after=new_stake, bet_id=bet_id)
        tx.save_to_db()
        return new_stake

    @staticmethod
    def validate_boundaries(boundary: StakeBoundary, current_stake):
        return boundary.check_boundary(current_stake)

    @staticmethod
    def monitor_stake(monitor: StakeMonitor, new_stake):
        monitor.record_change(new_stake)
        return monitor.volatility()

    @staticmethod
    def generate_report(gambler_id):
        StakeHistoryReport.generate(gambler_id)
