# Standard Library Imports
import json
import re

from random import choice

# Loading files
json_file = open("data.json", "r")
text_file = open("database.txt", "a")
data = json.load(json_file)

print(type(data), type(data[0]['category']))
input("Wait >> ")
for book in data:
    book['member_id'] = None
    book['isbn'] = book['isbn'].replace('-', '').replace('X', '0')
    book['category'].append(choice(['technology', 'science', 'sports', 'art', 'social']))
    text_file.write(json.dumps(book) + "\n")

text_file.close()
json_file.close()
input("Load data into database >>> ")
database = open("database.txt", "r")
for book in database:
    new_data = json.loads(book)
    print(new_data['id'], new_data['isbn'], new_data['title'], new_data['author'])

database.close()

