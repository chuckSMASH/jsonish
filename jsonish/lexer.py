from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import re
import sys


class TokenMeta(type):
    def __new__(cls, name, parents, dct):
        if not dct.get('regex') and not dct.get('regex_str'):
            raise TypeError('Literal classes must be defined with a regex')
        elif not dct.get('regex'):
            regex_str = dct.get('regex_str')
            dct['regex'] = re.compile(regex_str)
        return super(TokenMeta, cls).__new__(cls, name, parents, dct)


class Token(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '<{} (value: {})>'.format(self.__class__.__name__, self.value)


def token_class_factory(name, regex_str):
    return TokenMeta(name.encode('ascii'), (Token,), {'regex_str': regex_str})


STRING_PATTERN = r'^"(\\"|\\\\|\\/|\b|\f|\n|\r|\t|\\u[A-Fa-f0-9]{4}|[^"\\])*"$'
NUMBER_PATTERN = r'^-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?$'
BOOLEAN_PATTERN = '^(true|false)$'
KEY_PATTERN = r'^"(\\"|\\\\|\\u[A-Fa-f0-9]{4}|[^"\\\b\f\n\r\t])*"$'

OBJ_START_LITERAL = token_class_factory('OBJ_START_LITERAL', r'^{$')
OBJ_END_LITERAL = token_class_factory('OBJ_END_LITERAL', r'^}$')
ARRAY_START_LITERAL = token_class_factory('ARRAY_START_LITERAL', r'^\[$')
ARRAY_END_LITERAL = token_class_factory('ARRAY_END_LITERAL', r'^\]$')
COMMA_LITERAL = token_class_factory('COMMA_LITERAL', r'^,$')
COLON_LITERAL = token_class_factory('COLON_LITERAL', r'^:$')
NULL_LITERAL = token_class_factory('NULL_LITERAL', r'^null$')
STRING_LITERAL = token_class_factory('STRING_LITERAL', STRING_PATTERN)
NUMBER_LITERAL = token_class_factory('NUMBER_LITERAL', NUMBER_PATTERN)
BOOLEAN_LITERAL = token_class_factory('BOOLEAN_LITERAL', BOOLEAN_PATTERN)
KEY_LITERAL = token_class_factory('KEY_LITERAL', KEY_PATTERN)
