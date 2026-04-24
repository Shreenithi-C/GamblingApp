from utils.db_connection import DBConnection

class GamblerProfile:
    def __init__(self, name, initial_stake, win_threshold, loss_threshold):
        self.name = name
        self.initial_stake = initial_stake
        self.current_stake = initial_stake
        self.win_threshold = win_threshold
        self.loss_threshold = loss_threshold
        self.statistics = {"wins": 0, "losses": 0, "total_bets": 0}

    def save_to_db(self):
        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()

        query = """
        INSERT INTO gambler_profile(name, initial_stake, current_stake, win_threshold, loss_threshold, wins, losses, total_bets)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (self.name, self.initial_stake, self.current_stake,
                  self.win_threshold, self.loss_threshold,
                  self.statistics["wins"], self.statistics["losses"], self.statistics["total_bets"])

        cursor.execute(query, values)
        conn.commit()
        print(f"Gambler {self.name} saved successfully")
        db.close()

    @staticmethod
    def get_all():
        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT gambler_id, name, current_stake, wins, losses, total_bets FROM gambler_profile")
        results = cursor.fetchall()
        db.close()
        return results

    @staticmethod
    def validate_eligibility(initial_stake, min_required=100):
        return initial_stake >= min_required

    @staticmethod
    def reset_profile(gambler_id):
        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()
        query = """
        UPDATE gambler_profile
        SET current_stake = initial_stake, wins=0, losses=0, total_bets=0
        WHERE gambler_id=%s
        """
        cursor.execute(query, (gambler_id,))
        conn.commit()
        print(f"Gambler profile {gambler_id} reset successfully")
        db.close()

    @staticmethod
    def update_profile(gambler_id, name=None, win_threshold=None, loss_threshold=None):
        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()

        updates = []
        values = []

        if name is not None:
            updates.append("name = %s")
            values.append(name)
        if win_threshold is not None:
            updates.append("win_threshold = %s")
            values.append(win_threshold)
        if loss_threshold is not None:
            updates.append("loss_threshold = %s")
            values.append(loss_threshold)

        if not updates:
            print("No updates provided.")
            return

        query = f"UPDATE gambler_profile SET {', '.join(updates)} WHERE gambler_id = %s"
        values.append(gambler_id)

        cursor.execute(query, tuple(values))
        conn.commit()
        db.close()

        print(f"Gambler {gambler_id} updated successfully.")

class BettingPreferences:
    def __init__(self, min_bet=100, max_bet=1000, preferred_game="Default", auto_play=False, session_limit=60):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.preferred_game = preferred_game
        self.auto_play = auto_play
        self.session_limit = session_limit  # minutes

    def update_preferences(self, min_bet=None, max_bet=None, preferred_game=None, auto_play=None, session_limit=None):
        if min_bet is not None: self.min_bet = min_bet
        if max_bet is not None: self.max_bet = max_bet
        if preferred_game is not None: self.preferred_game = preferred_game
        if auto_play is not None: self.auto_play = auto_play
        if session_limit is not None: self.session_limit = session_limit
