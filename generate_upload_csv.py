#!/usr/local/bin/python3
'''Optimized for macOS Big Sur 11.6'''

import secrets
import string
import csv
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

def count_users(filenames):
    '''Counts users in all downloaded files.'''
    user_count = 0
    for file in filenames:
        with open(file, newline='', encoding='utf-8') as inp:
            file_user_count = len(inp.readlines())-1
            user_count += file_user_count
    print(str(user_count) + " users were found.\n")
    return user_count

def generate_passwords(user_count):
    '''Generates passwords for all users into a list.'''
    alphabet = string.ascii_letters + string.digits
    passwords = []

    for _ in range(0, user_count):
        while True:
            password = ''.join(secrets.choice(alphabet) for _ in range(10))
            if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
                break
        passwords.append(password)
    return passwords

def extract_fieldnames(filenames):
    '''Extracts fieldnames/headers and lines/rows from a template file'''
    with open(filenames, newline='', encoding='utf-8') as inp:
        print("File named " + filenames + " opened for extracting fieldnames.\n")
        line = inp.readline()
        stripped_line = line.strip()
        fieldnames = (stripped_line.split(","))
    return fieldnames

def clear_upload_file():
    '''Clear upload file in case there s one already present.'''
    if os.path.isfile("users_to_upload.csv"):
        os.remove(("users_to_upload.csv"))
    return True

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

def prepare_upload_fields(row_dict_list, fieldnames):
    '''Uses template field names to create an upload list - returns a list of dictionaries.'''
    upload_row_dict_list = []
    for row in row_dict_list:
        row_dict = {}
        for field in fieldnames:
            if field in row:
                row_dict[field]=row.get(field)
        upload_row_dict_list.append(row_dict)
    return upload_row_dict_list

def write_passwords(new_row_dictionary_list, password_field, passwords, fieldnames):
    '''Write all user records into the ~new upload file~ with newly generated passwords.'''
    with open('users_to_upload.csv', 'w', encoding='utf-8') as csvfile:
        dictwriter = csv.DictWriter(csvfile,
        fieldnames=fieldnames,
        restval='',
        extrasaction='raise'
        )
        dictwriter.writeheader()
        for line, password in zip(new_row_dictionary_list, passwords):
            line[password_field] = password
            dictwriter.writerow(line)
    return True

def main():
    '''This is the main function.'''
    # Assign directory with csv files to process:
    directory = str(input(
    "\nEnter the path to the directory with downloaded data or press enter:\n")
    or 'users_download')

    # Iterate over files in that directory, check if there are any:
    filenames = find_userfiles(directory)
    print(len(filenames), "files detected.\n")

    # Count users in all downloaded files:
    user_count = count_users(filenames)

    #Generate passwords for all users into a list:
    passwords = generate_passwords(user_count)
    #print(*passwords, sep = "\n")

    # Extract fieldnames/headers and lines/rows from the files:
    template = str(input(
    "Please enter the name of the template file or press enter:\n")
    or 'users.csv')
    fieldnames = extract_fieldnames(template)

    # Clear upload file in case there is one already present:
    clear_upload_file()

    # Extract all users records from all of the files and creates a list -
    # return a list of dictionaries:
    row_dictionary_list = make_user_list(filenames)

    # Uses template field names to create an upload list -
    # return a list of dictionaries:
    new_row_dictionary_list = prepare_upload_fields(row_dictionary_list, fieldnames)
    #print(new_row_dictionary_list[0])

    # Write all user records into the ~new upload file~ with newly generated passwords:
    password_field = str(input("Please enter the exact password field or press enter:\n")
    or 'Password [Required]')
    write_passwords(new_row_dictionary_list, password_field, passwords, fieldnames)

    print("Passwords changed for all users. Export file 'users_to_upload.csv' is ready.\n")

if __name__ == "__main__":
    main()
