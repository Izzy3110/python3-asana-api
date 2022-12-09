import requests


class Workspaces(object):
    parent = None

    def __init__(self, parent):
        self.parent = parent

    def get_projects(self, workspace_gid):
        return self.parent.parse_json(
            requests.get(
                f"{self.parent.api_base_url}/workspaces/{workspace_gid}/projects",
                headers=self.parent.mkheader()
            ))
