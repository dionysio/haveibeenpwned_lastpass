#!/usr/bin/env python
# -*- coding: utf-8 -*-
import monkeypatch_lastpass
import lastpass


def get_lastpass_vault(username, password, multifactor_password=None):
    return lastpass.Vault.open_remote(username, password, multifactor_password)