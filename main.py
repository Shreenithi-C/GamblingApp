from models.gambler_profile import GamblerProfile
from services.betting_service import BettingService
from services.input_validator import InputValidator, ValidationConfig
from services.safe_input_handler import SafeInputHandler
from models.stake_management import StakeHistoryReport
from models.session import GamingSession, GameRecord, SessionParameters, SessionStatus
from reset_db import reset_database
from services.win_loss_calculator import (
    WinLossCalculator, RandomOutcomeStrategy,
    WeightedProbabilityStrategy, WinLossStatistics, RunningTotals
)
from utils.enums import OddsType

# UI classes
from ui.interactive_menu import InteractiveMenu
from ui.simple_game_engine import SimpleGameEngine
from ui.game_status_display import GameStatusDisplay
from ui.session_summary import SessionSummary

# Import strategies
from strategies.fixed_amount_strategy import FixedAmountStrategy
from strategies.percentage_strategy import PercentageStrategy
from strategies.martingale_strategy import MartingaleStrategy
from strategies.reverse_martingale_strategy import ReverseMartingaleStrategy
from strategies.fibonacci_strategy import FibonacciStrategy
from strategies.dalembert_strategy import DalembertStrategy

# Keep a reference to the current session
current_session = None

# Menu Display

def main_menu():
    InteractiveMenu.display_main_menu()

# Menu Action Functions

def create_profile():
    name = input("Enter gambler name: ")
    initial_stake = float(input("Enter initial stake: "))
    win_threshold = float(input("Enter win threshold: "))
    loss_threshold = float(input("Enter loss threshold: "))

    if GamblerProfile.validate_eligibility(initial_stake):
        gambler = GamblerProfile(name, initial_stake, win_threshold, loss_threshold)
        gambler.save_to_db()
        print(f"Gambler {name} created successfully.")
    else:
        print("Initial stake too low! Minimum required is 100.")

def view_profiles():
    profiles = GamblerProfile.get_all()
    print("\n All Profiles:")
    for p in profiles:
        print(f"ID: {p[0]} | Name: {p[1]} | Stake: {p[2]} | Wins: {p[3]} | Losses: {p[4]} | Total Bets: {p[5]}")

def place_bet():
    gambler_id = int(input("Enter gambler ID: "))

    # Validated stake
    current_stake = safe_input.get_validated_input(
        "Enter current stake: ",
        validator.validate_initial_stake
    )

    # Validated bet amount
    bet_amount = safe_input.get_validated_input(
        "Enter bet amount: ",
        validator.validate_bet_amount,
        current_stake
    )

    # Validated probability
    probability = safe_input.get_validated_input(
        "Enter win probability (0-1): ",
        validator.validate_probability
    )

    # Continue with existing betting logic
    outcome, new_stake = BettingService.place_single_bet(
        gambler_id, bet_amount, probability, current_stake, strategy="Manual"
    )
    GameStatusDisplay.display_game_outcome(outcome, bet_amount, new_stake)

def view_stake_history():
    gambler_id = int(input("Enter gambler ID: "))
    StakeHistoryReport.generate(gambler_id)

def reset_profile():
    gambler_id = int(input("Enter gambler ID: "))
    GamblerProfile.reset_profile(gambler_id)
    print(f"Gambler {gambler_id} profile reset.")

def update_profile():
    gambler_id = int(input("Enter gambler ID: "))
    name = input("Enter new name (leave blank to skip): ")
    win_threshold = input("Enter new win threshold (leave blank to skip): ")
    loss_threshold = input("Enter new loss threshold (leave blank to skip): ")

    GamblerProfile.update_profile(
        gambler_id,
        name=name if name else None,
        win_threshold=float(win_threshold) if win_threshold else None,
        loss_threshold=float(loss_threshold) if loss_threshold else None
    )
    print(f" Gambler {gambler_id} updated successfully.")

def reset_database_action():
    confirm = input("This will clear ALL data. Type 'YES' to confirm: ")
    if confirm.upper() == "YES":
        reset_database()
        print("Database reset complete.")
    else:
        print("Reset cancelled.")

def start_session():
    global current_session
    gambler_id = int(input("Enter gambler ID: "))
    upper_limit = float(input("Enter upper limit: "))
    lower_limit = float(input("Enter lower limit: "))
    min_bet = float(input("Enter minimum bet: "))
    max_bet = float(input("Enter maximum bet: "))
    max_games = int(input("Enter maximum number of games: "))
    max_duration = int(input("Enter maximum duration (minutes): "))

    params = SessionParameters(upper_limit, lower_limit, min_bet, max_bet, max_games, max_duration)
    current_session = GamingSession(gambler_id, params)
    current_session.start()

def play_game_in_session():
    global current_session
    if current_session and current_session.status == SessionStatus.ACTIVE:
        amount = float(input("Enter bet amount: "))
        probability = float(input("Enter win probability (0-1): "))
        current_stake = float(input("Enter current stake: "))
        outcome, new_stake = current_session.play_game(amount, probability, current_stake)
        print(f"Game Result → Outcome: {outcome} | New Stake: {new_stake}")
    else:
        print("No active session. Start one first.")

def pause_session():
    global current_session
    if current_session:
        current_session.pause()
    else:
        print("No session to pause.")

def resume_session():
    global current_session
    if current_session:
        current_session.resume()
    else:
        print("No session to resume.")

def end_session():
    global current_session
    if current_session:
        current_session.end()
    else:
        print("No session to end.")

def view_session_summary():
    global current_session
    if current_session:
        SessionSummary.display_session_summary("SessionPlayer", current_session.statistics, current_session.totals)
    else:
        print("No session summary available.")

def place_bet_with_strategy():
    gambler_id = int(input("Enter gambler ID: "))
    current_stake = float(input("Enter current stake: "))
    probability = float(input("Enter win probability (0-1): "))
    num_bets = int(input("Enter number of consecutive bets: "))

    print("\nChoose Strategy:")
    print("1. Fixed Amount")
    print("2. Percentage")
    print("3. Martingale")
    print("4. Reverse Martingale")
    print("5. Fibonacci")
    print("6. D'Alembert")

    strategy_choice = input("Enter strategy number: ")

    if strategy_choice == "1":
        amount = float(input("Enter fixed bet amount: "))
        strategy = FixedAmountStrategy(amount)
    elif strategy_choice == "2":
        percentage = float(input("Enter percentage (e.g. 0.05 for 5%): "))
        strategy = PercentageStrategy(percentage)
    elif strategy_choice == "3":
        base = float(input("Enter base bet amount: "))
        strategy = MartingaleStrategy(base)
    elif strategy_choice == "4":
        base = float(input("Enter base bet amount: "))
        strategy = ReverseMartingaleStrategy(base)
    elif strategy_choice == "5":
        base = float(input("Enter base bet amount: "))
        strategy = FibonacciStrategy(base)
    elif strategy_choice == "6":
        base = float(input("Enter base bet amount: "))
        strategy = DalembertStrategy(base)
    else:
        print("Invalid strategy choice")
        return

    strategy_name = strategy.__class__.__name__

    # Only call once: this saves transactions internally
    results = BettingService.place_consecutive_bets(gambler_id, strategy, probability, current_stake, num_bets)

    # Record results in the current session
    global current_session
    if current_session and current_session.status == SessionStatus.ACTIVE:
        stake = current_stake
        for i, (game_num, amount, outcome, stake) in enumerate(results, start=1):
            current_session.records.append(
                GameRecord(game_num, amount, outcome, stake-amount if outcome=="WIN" else stake+amount, stake, strategy_name)
            )

    print("\n Strategy Results:")
    for game in results:
        print(f"Game {game[0]} → Bet {game[1]} | Outcome: {game[2]} | Stake: {game[3]}")

def play_game_with_odds():
    gambler_id = int(input("Enter gambler ID: "))
    stake_before = float(input("Enter current stake: "))
    bet_amount = float(input("Enter bet amount: "))

    print("\nChoose Odds Type:")
    print("1. FIXED")
    print("2. PROBABILITY_BASED")
    print("3. AMERICAN")
    print("4. DECIMAL")
    odds_choice = int(input("Enter odds type number: "))

    if odds_choice == 1:
        odds_type = OddsType.FIXED
        odds_value = float(input("Enter fixed multiplier (e.g., 2 for 2x): "))
    elif odds_choice == 2:
        odds_type = OddsType.PROBABILITY_BASED
        odds_value = float(input("Enter win probability (0-1): "))
    elif odds_choice == 3:
        odds_type = OddsType.AMERICAN
        odds_value = float(input("Enter American odds (+200, -150, etc.): "))
    elif odds_choice == 4:
        odds_type = OddsType.DECIMAL
        odds_value = float(input("Enter decimal odds (e.g., 1.5, 2.0): "))
    else:
        print("Invalid odds type.")
        return

    print("\nChoose Outcome Strategy:")
    print("1. RandomOutcomeStrategy")
    print("2. WeightedProbabilityStrategy")
    strat_choice = int(input("Enter strategy number: "))

    if strat_choice == 1:
        strategy = RandomOutcomeStrategy()
    else:
        strategy = WeightedProbabilityStrategy()

    # Initialize stats and totals
    statistics = WinLossStatistics()
    totals = RunningTotals(stake_before)

    # Play game
    result = WinLossCalculator.play_game(
        gambler_id, bet_amount, stake_before,
        strategy, odds_type, odds_value,
        statistics, totals
    )

    print("\nGame Result:")
    print(result)
    print("\nStatistics Summary:")
    print(statistics.summary())
    print("\nRunning Totals:")
    print(totals.summary())

# ---------------------------
# Dispatch Dictionary
# ---------------------------
menu_actions = {
    "1": create_profile,
    "2": view_profiles,
    "3": place_bet,
    "4": view_stake_history,
    "5": reset_profile,
    "6": update_profile,
    "7": reset_database_action,
    "8": start_session,
    "9": play_game_in_session,
    "10": pause_session,
    "11": resume_session,
    "12": end_session,
    "13": view_session_summary,
    "14": place_bet_with_strategy,
    "15": play_game_with_odds,
    "16": None,  
    "17": None
}

# Configure validation rules
validation_config = ValidationConfig(
    min_stake=100, max_stake=100000,
    min_bet=1, max_bet=10000,
    min_prob=0.0, max_prob=1.0,
    strict_mode=True, allow_zero_stake=False
)

validator = InputValidator(validation_config)
safe_input = SafeInputHandler(validator)

# Main Loop

def main():
    while True:
        main_menu()
        choice = input("Enter choice: ")

        if choice == "16":
            print("Exiting Gambling App...")
            break
        elif choice == "17":
            engine = SimpleGameEngine("DemoPlayer", 1000)
            while True:
                engine.play_round()
                cont = input("Play another round? (y/n): ")
                if cont.lower() != "y":
                    engine.end_session()
                    break
        else:
            action = menu_actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
