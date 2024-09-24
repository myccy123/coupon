import logging
import os
import time
import uuid
from random import sample
from string import ascii_letters, digits

from django.conf import settings
import requests
from common.decorations import http_log
from common.response import success, error, serialize
from common.utils.jsonutil import loads, dumps
from wechatpayv3 import WeChatPay, WeChatPayType

from wx.models import UserInfo, PaymentInfo

# 微信支付商户号（直连模式）或服务商商户号（服务商模式，即sp_mchid)
MCHID = '1689201091'

# 接入模式:False=直连商户模式，True=服务商模式
PARTNER_MODE = True
SUB_MCHID = '1689210526' if PARTNER_MODE else None

# 商户证书私钥
with open(settings.BASE_DIR / 'cert' / 'apiclient_key.pem') as f:
    PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = '29F1344589281DEC1C57C47AE22477C3AF8E660B'

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = 'zhonghuarenmingongheguowansui123'

# APPID，应用ID或服务商模式下的sp_appid
APPID = 'wx27a560d7b1d32c78'
SUB_APPID = 'wx4e3c719a61caa631'
APP_SECRET = 'cb96bd2434aceb6da98312c0750507c8'

# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = 'http://weaz.fangkuaixiu.com:8000/wx/notify/'

# 微信支付平台证书缓存目录，减少证书下载调用次数，首次使用确保此目录为空目录.
# 初始调试时可不设置，调试通过后再设置，示例值:'./cert'
CERT_DIR = None

# 日志记录器，记录web请求和回调细节
logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG,
                    filemode='a',
                    format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("demo")

# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://requests.readthedocs.io/en/latest/user/advanced/#proxies
PROXY = None

# 请求超时时间配置
TIMEOUT = (10, 30)  # 建立连接最大超时时间是10s，读取响应的最大超时时间是30s

# 初始化
wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.NATIVE,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR,
    logger=LOGGER,
    partner_mode=PARTNER_MODE,
    proxy=PROXY,
    timeout=TIMEOUT
)


def get_token():
    params = {
        'appid': APPID,
        'secret': APP_SECRET,
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
        'appid': SUB_APPID,
        'secret': APP_SECRET,
        'js_code': js_code,
        'grant_type': grant_type,
    }
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    res = requests.get(url, params)
    print(res.json())
    if res.status_code == 200:
        openid = res.json().get('openid', '')
        is_pay = False
        try:
            user = UserInfo.objects.get(openid=openid)
            is_pay = user.is_pay
        except UserInfo.DoesNotExist:
            UserInfo.objects.create(openid=openid)

        return success({'isPay': is_pay, **res.json()})
    else:
        return error('01', '调用微信接口失败！')


@http_log()
def notify(request):
    headers = {
        'Wechatpay-Signature': request.META.get('HTTP_WECHATPAY_SIGNATURE'),
        'Wechatpay-Timestamp': request.META.get('HTTP_WECHATPAY_TIMESTAMP'),
        'Wechatpay-Nonce': request.META.get('HTTP_WECHATPAY_NONCE'),
        'Wechatpay-Serial': request.META.get('HTTP_WECHATPAY_SERIAL')
    }
    result = wxpay.callback(headers=headers, body=request.body)
    resource = result.get('resource', {})
    if result.get('event_type') == 'TRANSACTION.SUCCESS':
        PaymentInfo.objects.create(openid=resource.get('payer').get('sub_openid'),
                                   amount=resource.get('amount').get('total') / 100,
                                   sp_appid=resource.get('sp_appid'),
                                   sub_appid=resource.get('sub_appid'),
                                   sp_mchid=resource.get('sp_mchid'),
                                   sub_mchid=resource.get('sub_mchid'),
                                   sp_openid=resource.get('payer').get('sp_openid'),
                                   sub_openid=resource.get('payer').get('sub_openid'),
                                   note=result.get('summary'),
                                   res_content=dumps(result))
        try:
            u = UserInfo.objects.get(openid=resource.get('payer').get('sub_openid'))
            u.is_pay = True
        except UserInfo.DoesNotExist:
            pass

    print(f'msg from wx: {result}')
    return success()


@http_log()
def get_prepay_id(request):
    body = loads(request.body)
    # 以小程序下单为例，下单成功后，将prepay_id和其他必须的参数组合传递给小程序的wx.requestPayment接口唤起支付
    out_trade_no = ''.join(sample(ascii_letters + digits, 8))
    description = body.get('description', '')
    # 单位为分
    amount = body.get('amount', 1) * 10 * 10
    payer = {'sub_openid' if PARTNER_MODE else 'openid': body.get('openid')}
    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': int(amount)},
        pay_type=WeChatPayType.MINIPROG,
        payer=payer,
        sub_mchid=SUB_MCHID,
        sub_appid=SUB_APPID if PARTNER_MODE else None)

    result = loads(message)
    if code in range(200, 300):
        prepay_id = result.get('prepay_id')
        timestamp = str(int(time.time()))
        noncestr = str(uuid.uuid4()).replace('-', '')
        package = 'prepay_id=' + prepay_id
        sign = wxpay.sign(data=[SUB_APPID, timestamp, noncestr, package])
        signtype = 'RSA'
        return success({
            'appId': APPID,
            'timeStamp': timestamp,
            'nonceStr': noncestr,
            'prepay_id': prepay_id,
            'package': 'prepay_id=%s' % prepay_id,
            'signType': signtype,
            'paySign': sign
        })
    else:
        return error('01', result.get('code'))


@http_log()
def coupon_list(request):
    body = loads(request.body)
    res = wxpay.marketing_favor_stock_list(stock_creator_mchid=SUB_MCHID)
    print(res)
    return success()
