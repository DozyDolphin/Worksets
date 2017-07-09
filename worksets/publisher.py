'''
Copyright 2017 Anders Lykke Gade

This file is part of Worksets.

Worksets is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Worksets is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Worksets.  If not, see <http://www.gnu.org/licenses/>.
'''

import logging
import collections


class Publisher:

    def __init__(self, events):
        self.logger = logging.getLogger('Publisher')
        self.subscribers = {event: {}
                            for event in events}
        self.logger.info('Publisher initiated')

    def get_subscribers(self, event):
        return self.subscribers[event]

    def register(self, events, subscriber, callback=None):
        if callback is None:
            callback = getattr(subscriber, 'update')
        for event in events:
            self.get_subscribers(event)[subscriber] = callback

    def unregister(self, events, subscriber):
        for event in events:
            del self.get_subscribers(event)[subscriber]

    def dispatch(self, event, message):
        self.logger.debug("Dispatching event " + event + " with message: " + message)
        for subscriber, callback in self.get_subscribers(event).items():
            callback(message)

    def user_message(self, event, message_list):
        '''
        event = 'MESSAGE'
        message_list = [text, informative_text, detailed_text, message_type]
            messagetype corresponds to possible icons for the QMessageBox:
                Question, Information, Warning, Critical
        '''
        for subscriber, callback in self.get_subscribers(event).items():
            callback(message_list)
