#!/usr/bin/env python
import re


class Bot(object):

    def __init__(self, name, *args, **kwags):
        self.name = name
        self.listen_map = {}

    def add_listen_rule(self, rule, endpoint, **kwargs):
        rule = "^@%s %s$" % (self.name, rule)
        self.listen_map[rule] = endpoint

    def listen_for(self, rule, **kwargs):

        def decorator(endpoint):
            self.add_listen_rule(rule, endpoint, **kwargs)
            return endpoint
        return decorator

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
        # response = "%s: %s" % (function.__name__, function(**kwargs))
        response = "%s" % function(**kwargs)
        return response

    def listen(self):
        raise NotImplemented("Missing listen method")
