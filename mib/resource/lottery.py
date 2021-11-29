import json
from mib.db_model.lottery_db import Lottery

def lottery_join():
    return json.dumps({"body":"get_lottery"})

def lottery_join_post():
    return json.dumps({"body": "get_lottery"})

def get_lottery():
    return json.dumps({"body":"get_lottery"})


def post_lottery():
    return json.dumps({"body":"post_lottery"})