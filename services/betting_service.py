import random
from models.stake_management import StakeTransaction
from utils.enums import TransactionType

class BettingService:
    @staticmethod
    def place_single_bet(gambler_id, amount, probability, current_stake, strategy=None, bet_id=None):
        """Place a single bet and record transaction"""
        outcome = "WIN" if random.random() < probability else "LOSS"
        new_stake = current_stake + amount if outcome == "WIN" else current_stake - amount

        # Map outcome to TransactionType enum
        transaction_type = TransactionType.BET_WIN if outcome == "WIN" else TransactionType.BET_LOSS

        # Save transaction with strategy name if provided
        tx = StakeTransaction(
            gambler_id,
            amount,
            transaction_type,
            strategy=strategy,
            balance_after=new_stake,
            bet_id=bet_id
        )
        tx.save_to_db()

        return outcome, new_stake

    @staticmethod
    def place_bet_with_strategy(gambler_id, strategy, probability, current_stake, last_outcome=None):
        """Place a bet using a strategy"""
        amount = strategy.calculate_bet(current_stake, last_outcome)
        outcome, new_stake = BettingService.place_single_bet(
            gambler_id,
            amount,
            probability,
            current_stake,
            strategy=strategy.__class__.__name__
        )
        return outcome, new_stake, amount

    @staticmethod
    def place_consecutive_bets(gambler_id, strategy, probability, current_stake, num_bets):
        """Run multiple consecutive bets with a strategy"""
        results = []
        stake = current_stake
        last_outcome = None
        for i in range(num_bets):
            outcome, stake, amount = BettingService.place_bet_with_strategy(
                gambler_id, strategy, probability, stake, last_outcome
            )
            results.append((i+1, amount, outcome, stake))
            last_outcome = outcome
        return results
