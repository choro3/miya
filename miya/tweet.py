# -*- coding: utf-8 -*-

import logging

from chatbot import MessageGenerator

class RegularTweet(object):

    def __init__(self, config):
        self.generator = MessageGenerator(**dict(config.items('chatbot')))

    def __call__(self, api):
        try:
            text = self.generator.generate()
            api.update_status(text)
            logging.debug('sent tweet. text=%s' % text)
        except:
            logging.exeption('failed to send tweet.')
