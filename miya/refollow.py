# -*- coding: utf-8 -*-

import logging

class Refollow(object):
    
    event_type = 'event'

    def __init__(self): pass

    def __call__(self, api, event_type, status):

        if status.event != 'follow': return
        if status.target.screen_name != api.auth.get_username(): return

        try:
            user = api.get_user(status.source.screen_name)
            user.follow()
            logging.info('follow new user. user=%s' % status.source.screen_name)
        except:
            logging.exception('failed to follow user %s' % status.source.screen_name)
