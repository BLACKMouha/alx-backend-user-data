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
    filter_log_line = message
    for field in fields:
        regex = re.compile(f'({field}=)(.+?)(?=;)')
        filter_log_line = re.sub(
            regex,
            f'{field}={redaction}',
            filter_log_line)
    return re.sub(';', separator, filter_log_line)
