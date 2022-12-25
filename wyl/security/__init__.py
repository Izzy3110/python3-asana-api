import os
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


class Keys(object):
    key_filename = "mykey.pem"
    default_key_length = 4096
    key_format = 'PEM'

    key_password = None
    key = None
    key_file = None
    key_length = None

    def __init__(self, key_file, input_pass, key_length=None):
        self.key_password = input_pass
        self.key_file = key_file
        self.key_length = key_length
        if not os.path.isfile(self.key_file):
            self.write_key()
        self.key = self.load_key(filename=self.key_file, passphrase=self.key_password)
        super(Keys, self).__init__()

    def get_user_key(self, filename, input_pass) -> RSA.RsaKey:
        return self.load_key(filename, input_pass) if self.key is None else self.key

    def save_encrypted_pat(self, pat):
        return self.encrypt_message(pat)

    def get_decrypted_pat(self, encrypted_pat):
        return self.decrypt_message(encrypted_pat)

    def encrypt_message(self, message):
        return PKCS1_OAEP.new(self.key.public_key()).encrypt(message.encode("utf-8"))

    def decrypt_message(self, encrypted_message):
        return PKCS1_OAEP.new(self.key).decrypt(encrypted_message).decode("utf-8")

    def write_key(self):
        if self.key_length is None:
            self.key_length = self.default_key_length
        print("file: "+str(self.key_file))
        if not os.path.isfile(self.key_file):
            with open(self.key_file, 'wb') as f:
                f.write(RSA.generate(self.key_length).export_key(self.key_format, passphrase=self.key_password))
                f.close()

    def load_key(self, filename, passphrase):
        with open(filename, 'r') as r:
            try:
                return RSA.import_key(r.read(), passphrase=passphrase)
            except ValueError as e:
                print(e.args)
                return False
            finally:
                r.close()
