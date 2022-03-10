#!/usr/bin/env python3
'''Optimized for macOS Big Sur 11.6'''

# This is a simple export import fieldnames checker.
# It prints number of fields for csv file 1 and csv file 2.

with open("users.csv", newline='', encoding='utf-8') as inp:
    list_1 = list(inp.readline().strip().split(','))
    print("There are " + len(list_1) + " fields in csv file no 1.")

with open("users_to_upload.csv", newline='', encoding='utf-8') as inp2:
    list_2 = list(inp2.readline().strip().split(','))
    print("There are " + len(list_2) + " fields in csv file no 2.")

list_difference = []
for item in list_1:
    if item not in list_2:
        list_difference.append(item)
print(
"These fields are only present in csv no 1:\n"
+ list_difference
)

list_difference_2 = []
for item in list_2:
    if item not in list_1:
        list_difference_2.append(item)
print(
"These fields are only present in csv no 2:\n"
+ list_difference_2
)

for item in list_difference_2:
    print(
    "These are fields only present in csv no 2 and their index numbers:\n"
    + item, list_2.index(item)
    )
