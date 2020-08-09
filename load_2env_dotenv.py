#!/usr/bin/python -tt
# Project: creds_in_env
# Filename: load_env_decouple.py
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

# pip install dotenv
import dotenv
# from os.path import join, dirname
# from dotenv import load_dotenv

# Here is an example of leveraging code already written
# We have a function to check the existence and validity of an environment variable in the add_2env.py script
import add_2env


def load_env_from_dotenv_file(path):
    # Load the key/value pairs in the .env file as environment variables
    if os.path.isfile(path):
        dotenv.load_dotenv(path)
    else:
        print(f"ERROR! File {path} NOT FOUND! Aborting program execution...")
        exit()

    # # Accessing variables.
    # cntx = os.getenv('CONTEXT')
    # api_key = os.getenv('API_KEY')
    #
    # # Using variables.
    # print(cntx)
    # print(api_key)


def main():

    # Its a good practice to be explicit in code and so explicitly telling dotenv to look in the directory that contains
    # the running script is a good idea
    # Create an OS agnostic full path to the .env file (assuming the .env file you want is in the current working dir
    dotenv_path = os.path.join(os.getcwd(), '.env')

    load_env_from_dotenv_file(dotenv_path)

    # Verify that the environment variables in our .env file are set
    # Using the variables in the .env_example file - Remember to update as needed
    list_of_vars = ['API_KEY', 'MY_ENV', 'MY_REPO', 'CONTEXT', 'NETUSER', 'NETPASS', 'MY_BOOL', 'MY_INT']

    # Look for each of the variables in the list_of_vars list to confirm that they have been set in memory as
    # environment variables
    for var in list_of_vars:
        var_dict = add_2env.check_env(var)
        # print(f"\n")
        print(var_dict)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python load_2env' ")

    #parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',
                        default=False)
    arguments = parser.parse_args()
    main()
