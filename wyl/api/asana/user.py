import configparser
import json
import os


class User(object):
    parent = None
    api_base_url = None

    user_id = None

    def __init__(self, parent):
        config = configparser.ConfigParser()
        config.read("main.ini")

        self.global_config = {s: dict(config.items(s)) for s in config.sections()}

        self.parent = parent

    def get_me(self):
        return self.parent.client.users.me()

    def write_user_file(self):
        if "api."+self.parent.requests_api.provider_name+".Files" in self.global_config.keys():
            file_basepath = self.global_config["api." + self.parent.requests_api.provider_name]["file_basepath"]
            me_file = self.global_config["api."+self.parent.requests_api.provider_name+".Files"]["user"]
            target_filepath = os.path.join(os.getcwd(), file_basepath, "user_"+str(self.user_id), me_file)

            if os.path.isdir(os.path.dirname(target_filepath)):
                data_ = json.dumps(self.parent.user.to_json(), indent=4)
                if not os.path.isfile(target_filepath):
                    with open(target_filepath, "w", encoding="utf-8") as me_json_f:
                        me_json_f.write(data_)
                        me_json_f.close()
                else:

                    with open(target_filepath, encoding="utf-8") as me_json_read:
                        if me_json_read.read().strip() != data_.strip():
                            with open(target_filepath, "w",
                                      encoding="utf-8") as me_json_f:
                                me_json_f.write(json.dumps(self.parent.user.workspaces, indent=4))
                                me_json_f.close()
                        else:
                            print("no change: " + me_file)
                        me_json_read.close()
