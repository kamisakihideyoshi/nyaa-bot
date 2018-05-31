# coding=utf-8
import json
import threading
import time

import requests


class FirebaseAuth(object):
    def __init__(self, api_key: str, email: str, password: str):
        self.headers = {'Content-Type': 'application/json'}
        parameters = {'email': email,
                      'password': password, 'returnSecureToken': 'true'}
        self.token_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=' + api_key
        self.refresh_url = 'https://securetoken.googleapis.com/v1/token?key=' + api_key
        result = requests.post(
            self.token_url, json=parameters, headers=self.headers)
        token_json = json.loads(result.text)
        self.id_token = token_json['idToken']
        self.refresh_token = token_json['refreshToken']
        expiration = int(token_json['expiresIn'])

        threading._start_new_thread(self._start, (expiration,))

    def _refresh(self):
        parameters = {'grant_type': 'refresh_token',
                      'refresh_token': self.refresh_token}
        result = requests.post(
            self.refresh_url, json=parameters, headers=self.headers)
        print('Firebase debug:', result.text)
        token_json = json.loads(result.text)
        self.id_token = token_json['id_token']
        self.refresh_token = token_json['refresh_token']
        expiration = int(token_json['expires_in'])

        return expiration

    def _start(self, expiration: int):
        time.sleep(expiration - 10)
        while True:
            expiration = self._refresh()
            time.sleep(expiration - 10)

    def __str__(self):
        return self.id_token
