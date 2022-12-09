import requests


class Projects(object):
    parent = None

    def __init__(self, parent):
        self.parent = parent

    def get_projects(self):
        return self.parent.parse_json(
            requests.get(
                f"{self.parent.api_base_url}/projects",
                headers=self.parent.mkheader()
            ))