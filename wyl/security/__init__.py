import os
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


class Keys(object):
    key_filename = "mykey.pem"
    key_password = None

    default_key_length = 4096

    def __init__(self, key_file, input_pass, key_length=None):
        self.key_password = input_pass
        print("len: "+str(key_length))
        print("pass: "+str(input_pass))
        if not os.path.isfile(key_file):
            self.write_key(input_pass, self.default_key_length if key_length is None else key_length)
        self.key = self.load_key(filename=key_file, passphrase=input_pass)
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

    def write_key(self, filename, passphrase, key_size=None):
        if key_size is None:
            key_size = self.default_key_length
        if not os.path.isfile(filename):
            with open(filename, 'wb') as f:
                f.write(RSA.generate(key_size).export_key('PEM', passphrase=passphrase))
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
