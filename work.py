# coding=utf-8

from huobi import HuobiService, Util
from okcoin.OkcoinSpotAPI import OKCoinSpot
from helper import common

import json
import time
import logging
import ssl


if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    logging.basicConfig(filename='/tmp/log', filemode='a', level=logging.INFO,
                        format='%(asctime)s %(message)s')

    original_account_info = common.getAccountInfo()

    logging.info("begin: huobi: etc(%s) cny(%s) okcoin: etc(%s) cny(%s)\n total: etc(%s) cny(%s)"
            % (original_account_info['huobi']['etc'],
               original_account_info['huobi']['cny'],
               original_account_info['okcoin']['etc'],
               original_account_info['okcoin']['cny'],
               float(original_account_info['huobi']['etc']) + float(original_account_info['okcoin']['etc']),
               float(original_account_info['huobi']['cny']) + float(original_account_info['okcoin']['cny'])
               ))

    okcoinSpot = OKCoinSpot()
    coin_max = hb_max = 0
    while (True):
        coinRes = okcoinSpot.depth('etc_cny')
        coinRes_sell = coinRes['asks'][-1][0]
        coinRes_buy = coinRes['bids'][0][0]

        hbRes = HuobiService.getDepth()
        hbRes = json.loads(hbRes)['tick']
        hbRes_sell = hbRes['asks'][0][0]
        hbRes_buy = hbRes['bids'][0][0]


        print ('OKCOIN: sell: %.2f buy: %.2f' % (
            coinRes_sell,
            coinRes_buy))
        print ('HUOBI: buy: %.2f sell: %.2f' % (
            hbRes_buy,
            hbRes_sell))
        print ('OKCOIN: sell: %.2f buy: %.2f' % (
            coinRes_sell,
            coinRes_buy))
        print ('HUOBI: buy: %.2f sell: %.2f' % (
            hbRes_buy,
            hbRes_sell))
        if (hbRes_buy - coinRes_sell > 1.2):
            hb_t = HuobiService.trade(0.1, 'sell-market')
            logging.info(hb_t)
            if (hb_t['status'] != 'ok'):
                logging.info(hb_t['status'])
                exit()
            coin_t = okcoinSpot.trade('etc_cny', 'buy_market', coinRes_sell/10)
            logging.info(coin_t)
            if (str(coin_t['result']) != 'True'):
                logging.info(coin_t['result'])
                exit()

            coin_max = hbRes_buy - coinRes_sell
            message = ('OKCOIN: sell: %.2f buy: %.2f' % (
                coinRes_sell,
                coinRes_buy))
            logging.info(message)

            message = ('HUOBI: buy: %.2f sell: %.2f' % (
                hbRes_buy,
                hbRes_sell))
            logging.info(message)

            message = ('coin max: %.2f' % (
                coin_max))
            logging.info(message)

        if (coinRes_buy - hbRes_sell > 1.2):
            coin_t = okcoinSpot.trade('etc_cny', 'sell_market', 0, '0.1')
            logging.info(coin_t)
            if (str(coin_t['result']) != 'True'):
                logging.info(coin_t['result'])
                exit()
            hb_t = HuobiService.trade(round(hbRes_sell/10, 2), 'buy-market')
            logging.info(hb_t)
            if (hb_t['status'] != 'ok'):
                logging.info(hb_t['status'])
                exit()

            hb_max = coinRes_buy - hbRes_sell
            message = ('OKCOIN: sell: %.2f buy: %.2f' % (
                coinRes_sell,
                coinRes_buy))
            logging.info(message)

            message = ('HUOBI: buy: %.2f sell: %.2f' % (
                hbRes_buy,
                hbRes_sell))
            logging.info(message)

            message = ("hb max: %.2f" % hb_max)
            logging.info(message)
        time.sleep(10)
