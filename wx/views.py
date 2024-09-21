import requests
from django.contrib.auth import login
from django.contrib.auth.models import User

from common.decorations import http_log
from common.response import success, error, serialize
from common.utils.jsonutil import loads
from common.utils.dateutil import format_datetime


APPID = 'wx1f23481bc9aab425'
SECRET = '0cb39c1b746a2e0b8e31f3330081017c'
ALARM_MAP = {
    'data': '数据告警',
    'offline': '离线告警',
    'expire': '流量到期提醒',
}


def get_token():
    params = {
        'appid': APPID,
        'secret': SECRET,
        'grant_type': 'client_credential',
    }
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    res = requests.get(url, params)
    if res.status_code == 200:
        access_token = res.json().get('access_token')
        if access_token is not None:
            return access_token
    return ''


@http_log()
def get_openid(request):
    body = loads(request.body)
    js_code = body.get('jsCode', '')
    grant_type = body.get('grantType', 'authorization_code')
    params = {
        'appid': APPID,
        'secret': SECRET,
        'js_code': js_code,
        'grant_type': grant_type,
    }
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    res = requests.get(url, params)
    print(res.json())
    if res.status_code == 200:
        return success(res.json())
    else:
        return error('01', '调用微信接口失败！')
