from abc import ABC, abstractmethod

class BettingStrategy(ABC):
    @abstractmethod
    def calculate_bet(self, current_stake, last_outcome=None):
        """Return bet amount based on strategy and current stake"""
        pass
