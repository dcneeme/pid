import sqlite3

class DatabaseManager():
    '''
    dbmgr = DatabaseManager("testdb.db")
    for row in dbmgr.query("select * from users")
    print row
    This will keep the connection open for the duration of the object's existence.
    '''

    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def __del__(self):
        self.conn.close()
        
    
      