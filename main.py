import json
import os
from wyl.api.asana import AsanaAPI
from wyl.security import Keys


if __name__ == '__main__':
    input_pass = "Key1Pass!2%$"
    key_file = 'mykey.pem'
    pat = os.environ.get('ASANA_PAT')
    key_length = 4096

    keys = Keys(
        key_file=key_file,
        input_pass=input_pass,
        key_length=key_length
    )

    encrypted_pat = keys.save_encrypted_pat(pat=pat)
    test_ok = str(keys.get_decrypted_pat(encrypted_pat)) == str(pat)


    ###

    # ----------------------------------

    # ----------------------------------

    ###
    asana_api = AsanaAPI(keys.decrypt_message(encrypted_pat))
    print(json.dumps(asana_api.user.to_json(), indent=4))
    cwd_ = "data"
    if not os.path.isdir(cwd_):
        os.mkdir(cwd_)

    cwd_ = os.path.join(cwd_, "asana")
    if not os.path.isdir(cwd_):
        os.mkdir(cwd_)

    cwd_ = os.path.join(cwd_, "user_"+str(asana_api.user.gid) if not isinstance(asana_api.user.gid, str) else asana_api.user.gid)
    if not os.path.isdir(cwd_):
        os.mkdir(cwd_)

    with open(os.path.join(cwd_, "workspaces.json"), "w", encoding="utf-8") as me_json_f:
        me_json_f.write(json.dumps(asana_api.user.workspaces, indent=4))
        me_json_f.close()

    with open(os.path.join(cwd_, "me.json"), "w", encoding="utf-8") as me_json_f:
        me_json_f.write(json.dumps(asana_api.user.to_json(), indent=4))
        me_json_f.close()
