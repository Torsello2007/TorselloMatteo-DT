import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseWrapper:
    def __init__(self):
        # Recupero credenziali dal file .env (Requisito Commit 2)
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = int(os.getenv("DB_PORT"))
        self.database = os.getenv("DB_NAME")

    def get_connection(self):
        """Metodo di connessione"""
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def create_tables(self):
        """Crea le tabelle con SQL manuale (Vincolo: NO ORM)"""
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                # Query SQL scritta a mano come richiesto
                sql = """
                CREATE TABLE IF NOT EXISTS deliveries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tracking_code VARCHAR(50) NOT NULL UNIQUE,
                    recipient VARCHAR(100) NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    time_slot VARCHAR(50) NOT NULL,
                    status ENUM('READY', 'OUT_FOR_DELIVERY', 'DELIVERED', 'FAILED') DEFAULT 'READY',
                    priority ENUM('LOW', 'MEDIUM', 'HIGH') DEFAULT 'LOW'
                )
                """
                cursor.execute(sql)
            connection.commit()
            print("Tabella verificata correttamente.")
        except Exception as e:
            print(f"Errore: {e}")
        finally:
            connection.close()