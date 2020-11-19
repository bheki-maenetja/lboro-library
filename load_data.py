# Standard Library Imports
import json
import re

# Third Party Imports
my_file = open("data.json", "r")
text_file = open("database.txt", "w")
data = json.load(my_file)

for i in data:
    text_file.write(json.dumps(i) + "\n")

text_file.close()
my_file.close()
input("Load data into database >>> ")
database = open("database.txt", "r")
for i in database:
    new_data = json.loads(i)
    print(new_data, type(new_data))

