import mysql.connector
from dotenv import load_dotenv
import os

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

    def insert_session_data(self,u_id,session_id,time_stamp, stream_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO ChatDB.Session_Data (u_id,session_id,time_stamp, stream_id) 
            VALUES (%s,%s,%s,%s)''',(u_id,session_id,time_stamp, stream_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_latest_session_id(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT session_id FROM ChatDB.Session_Data WHERE 
            time_stamp=(SELECT MAX(time_stamp) FROM ChatDB.Session_Data)''')
        last_session_id = cursor.fetchone()[0]
        conn.close()
        return last_session_id

    def insert_chat_data(self,u_id,session_id,user_input,bot_response):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO ChatDB.Chat_Data (u_id,session_id,user_input,bot_response) 
            VALUES (%s, %s, %s,%s)''',(u_id,session_id,user_input,bot_response)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_active_users(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT u_id FROM ChatDB.Active_Users WHERE is_active=1''')
        active_user_ids = [row[0] for row in cursor.fetchall()]
        conn.commit()
        cursor.close()
        conn.close()
        return active_user_ids

    def reset_active_user(self,u_id):
        conn = self._connect()
        cursor = conn.cursor()
        # cursor.execute('''UPDATE ChatDB.Active_Users SET is_active=0 WHERE u_id=u_id''')
        cursor.execute('''UPDATE ChatDB.Active_Users SET is_active=0 WHERE u_id=%s''', (u_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def set_active_user(self,u_id):
        conn = self._connect()
        cursor = conn.cursor()
        # cursor.execute('''UPDATE ChatDB.Active_Users SET is_active=1 WHERE u_id=u_id''')
        cursor.execute('''UPDATE ChatDB.Active_Users SET is_active=1 WHERE u_id=%s''', (u_id,))
        conn.commit()
        cursor.close()
        conn.close()

