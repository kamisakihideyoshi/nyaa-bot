# coding=utf-8
import json
import requests

from .auth import FirebaseAuth


class FirebaseApp(object):
    def __init__(self, app_name, auth: FirebaseAuth=None):
        self.base_url = 'https://' + app_name + '.firebaseio.com/'
        self.auth = auth

    def get(self, child: str = None):
        url = self.base_url
        if child:
            if child[0] == '/':
                child = child[1:]
            url += child

        url += '.json'
        if self.auth:
            url += '?auth=' + self.auth.id_token

        result = requests.get(url)
        return json.loads(result.text)

    def post(self, child: str, data: dict):
        url = self.base_url
        if child:
            if child[0] == '/':
                child = child[1:]
            url += child

        url += '.json'
        if self.auth:
            url += '?auth=' + self.auth.id_token

        requests.post(url, data=json.dumps(data))
        return

    def put(self, child: str, data: dict):
        url = self.base_url
        if child:
            if child[0] == '/':
                child = child[1:]
            url += child

        url += '.json'
        if self.auth:
            url += '?auth=' + self.auth.id_token

        requests.put(url, data=json.dumps(data))
        return
