from InvestopediaApi import ita
from googlefinance import getQuotes
from tinydb import TinyDB, Query
import requests
import json
import helper

db = None
cursor = None


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


if __name__ == "__main__":
    for val in get_data()[0]:
        print(val["ticker"])

