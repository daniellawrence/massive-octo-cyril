from bot import bot
import unittest


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.bot = bot.Bot("testbot")

    def tearDown(self):
        self.bot = None

    def test_setup_and_teardown(self):
        self.assertEqual(self.bot.listen_map.keys(), ['^@testbot help$'])

    def test_bot_defaults(self):
        self.assertEqual(self.bot.__class__.__name__, "Bot")
        self.assertEqual(self.bot.listen_map.keys(), ['^@testbot help$'])
        with self.assertRaises(Exception):
            self.bot.listen()

    def test_bot_add_deco(self):
        self.assertEqual(len(self.bot.listen_map), 1)
        self.assertEqual(self.bot.listen_map.keys(), ['^@testbot help$'])

        @self.bot.listen_for("hi")
        def hi():
            pass

        self.assertIn('^@testbot hi$', self.bot.listen_map.keys())
        self.assertEqual(len(self.bot.listen_map.keys()), 2)

    def test_bot_matching(self):
        self.assertEqual(self.bot.listen_map.keys(), ['^@testbot help$'])

        @self.bot.listen_for("hi")
        def hi():
            pass

        self.assertIn('^@testbot hi$', self.bot.listen_map.keys())
        self.assertEqual(len(self.bot.listen_map.keys()), 2)
        (rule, function, kwargs) = self.bot.match_rule("@testbot hi")
        self.assertEqual(rule, '^@testbot hi$')
        self.assertEqual(kwargs, {})
        (rule, function, kwargs) = self.bot.match_rule("hello")
        self.assertEqual(rule, None)
        self.assertEqual(kwargs, None)

        @self.bot.listen_for("bye (?P<name>\w+)")
        def bye(name):
            return "cya %s" % name

        self.assertIn('^@testbot bye (?P<name>\w+)$',
                      self.bot.listen_map.keys())
        self.assertEqual(len(self.bot.listen_map.keys()), 3)

        (rule, function, kwargs) = self.bot.match_rule("bye")
        self.assertEqual(rule, None)
        self.assertEqual(kwargs, None)

        (rule, function, kwargs) = self.bot.match_rule("@testbot bye bob")
        self.assertEqual(rule, "^@testbot bye (?P<name>\w+)$")
        self.assertEqual(kwargs, {'name': 'bob'})
        self.assertEqual(function(**kwargs), "cya bob")

    def test_bot_response_to_hi(self):
        self.assertEqual(self.bot.listen_map.keys(), ['^@testbot help$'])

        @self.bot.listen_for("hi")
        def hi():
            return "called from hi"

        self.assertIn('^@testbot hi$', self.bot.listen_map.keys())
        self.assertEqual(len(self.bot.listen_map.keys()), 2)
        self.assertEqual(self.bot.respond_to("@testbot hi"), "called from hi")
        self.assertEqual(self.bot.respond_to("missing_function"), None)

    def test_simple2regex(self):
        d = (
            ('hostname1', 'hostname1'),
            ('hostnamea', 'hostnamea'),
            ('hostname2 hostname2', 'hostname2 hostname2'),
            ('<hostname3', '<hostname3'),
            ('<hostname3a>', '(?P<hostname3a>\\S+)'),
            ('__ <hostname4>', '__ (?P<hostname4>\\S+)'),
            ('hi <h5> <h5>', 'hi (?P<h5>\\S+) (?P<h5>\\S+)'),
            ('(?P<h5a>\\S+)', '(?P<h5a>\\S+)'),
        )
        for simple, regex in d:
            self.assertEqual(bot.simple2regex(simple), regex)

    def test_regex2simple(self):
        d = (
            ('hostname1', 'hostname1'),
            ('hostnamea', 'hostnamea'),
            ('hostname2 hostname2', 'hostname2 hostname2'),
            ('<hostname3', '<hostname3'),
            ('<hostname3a>', '(?P<hostname3a>\\S+)'),
            ('__ <hostname4>', '__ (?P<hostname4>\\S+)'),
            ('hi <h5> <h5>', 'hi (?P<h5>\\S+) (?P<h5>\\S+)'),
        )
        for simple, regex in d:
            self.assertEqual(bot.regex2simple("%s" % regex), "%s" % simple)

    def test_bot_matching_with_kwargs(self):
        self.assertEqual(self.bot.listen_map.keys(), ['^@testbot help$'])

        @self.bot.listen_for("hi <name>")
        def hi(name):
            return name

        self.assertEqual(self.bot.respond_to("@testbot hi bob"), "bob")

    def test_bot_matching_help(self):
        self.assertEqual(self.bot.listen_map.keys(), ['^@testbot help$'])
        self.assertIn("Try one of:", self.bot.respond_to("@testbot help"))
        self.assertIn("@testbot help", self.bot.respond_to("@testbot help"))

        @self.bot.listen_for("hi <name>")
        def hi(name):
            return name

        self.assertIn("@testbot hi <name>",
                      self.bot.respond_to("@testbot help"))

# unittest.main()
