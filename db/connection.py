"""
made: awakno
@Contributor: Null
@Version: 1.0
"""

import pymongo
import json
from librairie.color import Color

f = open("./config/config.json","r",encoding="utf-8")
config = json.load(f)
url = config["db"]["MDB"]["url"]

client = pymongo.MongoClient(url)
print(f"{Color.green}[{Color.blue}+{Color.green}]{Color.cyan} MongoDB connecté !")
ticket = client.ticket
ticket_db = ticket.ticket_config 
