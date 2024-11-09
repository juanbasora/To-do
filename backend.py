import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("to_do.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS to_do (id INTEGER PRIMARY KEY, due_date date, title text, priority text, description text, completed text)")
        self.conn.commit()

    def add_entry(self, due_date, title, description, priority, completed):
        self.cur.execute("INSERT INTO to_do VALUES (NULL, ?, ?, ?, ?, ?)", (due_date, title, description, priority, completed))
        self.conn.commit()

    def view_all(self):
        self.cur.execute("SELECT * FROM to_do")
        return self.cur.fetchall()

    # def last_edit(self):
    #     self.cur.execute("SELECT * FROM to_do WHERE id=(SELECT max(id) FROM to_do)")
    #     return self.cur.fetchone()

    # def search_date(self, due_date):
    #     self.cur.execute("SELECT * FROM to_do WHERE day=?", (due_date,))
    #     return self.cur.fetchall()

    def search_task(self, title, description):
        self.cur.execute("SELECT * FROM to_do WHERE title=? and description=?", (title, description))
        return self.cur.fetchall()

    def delete(self, id):
        self.cur.execute("DELETE FROM to_do WHERE id=?", (id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


# conn = sqlite3.connect("to_do.db")
# cur = conn.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS to_do (id INTEGER PRIMARY KEY, due_date date, title text, description text, completed text)")
# conn.commit()


# cur.execute("INSERT INTO to_do VALUES (NULL, ?, ?, ?, ?)", ("3/4/2024", "play games", "Play some zomboid with friends and make a ton of progress", "no"))
# cur.execute("INSERT INTO to_do VALUES (NULL, ?, ?, ?, ?)", ("4/1/2024", "work on this app", "Doing work on this app so I can complete it", "no"))
# conn.commit()

# cur.execute("SELECT * FROM to_do")
# print(cur.fetchall())