#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from getpass import getpass

from lastpass import exceptions

from utils import get_lastpass_vault


def _user_lastpass_username():
    return input("Enter your LastPass email: ")


def _user_lastpass_password():
    return getpass("Enter your LastPass password: ")


def _user_lastpass_multifactor_password():
    lastpass_multifactor_password = input("If you are using 2FA, enter your code (or press enter to skip this step):")
    return lastpass_multifactor_password or None


def _user_get_lastpass_vault():
    print("Hello this is HaveIBeenPwned for your LastPass vault.")
    print("First we need to log you in to your LastPass account, so we'll need your credentials.")

    retry = 'y'
    while retry == 'y':
        lastpass_username = _user_lastpass_username()
        lastpass_password = _user_lastpass_password()
        lastpass_multifactor_password = _user_lastpass_multifactor_password()

        print("Now we'll try to log you in!")

        try:
            vault = _user_login_lastpass(lastpass_username, lastpass_password, lastpass_multifactor_password)
            break
        except exceptions.Error as e:
            print("Couldn't log you in due to an error: {}".format(e))
            retry = input("Retry with some new credentials? y/n")
    else:
        input("Press any key to exit.")
        sys.exit()

    return vault


def _user_login_lastpass(username, password, multifactor_password=None):
    try:
        try:
            vault = get_lastpass_vault(username, password, multifactor_password)
        except exceptions.LastPassUnknownUsernameError:
            username = _user_lastpass_username()
            password = _user_lastpass_password()
            raise
        except exceptions.LastPassInvalidPasswordError:
            password = _user_lastpass_password()
            raise
        except (exceptions.LastPassIncorrectGoogleAuthenticatorCodeError, exceptions.LastPassIncorrectYubikeyPasswordError):
            multifactor_password = _user_lastpass_multifactor_password()
            raise
    except exceptions.Error:
        vault = get_lastpass_vault(username, password, multifactor_password)

    return vault


def _user_get_mode():
    print("There are multiple modes available: ")
    print("1 - Check all your passwords.")
    print("2 - Check all your usernames on specific domains.")
    print("* - Run all of the above one by one.")

    modes = {'1': ['check_password'], '2': ['check_username'], '*': ['check_password', 'check_username']}
    choices = '/'.join(k for k in modes.keys())
    while True:
        print()
        mode = input("Enter the number of your choice ({}): ".format(choices))
        if mode in modes:
            mode = modes[mode]
            break
        else:
            print("Incorrect mode chosen, retry!")

    return mode
