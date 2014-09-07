#!/usr/bin/env python
from bot import Bot
import time


def message_for_me(name, message):
    if message.startswith('@%s' % name):
        return True
    return False


class HipChatBot(Bot):

    API_RATE_LIMIT_SECONDS = 2

    def __init__(self, name, apikey, rooms):
        self.name = name
        self.apikey = apikey
        if isinstance(rooms, str):
            rooms = [rooms]
        self.rooms = rooms
        super().__init__(name)

    def _listen(self):
        responses = set([])
        new_messages = self.get_new_messages()
        for message in new_messages:
            if not message_for_me(self.name, message):
                continue
            # message_from_room = message['room']['name']
            message_from_room = "test"
            response = self.respond_to(message)
            if response:
                responses.add((message_from_room, response))
        return responses

    def listen(self):
        while True:
            responeses = self._listen()
            self.send_responses(responeses)
            time.sleep(self.API_RATE_LIMIT_SECONDS)

    def get_new_messages(self):
        raise NotImplemented("idk how to reach the servers")

    def format_response(self, message, room):
        return "@%s %s" % (room, message)

    def send_responses(self, responeses):
        for room, message in responeses:
            self.send_response(message, room)

    def send_response(self, message, room):
        print(self.format_response(message, room))  # noqa
