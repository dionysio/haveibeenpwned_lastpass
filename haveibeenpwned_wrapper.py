#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from hashlib import sha1
from urllib.parse import urlparse, quote, urljoin

try:
    from requests_cache import CachedSession as Session
except ImportError:
    from requests import Session


class HaveIBeenPwned(Session):
    def __init__(self, *args, **kwargs):
        self.last_request = time.time()
        super().__init__(*args, **kwargs)

    def request(self, *args, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['User-Agent'] = headers.pop('User-Agent', 'haveibeenpwned_lastpass v0.666 github.com/dionysio/haveibeenpwned_lastpass')
        kwargs['headers'] = headers

        response = super().request(*args, **kwargs)
        if not response.from_cache:
            self.last_request = time.time()
        return response

    def get(self, url, **kwargs):
        since_last_request = (time.time() - self.last_request)
        if since_last_request < 1.5:
            time.sleep(1.5 - since_last_request)

        response = super().get(url, **kwargs)
        if response.status_code == 429:
            time.sleep(int(response.headers['Retry-After']))
            response = super().get(url, **kwargs)
        return response

    @staticmethod
    def _get_sha1(text):
        return sha1(text).hexdigest().upper()

    @staticmethod
    def _get_domain(url):
        parsed_uri = urlparse(url.decode())
        return '{uri.netloc}'.format(uri=parsed_uri)

    def check_password(self, password, *args, **kwargs):
        hsh = self._get_sha1(password)
        response = self.get('https://api.pwnedpasswords.com/range/{}'.format(hsh[:5]))

        for value in response.text.splitlines():
            returned_hash, count = value.split(':')
            if hsh[5:] in (returned_hash, returned_hash[1:]):
                return count

        return 0

    def check_username(self, username, domain='', *args, **kwargs):
        url = 'https://haveibeenpwned.com/api/breachedaccount/{}'.format(quote(username))
        domain = self._get_domain(domain)
        response = self.get(url, params={'domain': domain})
        if response.text:
            pass
