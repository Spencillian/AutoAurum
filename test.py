# temp = {"ticker": "GME", "count_ticker": 400}
# arr = [1, 2, 3]
#
# # print(temp["cheese"])
# print(arr[-1])

from investopedia_api import InvestopediaApi

import json

with open('credentials.json') as ifh:
    credentials = json.load(ifh)

client = InvestopediaApi(credentials)

p = client.portfolio

print(p.account_value)
