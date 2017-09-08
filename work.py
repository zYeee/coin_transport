# coding=utf-8

from huobi import HuobiService
from okcoin.OkcoinSpotAPI import OKCoinSpot
import json
import time
import logging

apikey = 'XXXX'
secretkey = 'XXXXX'
okcoinRESTURL = 'www.okcoin.cn'

if __name__ == "__main__":
    logging.basicConfig(filename='/usr/share/nginx/html/log.html', filemode='w', level=logging.INFO,
                        format='%(asctime)s %(message)s')

    okcoinSpot = OKCoinSpot(okcoinRESTURL, apikey, secretkey)
    coin_max = hb_max = 0
    while (True):
        coinRes = okcoinSpot.depth('etc_cny')
        coinRes_sell = coinRes['asks'][-1][0]
        coinRes_buy = coinRes['bids'][0][0]

        hbRes = HuobiService.getDepth()
        hbRes = json.loads(hbRes)['tick']
        hbRes_sell = hbRes['asks'][0][0]
        hbRes_buy = hbRes['bids'][0][0]

        if (hbRes_buy - coinRes_sell > coin_max or hbRes_buy - coinRes_sell >= 0.8):
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

        if (coinRes_buy - hbRes_sell > hb_max or coinRes_buy - hbRes_sell >= 0.8):
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
        time.sleep(1)
