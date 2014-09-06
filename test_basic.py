import main


def test_bot_defaults():
    bot = main.Bot()
    assert bot.__class__.__name__ == "Bot"
    assert bot.listen_map == {}


def test_bot_add_deco():
    bot = main.Bot()
    assert bot.listen_map == {}

    @bot.listen_for("hi")
    def hi():
        pass

    assert 'hi' in bot.listen_map.keys()
    assert len(bot.listen_map.keys()) == 1


def test_bot_matching():
    bot = main.Bot()
    assert 'hi' in bot.listen_map.keys()
    assert len(bot.listen_map.keys()) == 1
    (rule, function, kwargs) = bot.match_message_to_listen_rule("hi")
    assert rule == 'hi'
    assert kwargs == {}
    (rule, function, kwargs) = bot.match_message_to_listen_rule("hello")
    assert rule is None
    assert kwargs is None

    @bot.listen_for("bye (?P<name>\w+)")
    def bye(name):
        return "cya %s" % name

    assert 'bye (?P<name>\w+)' in bot.listen_map.keys()
    assert len(bot.listen_map.keys()) == 2

    (rule, function, kwargs) = bot.match_message_to_listen_rule("bye")
    assert rule is None
    assert kwargs is None

    (rule, function, kwargs) = bot.match_message_to_listen_rule("bye bob")
    assert rule == "bye (?P<name>\w+)"
    assert kwargs == {'name': 'bob'}
    assert function(**kwargs) == "cya bob"
