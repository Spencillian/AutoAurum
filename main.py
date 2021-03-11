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
    return response.json()


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
            rank = get_db().search(query().ticker == value["ticker"])[0]["rank"]
            mentions = get_db().search(query().ticker == value["ticker"])[0]["mentions"]
        except IndexError:
            rank = []
            mentions = []

        rank.append(i)
        mentions.append(value["count_ticker"])
        get_db().upsert({"ticker": value["ticker"], "rank": rank, "mentions": mentions}, query().ticker == value['ticker'])


def get_top():
    return get_db().search(query().rank[-1] == 0)


# TODO: Figure out when to get into the market and with what sized bet based on sentiment
# make sure you don't short SPY lol
def activation():
    pass


# TODO: Figure out when to get out of the market based on percent price
def deactivation():
    pass


# TODO: Find better time interval for when to get new data
sched.add_job(update_db, "cron", [get_data()], day_of_week='mon-fri', hour=20)


if __name__ == "__main__":
    update_db(get_data())
    print(get_top())
    # sched.start()
