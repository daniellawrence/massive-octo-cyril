from bot import Bot
import unittest


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.bot = Bot("testbot")

    def tearDown(self):
        self.bot = None

    def test_setup_and_teardown(self):
        self.assertEqual(self.bot.listen_map, {})

    def test_bot_defaults(self):
        self.assertEqual(self.bot.__class__.__name__, "Bot")
        self.assertEqual(self.bot.listen_map, {})
        with self.assertRaises(Exception):
            self.bot.listen()

    def test_bot_add_deco(self):
        self.assertEqual(self.bot.listen_map, {})

        @self.bot.listen_for("hi")
        def hi():
            pass

        self.assertIn('^@testbot hi$', self.bot.listen_map.keys())
        self.assertEqual(len(self.bot.listen_map.keys()), 1)

    def test_bot_matching(self):
        self.assertEqual(self.bot.listen_map, {})

        @self.bot.listen_for("hi")
        def hi():
            pass
        self.assertIn('^@testbot hi$', self.bot.listen_map.keys())
        self.assertEqual(len(self.bot.listen_map.keys()), 1)
        (rule, function, kwargs) = self.bot.match_message_to_listen_rule("@testbot hi")
        self.assertEqual(rule, '^@testbot hi$')
        self.assertEqual(kwargs, {})
        (rule, function, kwargs) = self.bot.match_rule("hello")
        self.assertEqual(rule, None)
        self.assertEqual(kwargs, None)

        @self.bot.listen_for("bye (?P<name>\w+)")
        def bye(name):
            return "cya %s" % name

        self.assertIn('^@testbot bye (?P<name>\w+)$', self.bot.listen_map.keys())
        self.assertEqual(len(self.bot.listen_map.keys()), 2)

        (rule, function, kwargs) = self.bot.match_rule("bye")
        self.assertEqual(rule, None)
        self.assertEqual(kwargs, None)

        (rule, function, kwargs) = self.bot.match_rule("@testbot bye bob")
        self.assertEqual(rule, "^@testbot bye (?P<name>\w+)$")
        self.assertEqual(kwargs, {'name': 'bob'})
        self.assertEqual(function(**kwargs), "cya bob")

    def test_bot_response_to_hi(self):
        self.assertEqual(self.bot.listen_map, {})

        @self.bot.listen_for("hi")
        def hi():
            return "called from hi"

        self.assertIn('^@testbot hi$', self.bot.listen_map.keys())
        self.assertEqual(len(self.bot.listen_map.keys()), 1)
        self.assertEqual(self.bot.respond_to("@testbot hi"), "called from hi")
        self.assertEqual(self.bot.respond_to("missing_function"), None)

# unittest.main()
