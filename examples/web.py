from bot import Bot

bot = Bot()


@bot.listen_for("web hi (?P<name>\w+)")
def webhi(name):
    return "hello %s, from Webster" % name
