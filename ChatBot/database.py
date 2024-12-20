import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database Manager Class
class DatabaseManager:
    def __init__(self):
        self.db_config = {
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'host': os.environ.get('DB_HOST'),
            'database': os.environ.get('DB_NAME')
        }

    def _connect(self):
        return mysql.connector.connect(**self.db_config)

    def insert_chat_history(self, start_time, is_stream):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO ChatDB.Chat_history (start_time, is_stream) VALUES (%s, %s)''',
            (start_time, is_stream)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_latest_chat_id(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT chat_id FROM ChatDB.Chat_history 
            WHERE chat_id = (SELECT MAX(chat_id) FROM ChatDB.Chat_history)
        ''')
        chat_id = cursor.fetchone()[0]
        conn.close()
        return chat_id

    def insert_chat_data(self, chat_id, user, assistant):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO ChatDB.Chat_data (chat_id, user, assistant) VALUES (%s, %s, %s)''',
            (chat_id, user, assistant)
        )
        conn.commit()
        cursor.close()
        conn.close()
