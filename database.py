import sqlite3


class IdsDatabase():
    def __init__(self):
        self._con = sqlite3.connect("./data/exist_ids.db")
        self._cur = self._con.cursor()
        self._create_ids_table()

    def _create_ids_table(self) -> None:
        self._cur.execute("""
        CREATE TABLE IF NOT EXISTS uniq_ids (
        uniq_id INTEGER)
        """)

    def insert_new_id(self, id_:int) -> None:
        self._cur.execute("INSERT INTO uniq_ids VALUES (?)", (id_,))

    def get_ids(self) -> list:
        res = self._cur.execute("SELECT uniq_id FROM uniq_ids").fetchall()
        ids = [ d[0] for d in res]
        return ids

    def close(self) -> None:
        self._con.commit()
        self._con.close()


def main() -> None:
#    db = IdsDatabase()
#    db.insert_new_id(12)
#    print('Insert data')
#    db.close()

    db = IdsDatabase()
    ids = db.get_ids()
    print('Get data - ', ids[0][0])
    db.close()


if __name__ == '__main__':
    main()

