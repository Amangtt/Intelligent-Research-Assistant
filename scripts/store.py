import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os,sys


class database:

    def __init__(self,df,env,logger):
        self.df=df
        self.logger=logger 
        self.env=env
    def connect_store(self):
        try:
            # Load environment variables
            load_dotenv(self.env)

            DB_HOST = os.getenv("DB_HOST")
            DB_NAME = os.getenv("DB_NAME")
            DB_USER = os.getenv("DB_USER")
            DB_PASSWORD = os.getenv("DB_PASSWORD")
            DB_PORT = os.getenv("DB_PORT")
            self.logger.info('✅ Fetched the values successfully')

            # Connect to PostgreSQL
            conn = psycopg2.connect(
                dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
            )
            cur = conn.cursor()
            self.logger.info("✅ Successfully connected to the PostgreSQL database.")
            # Create table
            cur.execute("""
            CREATE TABLE IF NOT EXISTS medical_docs (
                id SERIAL PRIMARY KEY,
                filename TEXT,
                content TEXT
            );
            """)

            # Insert cleaned text
            for _, row in self.df.iterrows():
                cur.execute("INSERT INTO medical_docs (filename, content) VALUES (%s, %s)", (row["filename"], row["cleaned_content"]))

            conn.commit()
            cur.close()
            conn.close()
            print("✅ Data stored in PostgreSQL")
            self.logger.info('✅ Data stored in PostgreSQL')
        except Exception as e:
            error_message = f"Failed to store in PostgreSQL: {e}"
            self.logger.error(error_message)