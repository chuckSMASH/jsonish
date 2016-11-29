from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from . import tokens


logging.basicConfig(
    format='[%(asctime)s] - %(levelname)s: %(message)s',
    level=logging.INFO
)


def tokenize(s):
    """
    Convert an input string s into a list of Tokens
    """
    logging.debug('Attempting to tokenize: {}'.format(s))
    tokens = []
    remaining_str = s
    while remaining_str != '':
        remaining_str, token = _consume_next_symbol(remaining_str)
        tokens.append(token)
        logging.debug('appended token: {}'.format(token))
    return tokens


def _advance_to_next_symbol(s):
    for idx, character in enumerate(s):
        if not tokens.WHITESPACE.regex.match(character):
            return s[idx:]
    return ''


def _consume_next_symbol(s):
    s = _advance_to_next_symbol(s)
    next_char = s[0] if len(s) > 0 else ''
    if next_char == '"':
        s, token = _consume_next_string(s)
    elif next_char != '':
        s, token = _consume_next_literal(s)
    else:
        s, token = '', tokens.EMPTY_STRING('')
    return s, token


def _consume_next_string(s):
    curr_idx = 0
    s_length = len(s)
    while curr_idx < s_length:
        if tokens.STRING.regex.match(s[:curr_idx]):
            return s[curr_idx:], tokens.STRING(s[:curr_idx])
        curr_idx += 1
    raise ValueError('Unable to consume next string in `{}`'.format(s))


def _consume_next_literal(s):
    curr_idx = 0
    s_length = len(s)
    while curr_idx <= s_length:
        for token_type in tokens.TOKEN_CLASSES:
            matches_current = token_type.regex.match(s[:curr_idx])
            does_not_match_next = token_type.regex.match(s[:curr_idx+1])
            at_end = curr_idx + 1 > s_length
            if matches_current and (not does_not_match_next or at_end):
                return s[curr_idx:], token_type(s[:curr_idx])
        curr_idx += 1
    raise ValueError('Unable to consume next literal in `{}`'.format(s))
