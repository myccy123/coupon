import requests
from common.utils.dateutil import now, YYYYMMDDHHMMSS, format_datetime
from common.utils.strutil import md5, str_to_base64


def audio_notification(tel_list, content):
    for tel in tel_list:
        version = '2017-06-30'

        appid = '848814d399f24b2cb6555316b915260d'
        sid = 'c340fae0ba5940329e53754bed06e72b'
        token = 'e789df2aaf2e4b5685392aee61ca1c6d'
        now_ = format_datetime(now(), YYYYMMDDHHMMSS)
        auth = str_to_base64(sid + ':' + now_)
        sig_param = md5(sid + token + now_)

        headers = {
            'Authorization': auth
        }

        body = {
            'voiceNotify': {
                'appId': appid,
                'callee': tel,
                'type': 0,
                'content': content,
                'playTimes': 3,
            }
        }

        url = f'http://message.ucpaas.com/{version}/Accounts/{sid}/Calls/voiceNotify?sig={sig_param}'

        try:
            res = requests.post(url, json=body, headers=headers)
            print(f'通知成功，{tel}，{content}')
            print(res.status_code, res.json())
        except Exception as e:
            print(f'通知失败，{tel}，{content}')
            print(e)


def message_notification(tel_list, content):
    url = 'http://47.98.235.166:9918/sms.aspx'
    params = {
        'userid': '371',
        'account': 'HWRAJ', 'password': 'Hw123654',
        'mobile': ','.join(tel_list),
        'content': f'【建通科技】{content}',
        'sendTime': '',
        'action': 'send', 'extno': ''}
    try:
        res = requests.post(url, params=params)
        print(f"发送短信成功：{tel_list}，{params['content']}")
        print(res.status_code)
    except Exception as e:
        print(f"发送短信失败：{tel_list}，{params['content']}")
        print(e)
