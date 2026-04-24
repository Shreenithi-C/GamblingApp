class SessionSummary:
    @staticmethod
    def display_session_summary(gambler_name, statistics, totals):
        print("\nSession Summary")
        print(f"Gambler: {gambler_name}")
        print("Statistics:", statistics.summary())
        print("Running Totals:", totals.summary())
