#!/usr/bin/python -tt
# Project: creds_in_env
# Filename: add_2env
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "8/6/20"
__copyright__ = "Copyright (c) 2020 Claudia"
__license__ = "Python"

## All modules in this script are part of Python
import argparse
import os
import getpass
import pprint
import json


# Setting environment variables via the Linux CLI
# export NETUSER=cisco
# export NETPASS=cisco
# In Bash (OS-X or Linux), use unset to remove an environment variable
# unset NETUSER
# unset NETPASS


def all_env_vars(verbose=True):
    """
    :param verbose: Optional parameter to enable (True) or disable (False) printed output to STDOUT
    :return:

    """
    env_vars = os.environ

    if verbose:
        if "USER" in env_vars.keys():
            sys_user = os.environ['USER']
        elif "USERNAME" in env_vars.keys():
            sys_user = os.environ['USERNAME']
        else:
            sys_user = "System Username cannot be determined"
        print(f"\n======== ENVIRONMENT VARIABLES for USER {sys_user} ======== ")
        pprint.pprint(dict(env_vars), width  = 4)

    # Return all the environment variables as a dictionary
    return dict(env_vars)


def check_env(env_var):
    """
    :param env_var: Name of environment variable to check for existence and validity

    Checks for both the existence of an environment variable as well as existence and empty
    Returns three variables

    :return:
    var_exists: Variable is set in the environment
    var_exists_empty: Variable exists in the environment and is empty
    var_valid: Variable is valid (exists and is not empty)
    """
    var_info = {}

    var_info.update({'NAME': env_var})
    var_info.update({'EXISTS': False})
    var_info.update({'EMPTY': False})
    var_info.update({'VALID': False})
    var_info.update({'VALUE': os.getenv(env_var)})

    if os.getenv(env_var) and os.environ[env_var] != '':
        var_info.update({'EXISTS': True})
        var_info.update({'VALID': True})

    if env_var in os.environ.keys():
        if os.environ[env_var] == '':
            var_info.update({'EXISTS': True})
            var_info.update({'EMPTY': True})
            var_info.update({'VALID': False})

    return var_info


def set_env(desc="Username", always_upper=True, sensitive=False, debug=True):
    """
    Brief function to set environment variables (name/value) using the Python built in os module

    The function has 4 optional parameters:
    desc: Cosmetic message for the Input text to remind the user what key/value pair is being requested.
    Default: "Username"
    always_upper: Boolean used to convert the name to Uppercase to adhere to convention Default: True
    sensitive: Boolean used to

    Returns:
    os_var_valid; the variable is set and valid
    """

    print(f"\n======== Creating Environment Variable for {desc} ========")
    if always_upper: print(f"**** Variable NAME will be set to all uppercase per convention...")
    env_var_name = input(f"\nPlease enter {desc} environment variable name: ")

    if sensitive:
        env_var_value = getpass.getpass(f"Please enter {desc} sensitive environment variable value "
                                        f"(will not echo to screen): ")
    else:
        env_var_value = input(f"Please enter {desc} environment variable value: ")

    # If the always_upper option is True make the environment variable name all uppercase
    if always_upper:
        env_var_name = env_var_name.upper()

    # Set the environment variable in the Operating System
    os.environ[env_var_name] = env_var_value

    os_var_info_dict = check_env(env_var_name)

    if debug:
        if sensitive:
            if os_var_info_dict['VALID']:
                print(f"\n======== ENV SET Environment Variable {env_var_name} set and valid ========\n")
            else:
                print(f"\n======== ERROR! Environment Variable {env_var_name} set but EMPTY! ========\n")
        else:
            if os_var_info_dict['VALID']:
                print(f"\n======== ENV SET Environment Variable {env_var_name} set with valid value "
                      f"{os.environ[env_var_name]} ========\n")
            else:
                print(f"\n======== ERROR! Environment Variable {env_var_name} set but EMPTY! ========\n")

    return os_var_info_dict['VALID'], os_var_info_dict


def unset_env(env_var=''):
    # Unsetting environment variables depends on OS feature support and may not have expected outcome
    if not env_var:
        env_var = input(f"\nPlease enter environment variable name to UNSET: ")
    os.putenv(env_var, '')

    return os.unsetenv(env_var)


def main():

    print(f"\nCurrent Environment Variables:")
    env_vars_dict = all_env_vars()
    # evars_json = json.dumps(evars, indent=4, sort_keys=True)
    # print(evars_json)

    # Call the set_env function, by default the description of the environment variable is "Username". 
    # There is nothing special about this description value.
    # Its just a reminder of what key/value pair you are creating.
    set_env()
    
    # Call the set_env function with a description indicating we are setting a password and set the
    # sensitive option to true so that the password can be typed in securely without echo to the screen
    set_env(desc="Password", sensitive=True)

    env_vars_dict = all_env_vars(verbose=False)
    print(f"\nUPDATED Environment Variables:")
    env_vars_json = json.dumps(env_vars_dict, indent=4, sort_keys=True)
    print(env_vars_json)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python add_2env.py' ")

    arguments = parser.parse_args()
    main()
