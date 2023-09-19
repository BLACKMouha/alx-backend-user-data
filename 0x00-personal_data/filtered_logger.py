#!/usr/bin/env python3
'''filtered_logger module'''
import logging
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    '''Returns the log of message obfuscated
    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string used for obfuscating fields
        message: a string, representing the log line
        separator: a string used to separate all fields in the log line'''
    for field in fields:
        regex = re.compile(f'{field}=.+?(?=;)')
        message = re.sub(
            regex,
            f'{field}={redaction}',
            message)
    return re.sub(';', separator, message)
