from __future__ import unicode_literals

from twilio.rest import Client
from django.core.exceptions import MiddlewareNotUsed
import os
import logging
import json

logger = logging.getLogger(__name__)

MESSAGE = """You should leave within the next 15 minutes to make it to your destination on time."""

NOT_CONFIGURED_MESSAGE = """Cannot initialize Twilio notification
middleware. Required enviroment variables TWILIO_ACCOUNT_SID, or
TWILIO_AUTH_TOKEN or TWILIO_NUMBER missing"""


def load_users_file():
    with open('config/users.json') as usersFile:
        users = json.load(usersFile)
        return users


def load_twilio_config():
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = 17193236514

    if not all([twilio_account_sid, twilio_auth_token, twilio_number]):
        logger.error(NOT_CONFIGURED_MESSAGE)
        raise MiddlewareNotUsed

    return (twilio_number, twilio_account_sid, twilio_auth_token)


class MessageClient(object):
    def __init__(self):
        (twilio_number, twilio_account_sid,
         twilio_auth_token) = load_twilio_config()

        self.twilio_number = twilio_number
        self.twilio_client = Client(twilio_account_sid,
                                              twilio_auth_token)

    def send_message(self, body, to):
        self.twilio_client.messages.create(body=body, to=to,
                                           from_=self.twilio_number,
                                           # media_url=['https://demo.twilio.com/owl.png'])
                                           )


class TwilioNotificationsMiddleware(object):
    def __init__(self):
        self.users = load_users_file()
        self.client = MessageClient()

    def process_exception(self, request, exception):
        exception_message = str(exception)
        message_to_send = MESSAGE % exception_message

        for user in self.users:
            self.client.send_message(message_to_send, user['phone'])

        logger.info('Message Sent')

        return None