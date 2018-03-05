#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3 import Retry

import lastpass.fetcher


class CustomLastPassSession(Session):
    def __init__(self):
        super().__init__()

        self.mount('http://', adapter=HTTPAdapter(max_retries=Retry(backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])))
        self.mount('https://', adapter=HTTPAdapter(max_retries=Retry(backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])))


lastpass.fetcher.http = CustomLastPassSession()
