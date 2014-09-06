#!/usr/bin/env python
import re


class Bot(object):

    listen_map = {}

    def __init__(self):
        pass

    def add_listen_rule(self, rule, endpoint, **kwargs):
        self.listen_map[rule] = endpoint

    def listen_for(self, rule, **kwargs):

        def decorator(endpoint):
            self.add_listen_rule(rule, endpoint, **kwargs)
            return endpoint
        return decorator

    def match_message_to_listen_rule(self, message):
        for rule, function in self.listen_map.items():
            rule_match = re.match(rule, message)
            if not rule_match:
                continue
            return rule, function, rule_match.groupdict()
        return None, None, None

    def respond_to(self, message):
        (rule, function, kwargs) = self.match_message_to_listen_rule(message)
        if rule is None or function is None:
            return
        response = "%s: %s" % (function.__name__, function(**kwargs))
        print(response)


if __name__ == '__main__':
    bot = Bot()

    @bot.listen_for("hello (?P<name>\w+)")
    def hello(name):
        return "hello %s, from bot" % name

    @bot.listen_for("hi (?P<name>\w+)")
    def hi(name):
        return "hi %s, from bot" % name

    def echo(message):
        return "%s" % message
    bot.add_listen_rule("echo (?P<message>.*)", echo)

    bot.respond_to("hello bob")
    bot.respond_to("hi bob")
    bot.respond_to("bye bob")
    bot.respond_to("echo bob bob bob")
