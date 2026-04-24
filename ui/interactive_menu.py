class InteractiveMenu:
    @staticmethod
    def display_main_menu():
        print("\n=== Gambling App ===")
        print("1. Create Gambler Profile")
        print("2. View All Profiles")
        print("3. Place a Bet")
        print("4. View Stake History Report")
        print("5. Reset Gambler Profile")
        print("6. Update Gambler Profile")
        print("7. Reset Entire Database")
        print("8. Start New Session")
        print("9. Play Game in Session")
        print("10. Pause Session")
        print("11. Resume Session")
        print("12. End Session")
        print("13. View Session Summary")
        print("14. Place Bet with Strategy")
        print("15. Play Game with Odds") 
        print("16. Exit") 
        print("17. Demo Game (UC7)")     

    @staticmethod
    def prompt_for_bet_amount():
        try:
            return float(input("Enter bet amount: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return InteractiveMenu.prompt_for_bet_amount()
