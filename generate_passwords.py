#!/usr/bin/env python3
'''Optimized for macOS Big Sur 11.6'''

#This is a simple password generator for a 10 char password with 3 numbers.

import secrets
import string

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

USER_COUNT = int(input(
            "\nEnter the number of passwords to generate:\n"))

print(', '.join(generate_passwords(USER_COUNT)))
