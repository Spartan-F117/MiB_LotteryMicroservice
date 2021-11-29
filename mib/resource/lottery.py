from mib.db_model.lottery_db import Lottery, db
from flask import jsonify, request


def join_lottery():
    post_data = request.get_json()
    user_id = post_data.get('id')

    response = {
        "message": "look status code, message correctly parsed"
    }
    try:
        new_contestant = Lottery()
        new_contestant.contestant_id = user_id
        print("User added to lottery db:" + str(user_id))
        db.session.add(new_contestant)
        db.session.commit()
        return jsonify(response), 201
    except Exception as e:
        response["message"] = "error occured"
        return jsonify(response), 302


def is_participant():
    post_data = request.get_json()
    user_id = post_data.get('id')
    print("hello from lottery")
    response = {
        "message": "look status code, message correctly parsed"
    }
    lottery_query = Lottery.query.filter(Lottery.contestant_id == user_id).all()
    print(lottery_query)

    if lottery_query:
        print("invio 201")
        return jsonify(response), 201
    else:
        print("invio 202")
        return jsonify(response), 202
