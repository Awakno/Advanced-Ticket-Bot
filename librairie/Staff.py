"""
made: awakno
@Contributor: Null
@Version: 1.0
"""
import json

def is_staff(user):
    if json.load(open("config/config.json"))["owner"] == []:
        return False
    else:
        return True if user.id in json.load(open("config/config.json"))["owner"] else False