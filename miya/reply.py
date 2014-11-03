# -*- coding: utf-8 -*-

import logging
import datetime

class Reply(object):
    
    event_type = 'status'

    def __init__(self): pass

    def __call__(self, api, event_type, status):

        def is_mention(status):
            return status.text.startswith('@%s ' % api.auth.get_username())

        if is_mention(status):
            try:
                text = datetime.datetime.now().isoformat()
                api.update_status('@%s %s' % (status.user.screen_name, text),
                                  in_reply_to_status_id=status.id)
                logging.debug('sent reply message. target=%s text=%s' % (
                    status.user.screen_name, text))
            except:
                logging.exception('failed to send tweet.')
