import psycopg2
import time
import os


class Game:

    def __init__(self, row = [-1, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0, 0, time.time(), False]):
        self.fen = row[1]
        self.color = row[3]
        self.last_moved = row[4]
        self.warned = row[5]
        self.bot = row[2]

    def __str__(self):
        return self.fen


class Data:

    def __init__(self, url):
        self.DATABASE_URL = url

        self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')

        create_games_table = '''CREATE TABLE IF NOT EXISTS games (
										id bigint NOT NULL PRIMARY KEY UNIQUE,
										position text,
                                        bot integer,
										color integer,
										last_moved real,
										warned integer
									);'''
        create_ratings_table = '''CREATE TABLE IF NOT EXISTS ratings (
										id bigint NOT NULL PRIMARY KEY UNIQUE,
										rating real
									);'''
        create_prefix_table = '''CREATE TABLE IF NOT EXISTS prefixes (
										id bigint NOT NULL PRIMARY KEY UNIQUE,
										prefix text
									);'''
        create_themes_table = '''CREATE TABLE IF NOT EXISTS themes (
										id bigint NOT NULL PRIMARY KEY UNIQUE,
										theme text
									);'''
        create_votes_table = '''CREATE TABLE IF NOT EXISTS votes (
										id bigint NOT NULL PRIMARY KEY UNIQUE
									);'''
        create_stats_table = '''CREATE TABLE IF NOT EXISTS stats (
										id bigint NOT NULL PRIMARY KEY UNIQUE,
                                        lost int,
                                        won int,
                                        drew int
									);'''

        cur = self.get_conn().cursor()
        cur.execute(create_games_table)
        cur.execute(create_ratings_table)
        cur.execute(create_prefix_table)
        cur.execute(create_themes_table)
        cur.execute(create_votes_table)
        cur.execute(create_stats_table)

    def get_conn(self):
        if self.conn.closed:
            print('Connection is closed. Restarting...')
            self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        return self.conn

    def get_game(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM games WHERE id = {person};')
        rows = cur.fetchall()

        if len(rows) == 0:
            return None

        return Game(rows[0])

    def get_games(self):
        cur = self.get_conn().cursor()
        cur.execute('SELECT * FROM games')
        rows = cur.fetchall()

        games = {}

        for row in rows:
            moves_str = row[1].split(' ')
            moves = []
            for move in moves_str:
                try:
                    moves.append(int(move))
                except:
                    pass

            games[row[0]] = Game(row)

        return games

    def change_game(self, person, new_game: Game):
        cur = self.get_conn().cursor()

        update_sql = f'''INSERT INTO games VALUES ({person}, '{new_game.fen}', {new_game.bot}, {new_game.color}, {new_game.last_moved}, {int(new_game.warned)});'''

        cur.execute(f'DELETE FROM games WHERE id = {person};')
        cur.execute(update_sql)

        self.conn.commit()

    def get_rating(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM ratings WHERE id = {person};')
        rows = cur.fetchall()

        if len(rows) == 0:
            return None
        return rows[0][1]

    def get_ratings(self):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM ratings;')
        rows = cur.fetchall()

        ratings = {}
        for row in rows:
            ratings[row[0]] = row[1]

        return ratings

    def change_rating(self, person, new_rating):
        cur = self.get_conn().cursor()

        cur.execute(f'DELETE FROM ratings WHERE id = {person};')
        cur.execute(f'INSERT INTO ratings VALUES ({person}, {new_rating});')

        self.conn.commit()

    def get_prefix(self, guild):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM prefixes WHERE id = {guild};')
        rows = cur.fetchall()

        if len(rows) == 0:
            return '$'
        return rows[0][1]

    def change_prefix(self, guild, new_prefix):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM prefixes WHERE id = {guild};')
        cur.execute(
            f'INSERT INTO prefixes VALUES ({guild}, \'{new_prefix}\');')

        self.conn.commit()

    def get_stats(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM stats WHERE id = {person};')
        rows = cur.fetchall()
        if len(rows) == 0:
            return 0, 0, 0
        return rows[0][1], rows[0][2], rows[0][3]
    
    def change_stats(self, person, lost, won, drew):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM stats WHERE id = {person};')
        cur.execute(
            f'INSERT INTO stats VALUES ({person}, {lost}, {won}, {drew});')
        self.conn.commit()
        
    def total_games(self):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM stats;')
        rows = cur.fetchall()
        ans = 0
        for row in rows:
            ans += row[1] + row[2] + row[3]
        return ans

    def delete_game(self, person, won):
        cur = self.get_conn().cursor()
        game = self.get_game(person)
        num_lost, num_won, num_draw = self.get_stats(person)
        bot_lost, bot_won, bot_draw = self.get_stats(game.bot)
        if won is None:
            self.change_stats(person, num_lost, num_won, num_draw + 1)
            self.change_stats(game.bot, bot_lost, bot_won, bot_draw + 1)
        elif won == 1:
            self.change_stats(person, num_lost, num_won + 1, num_draw)
            self.change_stats(game.bot, bot_lost + 1, bot_won, bot_draw)
        elif won == 0:
            self.change_stats(person, num_lost + 1, num_won, num_draw)
            self.change_stats(game.bot, bot_lost, bot_won + 1, bot_draw)
        cur.execute(f'DELETE FROM games WHERE id = {person};')
        self.conn.commit()

    def get_theme(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM themes WHERE id = {person};')
        rows = cur.fetchall()

        if len(rows) == 0:
            return 'default'
        return rows[0][1]

    def change_theme(self, person, new_theme):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM themes WHERE id = {person};')
        cur.execute(f'INSERT INTO themes VALUES ({person}, \'{new_theme}\');')

        self.conn.commit()

    def has_claimed(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM votes WHERE id = {person}')
        rows = cur.fetchall()

        return len(rows) == 1

    def get_claimed(self):
        cur = self.get_conn().cursor()
        cur.execute(f'SELECT * FROM votes')
        rows = cur.fetchall()
        return rows

    def add_vote(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM votes WHERE id = {person}')
        cur.execute(f'INSERT INTO votes VALUES ({person})')
        self.conn.commit()

    def remove_vote(self, person):
        cur = self.get_conn().cursor()
        cur.execute(f'DELETE FROM votes WHERE id = {person}')
        self.conn.commit()


data_manager = Data(os.environ['DATABASE_URL'])
