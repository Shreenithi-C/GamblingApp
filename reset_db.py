from utils.db_connection import DBConnection

def reset_database():
    db = DBConnection()
    conn = db.connect()
    cursor = conn.cursor()

    # Clear dependent tables first (bets, transactions)
    cursor.execute("DELETE FROM bet WHERE 1=1")
    cursor.execute("ALTER TABLE bet AUTO_INCREMENT = 1")

    cursor.execute("DELETE FROM stake_transaction WHERE 1=1")
    cursor.execute("ALTER TABLE stake_transaction AUTO_INCREMENT = 1")

    # Clear gambler profiles last (since others depend on it)
    cursor.execute("DELETE FROM gambler_profile WHERE 1=1")
    cursor.execute("ALTER TABLE gambler_profile AUTO_INCREMENT = 1")

    # Clear sessions if needed
    cursor.execute("DELETE FROM gambling_session WHERE 1=1")
    cursor.execute("ALTER TABLE gambling_session AUTO_INCREMENT = 1")

    conn.commit()
    db.close()
    print("Database reset complete. All tables cleared and counters reset.")

if __name__ == "__main__":
    reset_database()
