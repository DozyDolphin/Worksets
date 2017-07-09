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
import sys
import traceback
from logging.handlers import TimedRotatingFileHandler


class Logger():

    loglevels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    def __init__(self, log_dir, log_level, log_enabled, log_to_console):
        self.logname = 'worksets.log'
        self.load_logger(log_dir, log_level, log_enabled, log_to_console)
        self.logger.info("Worksets started and logging enabled")

    def load_logger(self, log_dir, log_level, log_enabled, log_to_console):
        path = log_dir + '/' + self.logname
        self.logger = logging.getLogger()

        formatter = logging.Formatter('%(asctime)s %(levelname)s (%(name)s): %(message)s',
                                      '%d/%m/%Y %H:%M:%S')
        file_handler = TimedRotatingFileHandler(path,
                                                when='d',
                                                interval=1,
                                                backupCount=6)

        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        self.set_loglevel(log_level)
        self.log_enabled(log_enabled)

    def log_enabled(self, enabled):
        if enabled is True:
            logging.disable(logging.NOTSET)
            self.logger.debug("Logging enabled")
            sys.excepthook = self.handle_uncaught_exception
        elif enabled is False:
            self.logger.debug("Logging disabled")
            logging.disable(logging.CRITICAL)
            sys.excepthook = sys.excepthook

    def reload_logger(self, log_dir, log_level, log_enabled, log_to_console):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        self.load_logger(log_dir, log_level, log_enabled, log_to_console)

    def set_loglevel(self, level):
        if level == 'DEBUG':
            self.logger.info("Log level set to DEBUG")
            self.logger.setLevel(logging.DEBUG)
        elif level == 'INFO':
            self.logger.info("Log level set to INFO")
            self.logger.setLevel(logging.INFO)
        elif level == 'WARNING':
            self.logger.info("Log level set to WARNING")
            self.logger.setLevel(logging.WARNING)
        elif level == 'ERROR':
            self.logger.info("Log level set to ERROR")
            self.logger.setLevel(logging.ERROR)
        elif level == 'CRITICAL':
            self.logger.info("Log level set to CRITICAL")
            self.logger.setLevel(logging.CRITICAL)

    def handle_uncaught_exception(self, exc_type, exc_value, exc_traceback):
        message = ('An uncaught exception occured ' +
                   '- please report to Worksets on GITHUB \n' +
                   str(exc_type) + '\n' +
                   str(exc_value) + '\n' +
                   ''.join(traceback.format_tb(exc_traceback)))
        self.logger.critical(message)
