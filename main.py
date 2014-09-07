#!/usr/bin/env python
from bot import Bot

if __name__ == '__main__':
    bot = Bot()

    # from examples import web

    @bot.listen_for("hello (?P<name>\w+)")
    def hello(name):
        return "hello %s, from bot" % name

    @bot.listen_for("hi (?P<name>\w+)")
    def hi(name):
        return "hi %s, from bot" % name

    def echo(message):
        return "%s" % message
    bot.add_listen_rule("echo (?P<message>.*)", echo)

    m = bot.respond_to("hello bob")
    print(m)
    m = bot.respond_to("hi bob")
    print(m)
    m = bot.respond_to("bye bob")
    print(m)
    m = bot.respond_to("echo bob bob bob")
    print(m)
    m = bot.respond_to("web hi bob")
    print(m)
