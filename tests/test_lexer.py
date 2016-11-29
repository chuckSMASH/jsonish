from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from jsonish import lexer


class TestAdvanceToNextSymbolTestCase(unittest.TestCase):

    def test_empty_str(self):
        expected = ''
        actual = lexer._advance_to_next_symbol('')
        self.assertEqual(expected, actual)

    def test_no_whitespace(self):
        expected = 'abc'
        actual = lexer._advance_to_next_symbol('abc')
        self.assertEqual(expected, actual)

    def test_beginning_whitespace(self):
        expected = 'abc'
        actual = lexer._advance_to_next_symbol('   abc')
        self.assertEqual(expected, actual)

    def test_ending_whitespace(self):
        expected = 'abc   \t'
        actual = lexer._advance_to_next_symbol('abc   \t')
        self.assertEqual(expected, actual)
