# -*- coding: utf-8 -*-
import sqlite3


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()

    # current_open
    def create_lot(self, id, name, enchanted, seller, cost, buyer, time, base):
        with self.connection:
            self.cursor.execute('INSERT INTO actives (id, name, enchanted, seller, cost, buyer, time, base) '
                                'VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (id, name, enchanted, seller, cost, buyer, time, base,))

    def create_users(self, id, username, marker, lotid, updates1, updates2, lotdel):
        with self.connection:
            self.cursor.execute('INSERT INTO users (id, username, marker, lotid, updates1, updates2, lotdel) '
                                'VALUES (?, ?, ?, ?, ?, ?, ?)', (id, username, marker, lotid, updates1, updates2, lotdel,))

    def update_users(self, id, usernick, fullscore, score, lasttime, updates):
        with self.connection:
            self.cursor.execute('UPDATE users SET usernick=?, fullscore=?, score=?, lasttime=?, updates=? WHERE id = ?',
                                (usernick, fullscore, score, lasttime, updates, id,))

    def update_content(self, id, content):
        with self.connection:
            self.cursor.execute('UPDATE users SET content=? WHERE id = ?', (content, id,))

    def page_update(self, id, text):
        with self.connection:
            self.cursor.execute('UPDATE pages SET text=? WHERE id = ?', (text, id,))

    def update_lot(self, id, cost, buyer, time):
        with self.connection:
            self.cursor.execute('UPDATE actives SET cost=?, buyer=?, time=? WHERE id = ?', (cost, buyer, time, id,))

    def delete_lot(self, id):
        with self.connection:
            self.cursor.execute('DELETE FROM actives WHERE id = ?', (id,))

    def get_lot(self, id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM actives WHERE id = ?', (id,)).fetchall()
        if result:
            return result[0]
        else:
            return False

    def get_item(self, base):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM actives WHERE base = ? ORDER BY time', (base,)).fetchall()
        if result:
            return result
        else:
            return False

    def get_base(self,):
        with self.connection:
            result = self.cursor.execute('SELECT base FROM actives ORDER BY base').fetchall()
        if result:
            return result
        else:
            return False

    def get_userid(self, id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchall()
        if result:
            return result[0]
        else:
            return False

    def get_page(self, id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM pages WHERE id = ?', (id,)).fetchall()
        if result:
            return result[0]
        else:
            return False

    def get_allpages(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM pages', ()).fetchall()
        if result:
            return result
        else:
            return False

    def get_alluserid(self,):
        with self.connection:
            result = self.cursor.execute('SELECT id FROM users').fetchall()
        if result:
            return result
        else:
            return False

    def get_id(self,):
        with self.connection:
            result = self.cursor.execute('SELECT id FROM actives').fetchall()
        if result:
            return result
        else:
            return False

    def get_updates1(self,):
        with self.connection:
            result = self.cursor.execute('SELECT updates1 FROM users').fetchall()
        if result:
            return result
        else:
            return False

    def get_updates2(self,):
        with self.connection:
            result = self.cursor.execute('SELECT updates2 FROM users').fetchall()
        if result:
            return result
        else:
            return False

    def get_lotdel(self,):
        with self.connection:
            result = self.cursor.execute('SELECT lotdel FROM users').fetchall()
        if result:
            return result
        else:
            return False

    def get_ticket_id(self,):
        with self.connection:
            result = self.cursor.execute('SELECT ticket_id FROM tickets').fetchall()
        if result:
            return result
        else:
            return False

    def get_rowtickets(self, ticket_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM tickets WHERE ticket_id = ?', (ticket_id,)).fetchall()
        if result:
            return result
        else:
            return False

    def create_zerogame(self, number, postid, gambling):
        with self.connection:
            self.cursor.execute('INSERT INTO zerogame (number, postid, gambling) VALUES (?, ?, ?)',
                                (number, postid, gambling,))

    def update_updates1(self, id, updates1):
        with self.connection:
            self.cursor.execute('UPDATE users SET updates1=? WHERE id = ?', (updates1, id,))

    def update_updates2(self, id, updates2):
        with self.connection:
            self.cursor.execute('UPDATE users SET updates2=? WHERE id = ?', (updates2, id,))

    def update_lotdel(self, id, lotdel):
        with self.connection:
            self.cursor.execute('UPDATE users SET lotdel=? WHERE id = ?', (lotdel, id,))

    def update_lotid(self, id, lotid):
        with self.connection:
            self.cursor.execute('UPDATE users SET lotid=? WHERE id = ?', (lotid, id,))

    def update_castle(self, castle, gold, box, point, atk, atk_high, atk_low, deff, def_high, def_low, def_ger, sleep):
        with self.connection:
            self.cursor.execute(
                'UPDATE main SET gold=?, box=?, point=?, atk=?, atk_high=?, atk_low=?, deff=?, '
                'def_high=?, def_low=?, def_ger=?, sleep=? WHERE castle = ?',
                (gold, box, point, atk, atk_high, atk_low, deff, def_high, def_low, def_ger, sleep, castle,))

    def get_castle(self, castle):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM main WHERE castle = ?', (castle,)).fetchall()
        if result:
            return result[0]
        else:
            return False

    def get_paper(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM main ORDER BY gold', ()).fetchall()
        if result:
            return result
        else:
            return False

    def update_gambling(self, gambling):
        with self.connection:
            self.cursor.execute('UPDATE zerogame SET gambling=? WHERE zero = 0', (gambling,))

    def get_zerogame(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM zerogame WHERE zero = 0').fetchall()
        if result:
            return result[0]
        else:
            return False