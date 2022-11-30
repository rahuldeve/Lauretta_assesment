import sqlite3

def create_db(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            exit()


def create_table(db_file):
    try:
        db_conn = sqlite3.connect(db_file)
        sql = """
        create table login (
            name text primary key,
            country_code text not null,
            passwd blob not null
        )
        """
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.close()
    except sqlite3.Error as e:
        return str(e)


def get_entry(db_file, user_name):
    try:
        db_conn = sqlite3.connect(db_file)
        curr = db_conn.execute('select * from login where name=?', (user_name, ))
        entry = curr.fetchall()
        db_conn.close()
        return entry
    except sqlite3.Error as e:
        return str(e)



