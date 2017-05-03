import datetime
from passlib.hash import pbkdf2_sha256

def RfgStrptime(ts_string):
    ts = None
    try:
        ts = datetime.datetime.strptime(ts_string, "%d-%m-%Y %H:%M")
    except ValueError:
        pass
    return ts

def RfgKeyEncrypt(key):
    return pbkdf2_sha256.encrypt(key, rounds=200000, salt_size=16)

def RfgKeyVerify(key, hashed):
    return pbkdf2_sha256.verify(key, hashed)
