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
import subprocess
import platform
import os
import time
from collections import namedtuple
from .wmctrl import Wmctrl


class Wm():

    def __init__(self, publisher):
        self.logger = logging.getLogger(' Wm')
        self.publisher = publisher
        self.wmctrl = Wmctrl()

        operating_system = platform.system().lower()
        wm_name = self.wmctrl.get_wm_and_env_info()['name'].lower()
        print("wm_name is: " + wm_name)
        try:
            desktop_env = os.environ['XDG_CURRENT_DESKTOP'].lower()
        except KeyError:
            self.logger.debug("XDG_CURRENT_DESKTOP variable isn't set - using wmctrl name")
            desktop_env = wm_name

        if operating_system == 'linux':
            if desktop_env == 'unity':
                from .unity_wm import UnityWm as WmImpl
            if desktop_env == 'gnome' or desktop_env == 'gnome-classic:gnome' or wm_name == 'gnome shell':
                from .gnomeshell_wm import GnomeShellWm as WmImpl
            if desktop_env == 'openbox':
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
        output = subprocess.getoutput("xrandr -q | grep ' connected'")
        monitors = self._parse_xrandr_output(output)
        return monitors

    def _parse_xrandr_output(self, input):
        monitors = []
        input_lines = input.split('\n')
        Monitor_active = namedtuple(
            'Monitor_active',
            'name connected active primary x y width height phys_width phys_height')
        Monitor_inactive = namedtuple(
            'Monitor_inactive',
            'name connected active')

        for line in input_lines:
            raw = line.split(' ')
            index_of_geometry = 2

            name = raw[0]
            active = False
            connected = False
            primary = False

            if raw[1] == 'connected':
                connected = True

                if raw[2] == 'primary':
                    primary = True
                    index_of_geometry += 1

            if '(' not in raw[index_of_geometry]:
                active = True
                geometry_raw = raw[index_of_geometry].split('+')
                dimensions_raw = geometry_raw[0].split('x')
                x = int(geometry_raw[1])
                y = int(geometry_raw[2])
                width = int(dimensions_raw[0])
                height = int(dimensions_raw[1])
                phys_width = int(raw[-3][:-2])
                phys_height = int(raw[-1][:-2])

            if active:
                monitor = Monitor_active(
                    name,
                    connected,
                    active,
                    primary,
                    x,
                    y,
                    width,
                    height,
                    phys_width,
                    phys_height)
            if not active:
                monitor = Monitor_inactive(name, connected, active)
            # Sort monitors here
            monitors.append(monitor)
        return monitors

    def get_desktops(self):
        return self._wm.get_desktops()

    # Is this used outside?
    #def get_current_desktop(self):
    #    return self._wm.get_current_desktop()

    # Is this used outside?
    # def get_workspaces(self):
    #   return self._wm.get_workspaces()

    def get_windows(self):
        return self._wm.get_windows()

    def focus_window(self, window_wid):
        self._wm.focus_window(window_wid)

    def move_window(self, window, placement, placement_type):
        self._wm.move_window(window, placement, placement_type)

    def close_window(self, window):
        self._wm.close_window(window)

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

    def run_app(self, app):
        full_cmd_list = None

        if app.parameters:
            full_cmd_list = app.get_full_cmd_as_list()
        else:
            full_cmd_list = [app.executable]
        self.logger.debug("Trying to execute application: " + str(full_cmd_list))
        pid = subprocess.Popen(full_cmd_list,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE).pid
        self.logger.debug("Pid returned: " + str(pid))
        return pid

    def test_executable(self, executable):
        output = subprocess.run(['which', executable],
                                stdout=subprocess.PIPE).stdout.decode('utf-8')
        self.logger.debug("Executable test returned: " + output)
        if output == '':
            return False
        else:
            return True

    def get_user_home(self):
        home = os.path.expanduser('~')
        return home

    def get_config_dir(self):
        return self.get_user_home() + '/.config/worksets/'
