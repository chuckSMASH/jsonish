from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import re


class TokenMeta(type):
    def __new__(cls, name, parents, dct):
        if not dct.get('regex') and not dct.get('regex_str'):
            raise TypeError('Token classes must be defined with a regex')
        elif not dct.get('regex'):
            regex_str = dct.get('regex_str')
            dct['regex'] = re.compile(regex_str)
        return super(TokenMeta, cls).__new__(cls, name, parents, dct)


class BaseToken(object):
    def __init__(self, value):
        self.value = value
        self._check_value()

    def __repr__(self):
        return '<{} (value: {})>'.format(self.__class__.__name__, self.value)

    def __str__(self):
        return repr(self)

    def _check_value(self):
        if not self.regex.match(self.value):
            raise ValueError('Unexpected token: `{}`'.format(self.value))


def token_class_factory(name, regex_str):
    return TokenMeta(
        name.encode('ascii'), (BaseToken,), {'regex_str': regex_str}
    )


STRING_PATTERN = r'^"(\\"|\\\\|\\/|\b|\f|\n|\r|\t|\\u[A-Fa-f0-9]{4}|[^"\\])*"$'
NUMBER_PATTERN = r'^-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?$'
BOOLEAN_PATTERN = '^(true|false)$'
KEY_PATTERN = r'^"(\\"|\\\\|\\u[A-Fa-f0-9]{4}|[^"\\\b\f\n\r\t])*"$'

OBJ_START = token_class_factory('OBJ_START', r'^{$')
OBJ_END = token_class_factory('OBJ_END', r'^}$')
ARRAY_START = token_class_factory('ARRAY_START', r'^\[$')
ARRAY_END = token_class_factory('ARRAY_END', r'^\]$')
COMMA = token_class_factory('COMMA', r'^,$')
COLON = token_class_factory('COLON', r'^:$')
NULL = token_class_factory('NULL', r'^null$')
STRING = token_class_factory('STRING', STRING_PATTERN)
NUMBER = token_class_factory('NUMBER', NUMBER_PATTERN)
BOOLEAN = token_class_factory('BOOLEAN', BOOLEAN_PATTERN)
KEY = token_class_factory('KEY', KEY_PATTERN)
WHITESPACE = token_class_factory('WHITESPACE', '^\s+$')
EMPTY_STRING = token_class_factory('EMPTY_STRING', '^$')


TOKEN_CLASSES = [
    OBJ_START,
    OBJ_END,
    ARRAY_START,
    ARRAY_END,
    COMMA,
    COLON,
    NULL,
    STRING,
    NUMBER,
    BOOLEAN,
]
