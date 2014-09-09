#!/usr/bin/env python
import re


def message_for_me(name, message):
    if message.startswith('@%s' % name):
        return True
    return False


def regex2simple(regex):
    words = regex.split()
    words_regex = []
    for w in words:
        if '?P' not in w:
            words_regex.append(w)
            continue
        regex_w = w.replace('(?P<', '<')
        regex_w = re.sub('>.*', '>', regex_w)
        words_regex.append(regex_w)
    return ' '.join(words_regex)


def simple2regex(regex):
    words = regex.split()
    words_regex = []
    for w in words:
        if '?P' in w:
            words_regex.append(w)
            continue
        regex_w = re.sub(
            r'(<\w+>)',
            r'(?P\1\S+)',
            w
        )
        words_regex.append(regex_w)
    return ' '.join(words_regex)


class Bot(object):

    def __init__(self, name, *args, **kwags):
        self.name = name
        self.listen_map = {}
        self.add_listen_rule('help', self.help)

    def add_listen_rule(self, rule, endpoint, **kwargs):
        rule = "^@%s %s$" % (self.name, rule)
        self.listen_map[rule] = endpoint

    def listen_for(self, rule, **kwargs):
        rule = simple2regex(rule)

        def decorator(endpoint):
            self.add_listen_rule(rule, endpoint, **kwargs)
            return endpoint
        return decorator

    def _listen(self):
        responses = set([])
        new_messages = self.get_new_messages()
        for message in new_messages:
            if not message_for_me(self.name, message):
                continue
            try:
                response = self.respond_to(message)
            except Exception as response_error:
                response = "%s" % response_error  # noqa
            if response:
                responses.add(response)
        return responses

    def run(self):
        self.connect()
        self.listen()

    def match_rule(self, message):
        return self.match_message_to_listen_rule(message)

    def match_message_to_listen_rule(self, message):
        for rule, function in self.listen_map.items():
            rule_match = re.match(rule, message)
            if not rule_match:
                continue
            return rule, function, rule_match.groupdict()
        return None, None, None

    def respond_to(self, message):
        (rule, function, kwargs) = self.match_rule(message)
        if rule is None or function is None:
            return
        if kwargs:
            response = "%s" % function(**kwargs)
        elif function == self.help:
            response = "%s" % self.help()
        else:
            response = "%s" % function()
        return response

    def help(self):
        "Generate a help map"
        output = "Try one of:\n"
        for rule, func in self.listen_map.items():
            description = func.__name__
            if func.__doc__:
                description = func.__doc__
            rule = regex2simple(rule)
            output += "%-50s\t%s\n" % (rule, description)
        return output

    def listen(self):
        raise NotImplemented("Missing listen() method")

    def connect(self):
        raise NotImplemented("Missing connect() method")
