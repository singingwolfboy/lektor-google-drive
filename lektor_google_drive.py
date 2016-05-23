# -*- coding: utf-8 -*-
import sys
import requests
import urllib
from functools import partial
import webbrowser
from lektor.pluginsystem import Plugin
from lektor.types import Type


PY2 = sys.version_info[0] == 2
if PY2:
    input = raw_input
    quote_plus = urllib.quote_plus
else:
    quote_plus = urllib.parse.quote_plus


class GoogleDriveFile(object):
    scopes = ["https://www.googleapis.com/auth/drive.readonly"]

    def __init__(self, file_id, client_id, client_secret, access_token=None):
        self.file_id = file_id
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token = access_token

    @property
    def access_token(self):
        if self._access_token:
            return self._access_token

        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            "response_type=code&redirect_uri=urn:ietf:wg:oauth:2.0:oob&"
            "client_id={client_id}&scope={scopes}"
        ).format(
            client_id=quote_plus(self.client_id),
            scopes=quote_plus(" ".join(self.scopes)),
        )
        webbrowser.open(auth_url)
        code = input("Enter your code: ")

        token_url = "https://www.googleapis.com/oauth2/v4/token"
        token_data = {
            "grant_type": "authorization_code",
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
        }
        resp = requests.post(token_url, data=token_data)
        self._access_token = resp.json()["access_token"]
        return self._access_token

    def get(self):
        url = (
            "https://www.googleapis.com/drive/v3/files/{file_id}"
        ).format(
            file_id=quote_plus(self.file_id),
        )
        headers = {
            "Authorization": "Bearer {token}".format(token=self.access_token),
        }
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        return resp.json()

    def export(self, mimetype="text/plain"):
        url = (
            "https://www.googleapis.com/drive/v3/files/{file_id}/export?"
            "mimeType={mimetype}"
        ).format(
            file_id=quote_plus(self.file_id),
            mimetype=quote_plus(mimetype),
        )
        headers = {
            "Authorization": "Bearer {token}".format(token=self.access_token),
        }
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        return resp.text

    @property
    def title(self):
        return self.get()["name"]

    @property
    def text(self):
        return self.export("text/plain")

    @property
    def html(self):
        return self.export("text/html")

    @property
    def rtf(self):
        return self.export("application/rtf")


class GoogleDriveType(Type):
    widget = 'multiline-text'

    def __init__(self, env, options, client_id, client_secret, access_token=None):
        Type.__init__(self, env, options)
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

    def value_from_raw(self, raw):
        return GoogleDriveFile(
            raw.value, client_id=self.client_id, client_secret=self.client_secret,
            access_token=self.access_token,
        )

class GoogleDrivePlugin(Plugin):
    name = 'Google Drive'
    description = 'Pull content from Google Drive documents'

    @property
    def client_id(self):
        return self.get_config().get('api.client_id')

    @property
    def client_secret(self):
        return self.get_config().get('api.client_secret')

    @property
    def access_token(self):
        return self.get_config().get('api.access_token', None)

    def on_setup_env(self, **extra):
        GoogleDrivePartialType = partial(
            GoogleDriveType,
            client_id=self.client_id, client_secret=self.client_secret,
            access_token=self.access_token,
        )
        self.env.types['google-drive'] = GoogleDrivePartialType
