from models.gambler_profile import GamblerProfile, BettingPreferences
from models.gambler_statistics import GamblerStatistics

class GamblerProfileService:
    @staticmethod
    def create_profile(name, initial_stake, win_threshold, loss_threshold):
        if GamblerProfile.validate_eligibility(initial_stake):
            gambler = GamblerProfile(name, initial_stake, win_threshold, loss_threshold)
            gambler.save_to_db()
            return gambler
        else:
            raise ValueError("Initial stake too low! Minimum required is 100.")

    @staticmethod
    def update_profile(gambler_id, name=None, preferences: BettingPreferences=None, win_threshold=None, loss_threshold=None):
        gambler = GamblerProfile.get_by_id(gambler_id)
        if name: gambler.name = name
        if preferences: gambler.preferences = preferences
        if win_threshold: gambler.win_threshold = win_threshold
        if loss_threshold: gambler.loss_threshold = loss_threshold
        gambler.update_in_db()

    @staticmethod
    def retrieve_statistics(gambler_id):
        stats = GamblerProfile.get_statistics(gambler_id)
        return GamblerStatistics(**stats)

    @staticmethod
    def reset_profile(gambler_id):
        gambler = GamblerProfile.get_by_id(gambler_id)
        # proportional reset: thresholds scale with initial stake
        factor = gambler.initial_stake / gambler.current_stake if gambler.current_stake > 0 else 1
        gambler.current_stake = gambler.initial_stake
        gambler.win_threshold *= factor
        gambler.loss_threshold *= factor
        gambler.reset_in_db()
