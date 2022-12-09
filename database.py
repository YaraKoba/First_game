import sqlite3


class DataBaseClient:
    def __init__(self, filename):
        self.filename = filename
        self.conn = None

    def setup(self):
        self.conn = sqlite3.connect(self.filename, check_same_thread=False)

    def execute_command(self, command, params):
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

    SELECT_EASY = ("""
        SELECT * FROM easy_players ORDER BY total_res DESC
    """)

    INSERT_REAL = ("""
        INSERT INTO real_players (name, total_res, date) VALUES (?, ?, ?)
    """)

    SELECT_REAL = ("""
            SELECT * FROM real_players ORDER BY total_res DESC
        """)

    def __init__(self, database: DataBaseClient):
        self.db = database

    def setup(self):
        self.db.setup()

    def save_result(self, params, mod):
        sql_easy = f"UPDATE easy_players SET total_res = ? WHERE name = ?"
        sql_real = f"UPDATE real_players SET total_res = ? WHERE name = ?"
        if mod == 'easy':
            try:
                self.db.execute_command(PlayerRecord.INSERT_EASY, params)
            except sqlite3.IntegrityError:
                self.db.execute_command(sql_easy, (params[1], params[0]))
        else:
            try:
                self.db.execute_command(PlayerRecord.INSERT_REAL, params)
            except sqlite3.IntegrityError:
                self.db.execute_command(sql_real, (params[1], params[0]))

    def get_players(self, mod):
        if mod == 'easy':
            return self.db.execute_select_command(PlayerRecord.SELECT_EASY)
        else:
            return self.db.execute_select_command(PlayerRecord.SELECT_REAL)

    def dell_players(self):
        easy_players = self.get_players('easy')
        real_players = self.get_players('real')
        if len(easy_players) > 10:
            self.db.execute_command("DELETE FROM easy_players WHERE total_res < ?", (easy_players[9][2]))
        if len(real_players) > 10:
            self.db.execute_command("DELETE FROM real_players WHERE total_res < ?", (real_players[9][2]))