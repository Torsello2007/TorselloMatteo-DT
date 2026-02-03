import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseWrapper:
    def __init__(self):
        self.db_config = {
            'host': os.getenv("DB_HOST"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'database': os.getenv("DB_NAME"),
            'port': int(os.getenv("DB_PORT")),
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.create_table()

    def connect(self):
        return pymysql.connect(**self.db_config)

    def execute_query(self, query, params=()):
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
        finally:
            conn.close()

    def fetch_query(self, query, params=()):
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS deliveries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tracking_code VARCHAR(100) NOT NULL UNIQUE,
            recipient VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            time_slot VARCHAR(100) NOT NULL,
            status ENUM('READY', 'OUT_FOR_DELIVERY', 'DELIVERED', 'FAILED') DEFAULT 'READY',
            priority ENUM('LOW', 'MEDIUM', 'HIGH') DEFAULT 'LOW'
        )
        '''
        self.execute_query(query)

    def get_all_deliveries(self):
        return self.fetch_query("SELECT * FROM deliveries")

    def add_delivery(self, tracking, recipient, address, time_slot, priority):
        query = "INSERT INTO deliveries (tracking_code, recipient, address, time_slot, priority) VALUES (%s, %s, %s, %s, %s)"
        params = (tracking, recipient, address, time_slot, priority)
        try:
            self.execute_query(query, params)
            return True
        except: return False

    # AGGIUNTA PER COMMIT 6
    def update_status(self, delivery_id, new_status):
        query = "UPDATE deliveries SET status = %s WHERE id = %s"
        try:
            self.execute_query(query, (new_status, delivery_id))
            return True
        except: return False


    def update_status(self, delivery_id, new_status):
        """Aggiorna lo stato di una consegna (Richiesto Commit 6)"""
        query = "UPDATE deliveries SET status = %s WHERE id = %s"
        try:
            self.execute_query(query, (new_status, delivery_id))
            return True
        except:
            return False