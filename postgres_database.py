"""Handles all work on posgres database"""

import psycopg2
import psycopg2.extras


class PostgreSQL():

    def __init__(self, **kwargs):

        login = kwargs.get('login')
        password = kwargs.get('password')
        host = kwargs.get('host')
        base = kwargs.get('base')
        port = kwargs.get('port')

        self.conn = psycopg2.connect(user=login,
                                     dbname = base,
                                     password=password,
                                     port=port,
                                     host=host)

        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def create_tables(self):
        """Creates tables for holding data if they do not exist already"""

        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS airtables_therapists
                                   (id text, name text, methods text, photo text,
                                   UNIQUE(id));""")

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS airtables_dumps
                                   (ID  SERIAL PRIMARY KEY, date text,  loaded_data json, 
                                   UNIQUE(ID));""")
            self.conn.commit()

        except:
            self.cursor.execute("ROLLBACK")
            self.conn.commit()
            print('Error creating tables. Please checkup database credentials, host and password.')

    def insert(self, **kwargs):
        """Inserts values to table"""

        assert "table" in kwargs
        assert "columns" in kwargs
        assert "values" in kwargs

        table = kwargs.get('table')
        columns = kwargs.get('columns')
        values = kwargs.get('values')

        in_values = []
        for i in values:
            i = [f"'{j}'" if type(j) == str else str(j) for j in i]
            in_values.append((f'({", ".join(i)})'))

        update = []

        for i in columns[1:]:
            update.append(f'{i}=excluded.{i}')

        try:
            self.cursor.execute(f'''INSERT INTO {table} ({', '.join(columns)}) 
                                    VALUES {', '.join(in_values)}
                                    ON CONFLICT (id) DO UPDATE 
                                    SET {', '.join(update)};''')
            self.conn.commit()

        except:
            self.cursor.execute("ROLLBACK")
            self.conn.commit()
            print('Error in insert')
            print(f'''INSERT INTO {table} ({', '.join(columns)}) 
                      VALUES {', '.join(in_values)}
                      ON CONFLICT (id) DO UPDATE 
                      SET {', '.join(update)};''')

    def get_data(self, table):

        self.cursor.execute(f'select * from {table};')
        data = self.cursor.fetchall()
        return data

    def delete(self, **kwargs):

        assert "table" in kwargs
        assert "ids" in kwargs

        table = kwargs.get('table')
        ids = kwargs.get('ids')

        try:

            self.cursor.execute(
                f"""DELETE FROM {table}
                   WHERE  id NOT in ({','.join(str(i) for i in ids)});""")

            self.conn.commit()

        except:
            self.cursor.execute("ROLLBACK")
            self.conn.commit()
            print('Error in deleting data')
            print(f'''DELETE FROM {table} 
                      WHERE  id NOT in ({','.join(str(i) for i in ids)});''')

    def get_therapist_by_id(self, id):

        self.cursor.execute(
            f"""select * from airtables_therapists
               WHERE  id='{id}'""")

        return self.cursor.fetchone()
