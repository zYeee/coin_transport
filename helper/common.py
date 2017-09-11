# coding=utf-8
from huobi import HuobiService
from okcoin.OkcoinSpotAPI import OKCoinSpot


def getAccountInfo():
    result = {}

    result['huobi'] = {}
    account = HuobiService.accountInfo()
    for info in account['data']['list']:
        if (info['currency'] == 'cny' and info['type'] == 'trade'):
            result['huobi']['cny'] = info['balance']
        if (info['currency'] == 'etc' and info['type'] == 'trade'):
            result['huobi']['etc'] = info['balance']

    result['okcoin'] = {}
    okcoinSpot = OKCoinSpot()
    account = okcoinSpot.userinfo()
    result['okcoin']['cny'] = account['info']['funds']['free']['cny']
    result['okcoin']['etc'] = account['info']['funds']['free']['etc']

    return result
