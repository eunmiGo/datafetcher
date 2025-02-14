import os
from datetime import datetime
from config.config import Config


import psycopg2


class LoadMetaData:
    def __init__(self, file_path, file_size):
        self.file_path = file_path
        self.file_size = file_size

    def load_meta_data(self):
        file_path = self.file_path
        file_size = self.file_size

        conn = psycopg2.connect(
            host=Config.postgres_server.host,
            database=Config.postgres_server.database,
            user=Config.postgres_server.user,
            password=Config.postgres_server.password,
            port=Config.postgres_server.port
        )

        cur = conn.cursor()

        if isinstance(file_path, list) & isinstance(file_size, list):
            for path, size in zip(file_path, file_size):
                file_name = os.path.basename(path)
                try:
                    insert_query = """
                        INSERT INTO file_metadata (file_name, upload_time, file_size, file_path)
                        VALUES (%s, %s, %s, %s)
                    """
                    cur.execute(insert_query, (file_name, datetime.now(), size, path))
                    conn.commit()
                except psycopg2.Error as db_error:
                    print(f"PostgreSQL 저장 중 오류 발생: {db_error}")
                    conn.rollback()
        else:
            file_name = os.path.basename(file_path)
            try:
                insert_query = """
                        INSERT INTO file_metadata (file_name, upload_time, file_size, file_path)
                        VALUES (%s, %s, %s, %s)
                    """
                cur.execute(insert_query, (file_name, datetime.now(), file_size, file_path))
                conn.commit()

            except psycopg2.Error as db_error:
                print(f"PostgreSQL 저장 중 오류 발생: {db_error}")
                conn.rollback()
            finally:
                conn.close()
        return "메타데이터가 PostgreSQL에 저장되었습니다."
