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
import platform
import os
import time


class Wm():

    def __init__(self, publisher):
        self.logger = logging.getLogger(' Wm')
        self.publisher = publisher
        operating_system = platform.system().lower()
        desktop_env = os.environ['XDG_CURRENT_DESKTOP'].lower()

        if operating_system == 'linux':
            if desktop_env == 'unity':
                from .unitywm import UnityWm as WmImpl
            if desktop_env == 'gnome' or desktop_env == 'gnome-classic:gnome':
                from .gnomeshell_wm import GnomeShellWm as WmImpl

        try:
            self._wm = WmImpl()
        except NameError:
            message_list = ['Desktop Environment not supported.',
                            'You seem to be running the %s desktop environment. Unfortunately, at the moment only the Unity desktop environment is supported.\n\n The application will terminate.' % desktop_env.title(),
                            '',
                            'Critical',
                            True]
            self.publisher.user_message('MESSAGE', message_list)
            self.logger.critical(message_list[0] + ' ' + message_list[1])

    def get_monitors(self):
        return self._wm.get_monitors()

    def get_desktops(self):
        return self._wm.get_desktops()

    def get_current_desktop(self):
        return self._wm.get_current_desktop()

    def get_workspaces(self):
        return self._wm.get_workspaces()

    def get_windows(self):
        return self._wm.get_windows()

    def get_window(self):
        return self._wm.get_window()

    def focus_window(self, window_wid):
        self._wm.focus_window(window_wid)

    def run_app(self, app):
        self._wm.run_app(app)

    def move_window(self, window, placement, placement_type):
        self._wm.move_window(window, placement, placement_type)

    def close_window(self, window):
        self._wm.close_window(window)

    def get_user_home(self):
        home = os.path.expanduser('~')
        return home

    def get_config_dir(self):
        return self.get_user_home() + self._wm.get_config_dir()

    def test_executable(self, executable):
        return self._wm.test_executable(executable)


    def run_app_and_get_window(self, app):
        windows_before = self.get_windows()
        window = None
        pid = self.run_app(app)

        if app.uses_existing_window:
            self.logger.debug("Looking for existing window.")
            window = self._if_uses_existing_window(windows_before, pid, app)
            if window is not None:
                self.logger.debug('...found existing window: ' + window.title)
                return window

        time.sleep(0.5)
        times = 0
        while times <= 10:
            self.logger.debug("LOOP RUNNING... " + str(times))
            windows = self.get_windows()
            if len(windows) > len(windows_before):
                self.logger.debug("Found new windows.")
                new_windows = self._extract_new_windows(windows_before,
                                                        windows)
                for new_window in new_windows:
                    self.logger.debug("Testing the found windows")
                    window = self._test_window(pid, new_window, app)
                    if window is not None:
                        self.logger.debug('Found the window for the application: ' + window.information())
                        break

                if window is not None:
                    if app.has_splash:
                        window = self._if_splash(window, pid, app)
                    break
                else:
                    self.logger.debug("A window appeared but it wasn't the right one")

            else:
                self.logger.debug('No new windows!')
            windows = []
            times += 1
            time.sleep(1)

        return window

    def _extract_new_windows(self, windows_before, windows):
        windows_new = []

        for window in reversed(windows):
            uniqueness = True
            for window_before in reversed(windows_before):
                if window.wid == window_before.wid:
                    uniqueness = False
            if uniqueness is True:
                windows_new.append(window)

        return windows_new

    def _test_window(self, pid, window, app):
        self.logger.debug('testing the window...')
        certainty = 0
        chosen_window = None
        if not window.wm_class == 'N/A':
            wm_name = window.wm_class.split('.')[1].lower()
            if (wm_name == app.executable.lower() and
               window.wm_class.split('.')[0].lower() != 'desktop_window'):
                certainty += 1
                self.logger.debug("window name matched: +1 certainty")

        if app.executable.lower() in window.title.lower():
            certainty += 1
            self.logger.debug("window title matched: +1 certainty")

        if window.pid == str(pid):
            certainty += 1
            self.logger.debug("PID matched: +1 certainty")

        if certainty >= 1 or self._test_for_edge_cases(window, app) is True:
            self.logger.debug('returning window')
            chosen_window = window

        return chosen_window

    def _test_for_edge_cases(self, window, app):
        self.logger.debug('testing for edge cases...')
        libre_office = ['lowriter', 'localc', 'lodraw']

        if app.executable in libre_office:
            if (window.pid == '0' and
               window.title == 'LibreOffice' and
               app.has_splash is True):
                self.logger.debug('found Libre Office Splash Screen')
                return True
            if (window.pid != '0' and
               'libreoffice' in window.title.lower()):
                self.logger.debug('found Libre Office Window')
                return True

    def _if_uses_existing_window(self, windows, pid, app):
        chosen_window = None
        for window in reversed(windows):
            chosen_window = self._test_window(pid, window, app)
            if chosen_window is not None:
                break
        return chosen_window

    def _if_splash(self, splash, pid, app):
        self.logger.debug('Testing for splash screen...')
        amount_to_sleep = 0.5
        times = 0
        chosen_window = None

        while times <= 20:
            self.logger.debug("\n")
            self.logger.debug("if_splash LOOP RUNNING... " + str(times))
            windows = self.get_windows()

            for window in reversed(windows):
                if window.wid == splash.wid:
                    self.logger.debug('Still splash screen!')
                    break
                else:
                    self.logger.debug("Window found: " + window.information())
                    chosen_window = self._test_window(pid, window, app)
                    if chosen_window is not None:
                        break
            if chosen_window is not None:
                self.logger.debug('A matching window that is not the splash screen has been found')
                break
            times += 1
            time.sleep(amount_to_sleep)

        return chosen_window
