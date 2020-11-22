# Standard Library Imports
import json
import re

from random import choice

# Loading files
# json_file = open("data.json", "r")
# text_file = open("database.txt", "a")
# data = json.load(json_file)

# print(type(data), type(data[0]['category']))
# input("Wait >> ")
# for book in data:
#     book['member_id'] = None
#     book['isbn'] = book['isbn'].replace('-', '').replace('X', '0')
#     text_file.write(json.dumps(book) + "\n")

# text_file.close()
# json_file.close()
input("Load data into database >>> ")
database = open("database.txt", "r+")
database.seek(0)

book_index = [json.loads(book) for book in database]
for book in book_index:
    for other_book in book_index:
        if book['title'] == other_book['title'] and (book['isbn'] != other_book['isbn']) and (book['author'] != other_book['author']):
            other_book['isbn'] = book['isbn']
            other_book['author'] = book ['author']
            print('changed a book')
    database.write(json.dumps(book) + "\n")

database.close()

