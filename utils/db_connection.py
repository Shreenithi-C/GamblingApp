import mysql.connector
from mysql.connector import Error
from settings import Settings

class DBConnection:
    def __init__(self):
        self.settings = Settings()
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.settings.DB_HOST,
                user=self.settings.DB_USER,
                password=self.settings.DB_PASSWORD
            )
            if self.connection.is_connected():
                self._create_database()
                self._create_tables()
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def _create_database(self):
        cursor = self.connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.settings.DB_NAME}")
        cursor.execute(f"USE {self.settings.DB_NAME}")

    def _create_tables(self):
        cursor = self.connection.cursor()

        # Gambler Profile
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS gambler_profile (
            gambler_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            initial_stake DECIMAL(10,2),
            current_stake DECIMAL(10,2),
            win_threshold DECIMAL(10,2),
            loss_threshold DECIMAL(10,2),
            wins INT DEFAULT 0,
            losses INT DEFAULT 0,
            total_bets INT DEFAULT 0
        )
        """)

        # Stake Transactions (drop & recreate to ensure schema sync)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stake_transaction (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            gambler_id INT,
            amount DECIMAL(10,2),
            transaction_type VARCHAR(50),
            strategy VARCHAR(100),
            balance_after DECIMAL(10,2),
            bet_id INT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (gambler_id) REFERENCES gambler_profile(gambler_id)
        )
        """)

        # Bets
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bet (
            bet_id INT AUTO_INCREMENT PRIMARY KEY,
            gambler_id INT,
            amount DECIMAL(10,2),
            probability FLOAT,
            outcome VARCHAR(10),
            FOREIGN KEY (gambler_id) REFERENCES gambler_profile(gambler_id)
        )
        """)

        # Sessions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS gambling_session (
            session_id INT AUTO_INCREMENT PRIMARY KEY,
            gambler_id INT,
            start_time DATETIME,
            end_time DATETIME,
            status VARCHAR(20),
            total_games INT DEFAULT 0,
            wins INT DEFAULT 0,
            losses INT DEFAULT 0,
            FOREIGN KEY (gambler_id) REFERENCES gambler_profile(gambler_id)
        )
        """)

        # game result
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_result (
            game_id INT AUTO_INCREMENT PRIMARY KEY,
            gambler_id INT,
            bet_amount DECIMAL(10,2),
            odds_type VARCHAR(20),
            odds_value DECIMAL(10,2),
            outcome VARCHAR(10),
            winnings DECIMAL(10,2),
            stake_before DECIMAL(10,2),
            stake_after DECIMAL(10,2),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (gambler_id) REFERENCES gambler_profile(gambler_id)
        )
        """)


    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
