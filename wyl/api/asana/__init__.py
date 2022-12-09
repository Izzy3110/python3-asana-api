import inspect
import json

import asana
from wyl.api.asana.projects import Projects
from wyl.api.asana.workspacs import Workspaces
from wyl.api.asana.user import User


class AsanaAPI(object):
    api_base_url = "https://app.asana.com/api/1.0"
    token_type = "Bearer"

    client = None
    _ready = False

    user = None

    personal_access_token = None

    workspaces_api = None
    projects_api = None

    def __init__(self, personal_access_token):
        self.personal_access_token = personal_access_token
        self.make_client()

        self.workspaces_api = Workspaces(self)
        self.projects_api = Projects(self)
        self.user_api = User(self)

        me = self.user_api.get_me()
        self.user = AsanaUser(me, self)

        super(AsanaAPI, self).__init__()

    def mkheader(self):
        return {
            "Accept": "application/json",
            "Authorization": self.token_type+" "+self.personal_access_token
        }



    @staticmethod
    def parse_json(api_response):
        response_json = api_response.json()
        if "errors" in response_json:
            for error in response_json["errors"]:
                print(error["message"] + " ", end='')
                print(error["help"])
            return False
        if "data" in response_json:
            return response_json["data"]
        else:
            return response_json

    def make_client(self):
        self.client = asana.Client.access_token(self.personal_access_token)
        if self.client is not None:
            self._ready = True


class AsanaUser(object):
    gid: int = None
    email: str = None
    name: str = None
    photo = None
    resource_type: str = None
    workspaces: list = None

    projects = []
    project_gids = []
    workspace_ids = []

    valid_me = ['gid', 'email', 'name', 'photo', 'resource_type', 'workspaces']

    current_user = None

    def __init__(self, current_user, current_api):
        self.asana_api = current_api
        self.current_user = current_user

        self._parse_me()
        self.set_projects(self.asana_api.projects_api.get_projects())

    def _parse_me(self):
        for k in self.current_user.keys():
            if self.__getattribute__(k) is None and k in self.valid_me:
                if k == "workspaces":
                    for i_w in range(0, len(self.current_user[k])):
                        if self.current_user[k][i_w]["gid"] not in self.workspace_ids:
                            self.workspace_ids.append(int(self.current_user[k][i_w]["gid"]))
                self.__setattr__(k, self.current_user[k])

    projects_dict = {}

    def set_projects(self, projects):
        self.projects = projects
        for p_i in range(0, len(projects)):
            if projects[p_i]["gid"] not in self.projects_dict.keys():
                self.projects_dict[projects[p_i]["gid"]] = projects[p_i]
            self.project_gids.append(int(projects[p_i]["gid"]))

    def to_json(self, str_=None):
        dict_ = {}
        for m in inspect.getmembers(self):
            if not m[0].startswith("_"):
                if m[0] in self.valid_me:
                    dict_[m[0]] = m[1]
        if str_ is not None and str_:
            return json.dumps(dict_)
        else:
            return dict_
