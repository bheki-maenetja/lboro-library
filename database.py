# Standard Library Imports
import json
import re

# Third Party Imports
json_file = open("data.json", "r")
text_file = open("database.txt", "w")
data = json.load(json_file)

print(type(data), type(data[0]['category']))
input("Wait >> ")
for book in data:
    book['member_id'] = None
    book['isbn'] = book['isbn'].replace('-', '').replace('X', '0')
    text_file.write(json.dumps(book) + "\n")

text_file.close()
json_file.close()
input("Load data into database >>> ")
database = open("database.txt", "r")
for book in database:
    new_data = json.loads(book)
    print(new_data['id'],new_data['member_id'], new_data['author'])

database.close()

