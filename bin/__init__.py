from hashlib import md5 as _md5


def md5(data):
    return _md5(str(data).encode()).hexdigest()

