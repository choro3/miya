# -*- coding: utf-8 -*-

import logging
import random
import cPickle

# TODO: 

class MessageGenerator(object):
    def __init__(self, **kwargs):
        self.dic = cPickle.load(open(kwargs['dictionary']))
    def generate(self, n=3, term='EOS'):
        res = ''
        cur = ''
        while True:
            try:
                cur = random.choice(self.dic[cur])
            except KeyError:
                return res
            if cur == term: break
            res += cur
            cur = res[-n:]
        return res
        
if __name__ == '__main__':
    pass
