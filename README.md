massive-octo-cyril
==================

Simple python chat bot


Add a new function

    @bot.listen_for("regex pattern, (?P<kwarg>\w+)")
    def function_name(kwarg):
        return "Hello from function_name: %s" % kwarg

Testing

    bot.respond("you test message")
