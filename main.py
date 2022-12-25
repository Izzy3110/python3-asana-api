import os
from wyl.api import RequestsApi
from wyl.api.asana import AsanaAPI
from wyl.security import Keys
import configparser
import argparse
import sys


global_config = {}


def parse_config(current_args):
    config_filepath_ = str(current_args.config) if current_args.config is not None else "main.ini"
    if os.path.isfile(config_filepath_):
        config = configparser.ConfigParser()
        config.read("main.ini")
        return {s: dict(config.items(s)) for s in config.sections()}
    return {}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    args = parser.parse_args()

    input_pass = os.environ.get('KEY_PASSWORD', "Key1Pass!2%$")
    key_file = os.environ.get('KEY_FILENAME', 'mykey.pem')
    pat = os.environ.get('ASANA_PAT')

    key_length = 4096
    keys = Keys(
        key_file=key_file,
        input_pass=input_pass,
        key_length=key_length
    )

    encrypted_pat = keys.save_encrypted_pat(pat=pat)

    test_ok = str(keys.get_decrypted_pat(encrypted_pat)) == str(pat)
    if not test_ok:
        sys.exit(1)

    requests_api = RequestsApi("asana", token=keys.decrypt_message(encrypted_pat))

    asana_api = AsanaAPI(requests_api, parse_config(args))
