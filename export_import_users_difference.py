#!/usr/bin/env python3
'''Optimized for macOS Big Sur 11.6'''

# This is a simple export import user difference checker.
# Used to confirm csv file to be uploaded contains all the users from downloaded csv files.

import os

def find_userfiles(directory):
    '''Iterates over files in that directory, check if there are any.'''
    filenames = []
    # Clears .DS_Store MacOS bullshit file in case MacOS creates it here.
    if os.path.isfile(directory +"/.DS_Store"):
        os.remove(directory +"/.DS_Store")
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            filenames.append(f)
        else:
            print("No User Downloads found.")
    return filenames

def make_user_list(filenames):
    '''Extract all users records from all of the files and creates a list:
       returns a list of dictionaries.'''
    rows_dict_list = []
    for file in filenames:
        with open(file, newline='', encoding='utf-8') as inp:
            lines = inp.readlines()
        for l in range(1, len(lines)):
            if file[0] and l == 1:
                stripped_line = lines[0].strip()
                fieldnames = (stripped_line.split(","))
            line = lines[l]
            stripped_line = line.strip()
            line_list = (stripped_line.split(","))
            row_dictionary = dict(zip(fieldnames, line_list))
            rows_dict_list.append(row_dictionary)
    return rows_dict_list

def main():
    '''This is the main function.'''

    directory = str(input(
            "\nEnter the path to the directory with downloaded data or press enter:\n")
            or 'users_download')
    list_1 = []
    list_2 = []

    files = find_userfiles(directory)

    make_user_list(files)

    with open("users_to_upload.csv", newline='', encoding='utf-8') as inp:
        lines = inp.readlines()
        for l in range(1, len(lines)):
            line = lines[l]
            stripped_line = line.strip()
            line_list = (stripped_line.split(","))
            list_2.append(line_list)

    list_difference = []
    for item in list_1:
        if item not in list_2:
            list_difference.append(item)
    print(list_difference)

    list_difference_2 = []
    for item in list_2:
        if item not in list_1:
            list_difference_2.append(item)
            print(list_difference_2)

if __name__ == "__main__":
    main()

# for item in list_difference_2:
#   print(item, list_2.index(item))
