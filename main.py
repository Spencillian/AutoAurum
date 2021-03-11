from InvestopediaApi import ita
from googlefinance import getQuotes
from tinydb import TinyDB, Query
import requests
import helper
from apscheduler.schedulers.blocking import BlockingScheduler


db = None
cursor = None
sched = BlockingScheduler()


@helper.timer
def get_data():
    response = requests.get("https://api.swaggystocks.com/wsb/sentiment/top")
    return response.json(), response.status_code


def get_db():
    global db
    if db is None:
        db = TinyDB('db.json')
    return db


def query():
    global cursor
    if cursor is None:
        cursor = Query()
    return cursor


def update_db(req):
    for i, value in enumerate(req):
        try:
            arr = get_db().search(query().ticker == value)[0]["arr"]
        except IndexError:
            arr = []

        arr.append((i, value["count_ticker"]))
        get_db().upsert({"ticker": value["ticker"], "arr": arr}, query().name == value['ticker'])


sched.add_job(update_db, "cron", [get_data()[0]], day_of_week='mon-fri', hour=20)


if __name__ == "__main__":
    sched.start()
