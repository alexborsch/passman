import sqlite3


def create_new_db():
    conn = sqlite3.connect("data/database.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE passwords_db
                    (title text, data text)
                """)
    conn.commit()

