from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from jsonish import lexer


class TextRegexes(unittest.TestCase):

    def test_string_literal(self):
        good_strs = [
            r'""',
            r'"a"',
            r'"\""',
            r'"\\a\\b\\\""',
            r'"\"\\\"\\\""',
            r'"42"',
        ]
        bad_strs = [
            r'',
            r' ""',
            r'"" ',
            r'"\\""',
            r"''",
            r'"\\\\""',
            r'nostartquote"',
            r'"noendquote',
            r'42',
            r'',
        ]
        for good_str in good_strs:
            self.assertIsNotNone(lexer.STRING_LITERAL.regex.match(good_str))
        for bad_str in bad_strs:
            self.assertIsNone(lexer.STRING_LITERAL.regex.match(bad_str))

    def test_number_literal(self):
        good_nums = [
            r'1',
            r'0',
            r'1.0',
            r'21.234',
            r'-32.233e4',
            r'12E+30',
        ]
        bad_nums = [
            r'01',
            r'1.',
            r'.23',
            r'1+e',
            r'1+e5',
            r'+1',
            r'0-1',
            r'1.0.0',
            r'12E+30-5',
            r'"42"',
            r'',
        ]
        for good_num in good_nums:
            self.assertIsNotNone(lexer.NUMBER_LITERAL.regex.match(good_num))
        for bad_num in bad_nums:
            self.assertIsNone(lexer.NUMBER_LITERAL.regex.match(bad_num))

    def test_key_literal(self):
        good_keys = [
            r'"\\"',
            r'""',
            r'"\u79af"',
            r'"\""',
            r'"\"\\\\\"\\\\"',
            r'"abcdef\\\\"',
            r'"123"'
        ]
        bad_keys = [
            r'123',
            r'true',
            r'"\t"',
            r'"\b"',
            r'"\n"',
            r'"\r"',
            r'"\f"',
        ]
        for good_key in good_keys:
            self.assertIsNotNone(lexer.KEY_LITERAL.regex.match(good_key))
        for bad_key in bad_keys:
            self.assertIsNone(lexer.KEY_LITERAL.regex.match(bad_key))

    def test_simple_literals(self):
        for token, s in (
                (lexer.OBJ_START_LITERAL, '{'),
                (lexer.OBJ_END_LITERAL, '}'),
                (lexer.ARRAY_START_LITERAL, '['),
                (lexer.ARRAY_END_LITERAL, ']'),
                (lexer.COMMA_LITERAL, ','),
                (lexer.COLON_LITERAL, ':'),
                (lexer.NULL_LITERAL, 'null'),
                (lexer.BOOLEAN_LITERAL, 'true'),
                (lexer.BOOLEAN_LITERAL, 'false'),
        ):
            self.assertIsNotNone(token.regex.match(s))
            self.assertIsNone(token.regex.match(s + ' '))
            self.assertIsNone(token.regex.match(' ' + s))
            self.assertIsNone(token.regex.match(s + s))
            if s.upper() != s:
                self.assertIsNone(token.regex.match(s.upper()))
            if s.lower() != s:
                self.assertIsNone(token.regex.match(s.lower()))
