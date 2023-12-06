import pymysql


class DatabaseHandler:
    '''CLass-Handler BD'''


    def __init__(self, host, port, user, password=None):
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
        )

    def execute_query(self, sql, params=None):
        '''Metod query data from BD'''

        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def execute_insert(self, sql, params=None):
        '''Metod insert data in BD'''

        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
        self.connection.commit()

    def create_table(self, table_name: str):
        sql_query = f'CREATE TABLE IF NOT EXISTS legpromtest.{table_name}(\
                        inn VARCHAR(10),\
                        positive TEXT,\
                        negative TEXT\
                    );\
                    '
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query)
        self.connection.commit()


    def get_by_inn(self, inn: str):
        sql_query = f'SELECT inn, positive, negative ' \
                    f'FROM legpromtest.c_risks ' \
                    f'WHERE inn = {inn};'
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query)
            return ({
                'inn': item[0],
                'positive': item[1],
                'negative': item[2]
            } for item in cursor.fetchall())

    def get_all(self):
        sql_query = f'SELECT * ' \
                    f'FROM legpromtest.c_risks;'
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query)
            return ({
                'inn': item[0],
                'positive': item[1],
                'negative': item[2]
            } for item in cursor.fetchall())


    def close(self):
        '''Method close BD'''
        self.connection.close()



