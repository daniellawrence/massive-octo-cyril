massive-octo-cyril
==================

Simple python chat bot


	bot = Bot("mybot")
	
    @bot.listen_for("hello <username>")
    def function_name(username):
        return "hi %s, nice to meet you" % username

	if __name__ == '__main__':
		bot.run()


The bot would respond to 2 things

	you  : @mybot help
	mybot: Try one of:
	mybot: ^@mybot hello <name>   Greet the user
	mybot: ^@mybot help$          Generate a help map

	you:   @mybot hello myname
	mybot: hi myname, nice to meet you.


