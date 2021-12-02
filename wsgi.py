"""
Message in a Bottle
Web Server Gateway Interface

This file is the entry point for
mib-users-ms microservice.
"""

from mib import create_app, create_celery
from flask_mail import Mail
from flask_mail import Message as MessageFlask
import random
import requests
from flask import abort
from celery.schedules import crontab
from celery import Celery


# application instance
app = create_app()
celery_app = create_celery()
mail = Mail(app)

from mib.db_model.lottery_db import db, Lottery

# Celery Tasks
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    '''
        Set the time for Celery tasks:
         - every 1 minute execute the task "checkNewMessage"
         - every 1 minute execute the task "checkMessageOpened"
         - every month at day 1 and time 11:00 execute the task "lottery"
    '''
    # LOTTERY: Executes every month
    sender.add_periodic_task(
        crontab(hour=11, minute=00, day_of_month='1'), lottery.s())
    #sender.add_periodic_task(60.0, lottery.s(), name='check for new message received...')


def send_mail_lottery(email, winner):
    '''
        Will send an email after the lottery task to all users, for announcing the winner
    '''
    print("sending lottery mail...")
    msg = MessageFlask("Monthly winner!", sender="provaase5@gmail.com", recipients=email)
    msg.html = """<p>The monthly winner for the lottery is....</p>
                    <h2>{}</h2>""".format(winner)
    mail.send(msg)


def increment_point_user(winner):
    REQUESTS_TIMEOUT_SECONDS = 60.0
    USERS_ENDPOINT = app.config['USERS_MS_URL']
    nickname = ""
    user_id = str(winner)

    try:
        response = requests.get(USERS_ENDPOINT + '/increment_point_user/' + user_id,
                                timeout=REQUESTS_TIMEOUT_SECONDS)
        json_payload = response.json()
        if response.status_code == 200:
            # user is authenticated
            nickname = json_payload["nickname"]
        else:
            raise RuntimeError('Server has sent an unrecognized status code %s' % response.status_code)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return abort(500)
    return nickname


def get_email_by_id(receiver_id):
    REQUESTS_TIMEOUT_SECONDS = 60.0
    USERS_ENDPOINT = app.config['USERS_MS_URL']
    email = ""
    user_id = str(receiver_id)

    try:
        response = requests.get(USERS_ENDPOINT+'/user/'+user_id,
                                timeout=REQUESTS_TIMEOUT_SECONDS)
        json_payload = response.json()
        if response.status_code == 200:
            # user is authenticated
            email = json_payload["email"]
        else:
            raise RuntimeError('Server has sent an unrecognized status code %s' % response.status_code)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return abort(500)
    return email

@celery_app.task
def lottery():
    '''
        Recover all the participants to the lottery and extract a random winner.
        Will add "1 lottery point" to the winner
        At the end send an email to all participant with the nickname of the winner.
    '''
    print("lottery task")

    # List of participants
    list_participant = []

    # Retrive the participants to the montlhy lottery
    participants = db.session.query(Lottery)
    if participants.all():
        print("partecipanti: " + str(participants.all()))
        for user in participants.all():
            print(user)
            print(user.contestant_id)
            list_participant.append(user.contestant_id)

        # Reset monthly lottery table
        addresses = db.session.query(Lottery)
        addresses.delete()
        db.session.commit()

        if len(list_participant) == 0:
            return False

        # Extract a random winner
        # winner = randint(0,len(list_participant)-1)
        system_random = random.SystemRandom()
        winner = system_random.randint(0, len(list_participant) - 1)
        print("winner: " + str(winner))

        winner = list_participant[winner]

        # Increment user points and return the nickname of the winner
        nickname_winner = increment_point_user(winner)

        email_user_list = []
        for item in list_participant:
            participant_email = get_email_by_id(item)
            email_user_list.append(participant_email)
        send_mail_lottery(email_user_list, nickname_winner)

        return True



if __name__ == '__main__':
    app.run()
