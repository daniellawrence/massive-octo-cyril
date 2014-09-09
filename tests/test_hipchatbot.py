from bot import hipchat
import unittest


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.bot = hipchat.HipChatBot("testbot", "apikey", "roomname")

    def tearDown(self):
        self.bot = None

    def test_defaults(self):
        self.assertEqual(self.bot.name, "testbot")
        self.assertEqual(self.bot.apikey, "apikey")
        self.assertEqual(self.bot.room_name, 'roomname')

    def test_format_response(self):
        self.assertEqual(self.bot.format_response("msg", "room"), "@room msg")

    def test_get_new_messages(self):
        self.bot.get_new_messages = lambda: ["@testbot help"]
        self.assertIn("@testbot help", self.bot.get_new_messages())

    def test__listen(self):
        self.bot.get_new_messages = lambda: ["@testbot hi"]

        @self.bot.listen_for("hi")
        def hi():
            return "hi"

        responses = self.bot._listen()

        self.assertIn("@testbot hi", self.bot.get_new_messages())
        self.assertEqual(set(['hi']), responses)

    def test__listen_with_listen_for(self):
        self.bot.get_new_messages = lambda: ["@testbot help"]
        responses = self.bot._listen()
        self.assertIn("@testbot help", self.bot.get_new_messages())
        self.assertEqual(type(responses), set)

    def test__listen_without_message_for_bot(self):
        self.bot.get_new_messages = lambda: ["help"]
        responses = self.bot._listen()
        self.assertIn("help", self.bot.get_new_messages())
        self.assertEqual(set([]), responses)
