#!/usr/bin/env python3
"""
Main file
"""

get_db = __import__('filtered_logger').get_db

print(get_db.__annotations__.get('return'))
db = get_db()
cursor = db.cursor()
cursor.execute("SELECT COUNT(*) FROM users;")
for row in cursor:
    print(row[0])
cursor.close()
db.close()
