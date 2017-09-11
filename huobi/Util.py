# coding=utf-8
import hashlib
import time
import urllib
import urllib.parse
import urllib.request
import datetime
import hmac
import base64
import json
import configparser

config = configparser.ConfigParser()
with open('config.ini') as configfile:
    config.readfp(configfile)

ACCESS_KEY = config.get('HUOBI', 'access_key')
SECRET_KEY = config.get('HUOBI', 'secret_key')

LANG = 'zh-CN'

DEFAULT_GET_HEADERS = {
    'Accept': 'application/json',
    'Accept-Language': LANG
}

DEFAULT_POST_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Accept-Language': LANG
}


TRADE_URL = "https://be.huobi.com"

HUOBI_SERVICE_API = "https://api.huobi.com/apiv3"
ACCOUNT_INFO = "get_account_info"
GET_ORDERS = "get_orders"
ORDER_INFO = "order_info"
BUY = "buy"
BUY_MARKET = "buy_market"
CANCEL_ORDER = "cancel_order"
NEW_DEAL_ORDERS = "get_new_deal_orders"
ORDER_ID_BY_TRADE_ID = "get_order_id_by_trade_id"
SELL = "sell"
SELL_MARKET = "sell_market"

'''
发送信息到api
'''
def send2api(pParams, extra):
    pParams['access_key'] = ACCESS_KEY
    pParams['created'] = int(time.time())
    pParams['sign'] = createSign(pParams)
    if(extra) :
        for k in extra:
            v = extra.get(k)
            if(v != None):
                pParams[k] = v
        #pParams.update(extra)
    tResult = httpRequest(HUOBI_SERVICE_API, pParams)
    return tResult

'''
生成签名
'''
def createSign(params):
    params['secret_key'] = SECRET_KEY;
    params = sorted(params.items(), key=lambda d:d[0], reverse=False)
    message = urllib.parse.urlencode(params)
    message=message.encode(encoding='UTF8')
    m = hashlib.md5()
    m.update(message)
    m.digest()
    sig=m.hexdigest()
    return sig

'''
request
'''
def httpRequest(url, params, method='post'):
    if (method == 'get'):
        fp = urllib.request.urlopen(url)
    else:
        postdata = urllib.parse.urlencode(params)
        postdata = postdata.encode('utf-8')
        fp = urllib.request.urlopen(url, postdata)
    if fp.status != 200:
        return None
    else:
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        return mystr

def api_key_request(method, params, request_path):
    timestamp = _getTime()
    params_to_sign = {'AccessKeyId': ACCESS_KEY,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': timestamp}

    host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname

    params_to_sign['Signature'] = getSign(params_to_sign, method, host_name,
                                             request_path, SECRET_KEY)
    url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    return _request(method, url, params)

def getSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')
    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature

def _request(method, url, params):
    params = json.dumps(params).encode('utf-8')
    headers = DEFAULT_GET_HEADERS if method=='GET' else DEFAULT_POST_HEADERS
    req = urllib.request.Request(url, data=params, headers=headers, method=method)
    fp = urllib.request.urlopen(req)
    if fp.status != 200 :
            return None
    else:
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            mystr = json.loads(mystr)
            return mystr

def _getTime():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

