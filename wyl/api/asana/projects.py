import configparser


class Projects(object):
    parent = None
    api_base_url = None

    user_id = None

    def __init__(self, parent):
        config = configparser.ConfigParser()
        config.read("main.ini")

        self.global_config = {s: dict(config.items(s)) for s in config.sections()}

        self.parent = parent

    def get_projects(self):
        if self.parent.requests_api.provider_name in self.parent.requests_api.providers.keys():
            self.api_base_url = self.parent.requests_api.providers[self.parent.requests_api.provider_name]
        return self.parent.parse_json(

            self.parent.requests_api.get(
                "/projects"
            ))
