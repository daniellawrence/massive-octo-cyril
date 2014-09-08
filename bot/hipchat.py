#!/usr/bin/env python
from bot import Bot
import time
import hypchat
import datetime
import pytz


def message_for_me(name, message):
    if message.startswith('@%s' % name):
        return True
    return False


class HipChatBot(Bot):

    API_RATE_LIMIT_SECONDS = 10

    def __init__(self, name, apikey, room_name):
        self.name = name
        self.apikey = apikey
        self.room_name = room_name
        self.hc = None
        self.msgdate = datetime.datetime.now(tz=pytz.utc)
        # super().__init__(name)
        super(HipChatBot, self).__init__(name)

    def _listen(self):
        responses = set([])
        new_messages = self.get_new_messages()
        for message in new_messages:
            if not message_for_me(self.name, message):
                continue
            # message_from_room = message['room']['name']
            message_from_room = "test"
            try:
                response = self.respond_to(message)
            except Exception as response_error:
                response = "%s" % response_error
            if response:
                responses.add((message_from_room, response))
        return responses

    def run(self):
        self.connect_hipchat()
        self.listen()

    def listen(self):
        while True:
            responeses = self._listen()
            self.send_responses(responeses)
            time.sleep(self.API_RATE_LIMIT_SECONDS)

    def get_new_messages(self):
        hist = self.room.history()['items']
        new_messages = []
        for message in hist:
            if message['date'] <= self.msgdate:
                continue
            self.msgdate = message['date']
            new_messages.append(message['message'])
        return new_messages

    def format_response(self, message, room=''):
        message = "%s" % "<br />".join(message.split('\n'))
        return "@%s %s" % (room, message)

    def send_responses(self, responeses):
        for room, message in responeses:
            self.send_response(message, room)

    def send_response(self, message, room=''):
        self.room.message(message)

    def connect_hipchat(self):
        self.hc = hypchat.HypChat(self.apikey)
        rooms = self.hc.rooms()['items']
        for room in rooms:
            if room['name'] == self.room_name:
                break
        else:
            raise Exception("Unable to find room: %s" % self.rooms)
        self.room = room
        self.send_response(
            "%s listening in on room %s!" %
            (self.name, self.room_name)
        )
        return room
