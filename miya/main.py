# -*- coding: utf-8 -*-

import logging
import argparse
import ConfigParser
import datetime
import threading
import time

import tweepy
import croniter

from refollow import Refollow
from reply import Reply
from tweet import RegularTweet
from turkey import Tryjpy

class Bot(object):

    class Listener(tweepy.StreamListener):

        def __init__(self, *args, **kwargs):
            super(Bot.Listener, self).__init__(*args, **kwargs)
            self.handlers = []

        def on_status(self, status):
            self.call_handler('status', status)

        def on_event(self, status):
            self.call_handler('event', status)

        def call_handler(self, event_type, data):
            for handler in self.handlers:
                if handler.event_type == event_type:
                    handler(self.api, event_type, data)

    class Task(object):
        def __init__(self, callable, schedule, bot):
            self.callable = callable
            self.schedule = schedule
            self.bot = bot
        def __call__(self):
            while True:
                next_execution = self.schedule.get_next(datetime.datetime)
                time.sleep((next_execution - datetime.datetime.now()).seconds)
                self.callable(self.bot.api)

    def __init__(self, args):

        self.auth = tweepy.OAuthHandler(args.config.get('token', 'consumer_key'),
                                        args.config.get('token', 'consumer_secret'))
        self.auth.set_access_token(args.config.get('token', 'access_key'),
                                   args.config.get('token', 'access_secret'))

        self.api = tweepy.API(self.auth, api_root='/1.1')

        logging.info('logged in. screen_name=%s' % self.api.auth.get_username())

        self.listener = Bot.Listener(api=self.api)
        self.tasks = []

    def add_handler(self, handler):
        self.listener.handlers.append(handler)
        logging.debug('added userstream event handler: %s' % handler.__class__.__name__)

    def add_schedule(self, task, schedule):
        scheduler = croniter.croniter(schedule, datetime.datetime.now())
        self.tasks.append(threading.Thread(name='thread-%s' % task.__class__.__name__,
                                           target=Bot.Task(task, scheduler, self)))

    def _start_scheduled_tasks(self):
        for task in self.tasks:
            task.setDaemon(True)
            task.start()
            logging.debug('task %s is now running.' % task.name)

    def run(self):

        self._start_scheduled_tasks()

        stream = tweepy.Stream(self.auth, self.listener, secure=True)
        stream.userstream(async=True)

        logging.info('thread started.')

        try:
            while stream.running: time.sleep(1)
        except KeyboardInterrupt:
            logging.info('caught signal. now exiting...')
            stream.disconnect()

        logging.info('exit')

def main(args):

    logging.basicConfig(filename=args.logfile,
                        level=logging.DEBUG,
                        format='[%(asctime)s] %(module)s %(levelname)s %(message)s')

    logging.info('initializing...')

    args.config = ConfigParser.SafeConfigParser()
    args.config.read(args.conf)

    bot = Bot(args)

    bot.add_handler(Refollow())
    bot.add_handler(Reply())

    bot.add_schedule(RegularTweet(args.config),
                     args.config.get('schedule', 'RegularTweet'))
    bot.add_schedule(Tryjpy(args.config),
                     args.config.get('schedule', 'Tryjpy'))

    bot.run()

def console_script():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', default='app.conf')
    parser.add_argument('--logfile', default='app.log')

    main(parser.parse_args())

if __name__ == '__main__':
    console_script()
