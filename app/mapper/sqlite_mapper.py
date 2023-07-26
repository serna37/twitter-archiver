import datetime
import sqlite3
import pandas
from scraping import get_category as scraping

db = f'bookmarks.db'
create_table = f'CREATE TABLE IF NOT EXISTS bookmarks (tweetid, category, created_at, updated_at);'
create_index = f'CREATE INDEX IF NOT EXISTS idx_bookmarks_01 ON bookmarks(tweetid);'

select_1 = f'SELECT * FROM bookmarks LIMIT 1;'
select_all = f'SELECT * FROM bookmarks;'
select_uncategorised = f'SELECT * FROM bookmarks WHERE category IS NULL;'
select_ = f"""
SELECT
    rowid,
    tweetid,
    category
FROM
    bookmarks
ORDER BY
    RANDOM()
LIMIT
"""


def create():
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(create_table)
    cur.execute(create_index)
    con.close()


def delins(data):
    if not isinstance(data, list) or not data:
        return
    con = sqlite3.connect(db)
    # bulk insert
    now = datetime.datetime.now()
    arr_2d = [[v, None, now, now] for v in data]
    df = pandas.read_sql_query(sql=select_1, con=con)
    df_ins = pandas.DataFrame(data=arr_2d, columns=df.columns)
    df_ins.to_sql(name='bookmarks', con=con, if_exists='replace', index=False)
    con.close()


def update():
    con = sqlite3.connect(db)
    df = pandas.read_sql_query(sql=select_uncategorised, con=con)
    print(df)
    # TODO
    scraping.get_category("")
    con.close()


def select(num=10):
    if num > 31:
        num = 30
    con = sqlite3.connect(db)
    df = pandas.read_sql_query(sql=select_ + str(num), con=con)
    con.close()
    return df.to_json(orient='records')


def selectall():
    con = sqlite3.connect(db)
    df = pandas.read_sql_query(sql=select_all, con=con)
    con.close()
    return df.to_json(orient='records')
