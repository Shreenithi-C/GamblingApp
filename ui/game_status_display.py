class GameStatusDisplay:
    @staticmethod
    def display_current_status(gambler_name, current_stake, session_status=None):
        print(f"\n🎮 Current Status for {gambler_name}")
        print(f"Stake: {current_stake}")
        if session_status:
            print(f"Session Status: {session_status}")

    @staticmethod
    def display_game_outcome(outcome, bet_amount, new_stake):
        print(f"\n🎲 Outcome: {outcome}")
        print(f"Bet Amount: {bet_amount}")
        print(f"Updated Stake: {new_stake}")
