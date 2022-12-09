import requests


class User(object):
    parent = None

    def __init__(self, parent):
        self.parent = parent

    def get_me(self):
        return self.parent.client.users.me()
