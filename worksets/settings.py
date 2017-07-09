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
import locale
import gettext
import collections
import configparser
import os
from .logger import Logger


class Settings():

    WORKSETS_VERSION = '0.1'

    def __init__(self, publisher, wm):
        self.LOCALE_DIR = 'locale'

        self.CONFIG_DIR = wm.get_config_dir()
        self.SETTINGS_FILE = self.CONFIG_DIR + 'settings.cfg'
        self.USER_HOME = wm.get_user_home()

        self.language = 'System locale'
        self.script_dir = self.USER_HOME
        self.db_dir = self.CONFIG_DIR + 'db'
        self.log_dir = self.CONFIG_DIR + 'logs'
        self.log_enabled = True
        self.log_to_console = False
        self.log_level = 'DEBUG'

        if not os.path.isfile(self.SETTINGS_FILE):
            print("Settings file doesn't exist... creating.")
            self.initial_setup()
        else:
            print("Settings file exists... loading.")
            self.load_cfg()

        self.log_control = Logger(self.log_dir,
                                  self.log_level,
                                  self.log_enabled,
                                  self.log_to_console)
        self.logger = logging.getLogger('Settings')
        self.initiate_I18N()

    def initial_setup(self):
        dirs = [self.CONFIG_DIR, self.log_dir, self.db_dir]
        for directory in dirs:
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except IOError as e:
                print("Couldn't create directory " + directory + ": " + str(e))
                # SYSTEM EXIT
        self.write_cfg()

    def write_cfg(self):
        config = configparser.ConfigParser()
        config.add_section('Settings')
        config.set('Settings', 'language', self.language)
        config.set('Settings', 'script_dir', self.USER_HOME)
        config.set('Settings', 'db_dir', self.db_dir)
        config.set('Settings', 'log_dir', self.log_dir)
        config.set('Settings', 'log_enabled', str(self.log_enabled))
        config.set('Settings', 'log_to_console', str(self.log_to_console))
        config.set('Settings', 'log_level', self.log_level)

        try:
            with open(self.SETTINGS_FILE, 'w') as configfile:
                config.write(configfile)
        except IOError as e:
            print("Couldn't ẃrite config file: " + str(e))
            # SYSTEM EXIT

    def load_cfg(self):
        config = configparser.RawConfigParser()
        try:
            config.read(self.SETTINGS_FILE)
        except IOError as e:
            print("Couldn't read config file: " + str(e))
        try:
            self.language = config.get('Settings', 'language')
            self.script_dir = config.get('Settings', 'script_dir')
            self.db_dir = config.get('Settings', 'db_dir')
            self.log_dir = config.get('Settings', 'log_dir')
            self.log_enabled = config.getboolean('Settings', 'log_enabled')
            self.log_to_console = config.getboolean('Settings', 'log_to_console')
            self.log_level = config.get('Settings', 'log_level')
        except (configparser.MissingSectionHeaderError,
                configparser.NoSectionError,
                configparser.NoOptionError) as e:
            print("The settings file seems to be corrupted: " + e)
            print("Replacing settings file... ")
            #CLEAN UP, SO THAT INITIAL SETUP TESTS THAT FOR FOLDERS AND FILES
            self.initial_setup()

    def initiate_I18N(self):
        default_locale, encoding = locale.getdefaultlocale()
        self.available_languages = collections.OrderedDict()
        self.available_languages['System locale'] = default_locale
        self.available_languages['Dansk'] = 'da_DK'
        self.available_languages['English'] = 'en_US'
        gettext.install('worksets', self.LOCALE_DIR)
        self.change_language(self.language)

    def change_language(self, language_name):
        lang_code = self.available_languages[language_name]
        language = gettext.translation('worksets', self.LOCALE_DIR, languages=[lang_code])
        language.install()

    def save_settings(self, settings_data):
        if not self.language == settings_data['language']:
            print('language has been changed - updating...')
            self.language = settings_data['language']
            self.change_language(self.language)
        self.script_dir = settings_data['script_dir']
        self.log_enabled = bool(settings_data['log_enabled'])
        self.log_to_console = bool(settings_data['log_to_console'])
        self.log_level = settings_data['log_level']
        self.log_dir = settings_data['log_dir']
        self.log_control.reload_logger(self.log_dir, self.log_level, self.log_enabled, self.log_to_console)
        self.write_cfg()

    def get_log_levels(self):
        return self.log_control.loglevels