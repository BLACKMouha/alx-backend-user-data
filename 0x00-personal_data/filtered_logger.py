#!/usr/bin/env python3
'''filtered_logger module'''
import logging
import re
from typing import List
import csv
from os import getenv
import mysql.connector

with open('user_data.csv', mode='r') as f:
    reader = csv.reader(f)
    headers = tuple(next(reader))

PII_FIELDS = headers[0:5]


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
        regex = re.compile(f'({field}=)(.+?)(?={separator})')
        filter_log_line = re.sub(
            regex,
            f'{field}={redaction}',
            filter_log_line)
    return re.sub(';', separator, filter_log_line)


def get_logger() -> logging.Logger:
    '''Creates a logger'''
    logger = logging.getLogger(name='user_data')
    logger.setLevel(level=logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''Returns a conncetion to a database'''
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    user = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db = getenv('PERSONAL_DATA_DB_NAME', 'holberton')

    config = {'host': host, 'user': user, 'password': password, 'database': db}
    return mysql.connector.connection.MySQLConnection(**config)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(fmt=self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''Fitlers values in incoming log records'''
        from datetime import datetime
        s = self.FORMAT % {'name': record.name, 'levelname': record.levelname,
                           'asctime': datetime.now(), 'message': record.msg}
        return filter_datum(self.fields, self.REDACTION, s, self.SEPARATOR)
