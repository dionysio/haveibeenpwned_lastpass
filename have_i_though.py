#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback

from haveibeenpwned_wrapper import HaveIBeenPwned
from user_input import _user_get_lastpass_vault, _user_get_mode, get_lastpass_vault
from dateutil.relativedelta import relativedelta as rd


def have_i_though():
    success = []
    fail = []
    try:
        vault = _user_get_lastpass_vault()
        mode = ['check_password']

        number_of_accounts = len(vault.accounts)
        total = rd(seconds=number_of_accounts * 1.5 * len(mode))
        print('''Be patient please, it will take approx. {0.hours} hours {0.minutes} minutes {0.seconds} seconds to query for of your {1} entries.'''.format(total, number_of_accounts))

    except:
        print('Unexpected error occurred:')
        traceback.print_exc()

    return success, fail


def _have_i_though(vault, mode=['get_password', 'get_username']):
    if not isinstance(mode, list):
        mode = [mode]

    pwned = HaveIBeenPwned()
    success = []
    fail = []
    for operation in mode:
        for account in vault.accounts:
            result = {
                'name': account.name.decode(),
                'url': account.url.decode(),
                'username': account.username.decode(),
                'operation': operation
            }
            count_stolen = getattr(pwned, operation)(password=account.password, **result)
            result['count_stolen'] = count_stolen

            if result['count_stolen']:
                print("Password you use on {name}({url}) was part of a breach #{count_stolen} time/s.".format(**result))
                fail.append(result)
            else:
                success.append(result)

    return success, fail


if __name__ == '__main__':
    have_i_though()
