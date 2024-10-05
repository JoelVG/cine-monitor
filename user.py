from sqlite3 import connect
from datetime import datetime
from models.user import User


class UserCRUD:
    def __init__(self, db_name="users.db"):
        self.conn = connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                chat_id TEXT PRIMARY KEY,
                is_active INTEGER,
                created_at TEXT,
                updated_at TEXT
            )
        """
        )
        self.conn.commit()

    def create_user(self, user: User):
        self.cursor.execute(
            """
            INSERT INTO users (username, chat_id, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """,
            (user.username, user.chat_id, int(True), user.created_at, user.updated_at),
        )
        self.conn.commit()

    def read_user(self, chat_id: str):
        self.cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
        user_data = self.cursor.fetchone()
        if user_data:
            return User(
                username=user_data[0],
                chat_id=user_data[1],
                is_active=bool(user_data[2]),
                created_at=user_data[3],
                updated_at=user_data[4],
            )
        return None

    def modify_user(self, chat_id: str, is_active: bool):
        """
        Modify is_active and updated_at fields of a user
        """
        self.cursor.execute(
            """
            UPDATE users
            SET is_active = ?, updated_at = ?
            WHERE chat_id = ?
        """,
            (int(is_active), str(datetime.now()), chat_id),
        )
        self.conn.commit()

    def delete_user(self, chat_id: str):
        self.cursor.execute("DELETE FROM users WHERE chat_id = ?", (chat_id,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
