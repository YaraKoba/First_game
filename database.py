import sqlite3


class DataBaseClient:
    def __init__(self, filename):
        self.filename = filename
        self.conn = None

    def setup(self):
        self.conn = sqlite3.connect(self.filename, check_same_thread=False)

    def execute_command(self, command, params=()):
        if self.conn is not None:
            self.conn.execute(command, params)
            self.conn.commit()
        else:
            raise ConnectionError('You need create connection object!!!')

    def execute_select_command(self, command):
        if self.conn is not None:
            curs = self.conn.cursor()
            curs.execute(command)
            return curs.fetchall()
        else:
            raise ConnectionError('You need create connection object!!!')


class PlayerRecord:
    INSERT_EASY = ("""
        INSERT INTO easy_players (name, total_res, date) VALUES (?, ?, ?)
    """)

    INSERT_REAL = ("""
        INSERT INTO real_players (name, total_res, date) VALUES (?, ?, ?)
    """)

    def __init__(self, database: DataBaseClient):
        self.db = database

    def setup(self):
        self.db.setup()

    def save_result(self, params, mod):
        sql_get_name = f"SELECT total_res FROM {mod}_players WHERE name = '{params[0]}'"
        sql_update = f"UPDATE {mod}_players SET total_res = {params[1]} WHERE name = '{params[0]}'"
        try:
            if mod == 'easy':
                self.db.execute_command(PlayerRecord.INSERT_EASY, params)
            else:
                self.db.execute_command(PlayerRecord.INSERT_REAL, params)
        except sqlite3.IntegrityError:
            print(self.db.execute_select_command(sql_get_name)[0][0])
            if params[1] > self.db.execute_select_command(sql_get_name)[0][0]:
                self.db.execute_command(sql_update)

    def get_players(self, mod):
        sql = f"SELECT * FROM {mod}_players ORDER BY total_res DESC"
        return self.db.execute_select_command(sql)

    def dell_players(self):
        easy_players = self.get_players('easy')
        real_players = self.get_players('real')
        if len(easy_players) > 10:
            self.db.execute_command("DELETE FROM easy_players WHERE total_res < ?", (easy_players[9][1], ))
        if len(real_players) > 10:
            self.db.execute_command("DELETE FROM real_players WHERE total_res < ?", (real_players[9][1], ))

    def create_tabel(self):
        self.db.execute_command("""CREATE TABLE IF NOT EXISTS easy_players (
                                    name text UNIQUE,
                                    total_res INTEGER,
                                    date text
                                )""")
        self.db.execute_command("""CREATE TABLE IF NOT EXISTS real_players (
                                    name text UNIQUE,
                                    total_res INTEGER,
                                    date text
                                )""")
