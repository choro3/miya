# -*- coding: utf-8 -*-

import logging
import random
import datetime

import requests
from pyquery import PyQuery as pq

class Tryjpy(object):

    def __init__(self, config):
        self.pattern = ['これでにぃにもがっぽがぽだね！',
                        'にぃには損してない？',
                        '失敗を恐れる心の中にこそ恥辱は住むと知れ',
                        '外国為替証拠金取引は元本や利益が保証された金融商品ではありません。' \
                        '十分に仕組みやリスクをご理解いただき、ご自身の判断にて開始していただくようお願いいたします。',
                        '勝ちに不思議の勝ちあり、負けに不思議の負けなしだよにぃに！',
                        'にぃにのしいたけなんかに絶対負けたりしないから！',
                        '']


    def fetch(self):
        res = requests.get('http://stocks.finance.yahoo.co.jp/stocks/detail/?code=TRYJPY=X')
        d = pq(res.text)
        return [e.text for e in d('.ymuiEditLink.mar0 strong')]

    def __call__(self, api):

        bid, ask = self.fetch()
        text = '%sのトルコリラ円相場だよ！%s %s-%s #TRYJPY' % (
            datetime.datetime.now().strftime('%m月%d日%H時'), 
            random.choice(self.pattern),
            '%.3f' % float(bid),
            '%.3f' % float(ask))
        
        api.update_status(text)
        logging.debug('sent tweet. text=%s' % text)

class ISE(object):
    pass
