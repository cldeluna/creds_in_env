#!/usr/bin/python -tt
# Project: creds_in_env
# Filename: load_2env
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "8/8/20"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import os

# pip install python-decouple (UTF-8 encoding by default)
import decouple

import add_2env


def check_dotenv_file(path):
    # Check to make sure the .env file is valid
    if not os.path.isfile(path):

        print(f"ERROR! File {path} NOT FOUND! Aborting program execution...")
        exit()

    return os.path.isfile(path)


def main():

    valid_env_file = check_dotenv_file(os.path.join(os.getcwd(), '.env'))

    # Verify that the environment variables in our .env file are set
    # Using the variables in the .env_example file - Remember to update as needed
    list_of_vars = ['API_KEY', 'MY_ENV', 'MY_REPO', 'CONTEXT', 'NETUSER', 'NETPASS', 'MY_BOOL', 'MY_INT', 'TEST']

    print(f"\n======= View Variables loaded from .env file: ")
    for var in list_of_vars:
        print(f".env file variable name: {var} with value: {decouple.config(var)} of type {type(decouple.config(var))}")

    env_bool_value = decouple.config('MY_BOOL', default=False, cast=bool)
    print(f"\nBoolean Value with default and cast set:  variable MY_BOOL "
          f"with value: {env_bool_value} "
          f"of type {type(env_bool_value)}")

    env_int_value = decouple.config('MY_INT', default=0, cast=int)
    print(f"\nInteger Value with default and cast set:  variable MY_INT"
          f" with value: {env_int_value} "
          f"of type {type(env_int_value)}\n")

    # Confirm that while values were loaded from the .env file they were not set as environment variables
    test_check_dict = add_2env.check_env('TEST')
    print(f"\nChecking for environment variable: {test_check_dict['NAME']}:")
    print(f"\tExists: {test_check_dict['EXISTS']}")
    print(f"\tValid: {test_check_dict['VALID']}")
    print(f"\tValue: {test_check_dict['VALUE']}")


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python load_2env' ")
    arguments = parser.parse_args()
    main()
