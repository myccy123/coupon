import base64
import random
import hashlib


def camel(s):
    segs = s.split('_')
    cam = segs[0]
    for seg in segs[1:]:
        cam += seg.capitalize()

    return cam


def uncamel(s):
    if s == '':
        return ''

    uncam = s[0].lower()

    for letter in s[1:]:
        if letter.isupper():
            uncam += '_'
        uncam += letter.lower()

    return uncam


def prefill(src, total_length, fill_with='0'):
    if len(str(fill_with)) != 1:
        raise Exception('填充字符只能是1位长度')
    strs = str(src)
    i = len(strs)
    tmp = ''
    for _ in range(total_length - i):
        tmp += str(fill_with)

    return tmp + strs


def endfill(src, total_length, fill_with='0'):
    if len(str(fill_with)) != 1:
        raise Exception('填充字符只能是1位长度')
    strs = str(src)
    i = len(strs)
    tmp = ''
    for _ in range(total_length - i):
        tmp += str(fill_with)

    return strs + tmp


def gen_id(length=8):
    tmp = ''
    for _ in range(length):
        tmp += str(random.randint(0, 9))
    return tmp


def gen_uuid(length=12):
    chars = list(map(chr, range(ord('a'), ord('z')+1)))
    nums = [str(i) for i in range(0, 10)]
    tmp = ''
    for _ in range(length):
        tmp += random.choice(chars + nums)
    return tmp


def md5(s):
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()


def str_to_base64(s):
    if isinstance(s, bytes):
        return base64.b64encode(s).decode()
    else:
        return base64.b64encode(s.encode()).decode()


def decode_base64(data):
    if data == '' or data is None:
        return ''
    data = data.split(',')[1]
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'=' * (4 - missing_padding)
    return base64.b64decode(data)
