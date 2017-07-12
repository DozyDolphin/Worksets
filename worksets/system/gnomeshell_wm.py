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
import os
import time
from collections import namedtuple
from .wmctrl import Wmctrl


class GnomeShellWm():
    ''' This handles system calls on machines with the Ubuntu OS. It relies on wmctrl
        but due to Compiz/Ubuntus special workarounds are implemented:

            * uses dconf to get workspaces and uses this to translate wmctrls
                desktop in relation to Compiz where only one desktop exists.
            * relies on xdo-tool to place windows that are not maximized
            * adjusts for the launcher and top bar when placing windows
    '''

    def __init__(self):
        self.logger = logging.getLogger(' GnomeShellWm ')
        self.wmctrl = Wmctrl()

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
        wmctrl_desktops = self.wmctrl.get_desktops()
        desktops = []
        for wmctrl_desktop in wmctrl_desktops:
            self.logger.debug
            desktop = self._convert_to_desktop(wmctrl_desktop)
            desktops.append(desktop)
        return desktops

    # this should be private in all wm's if not used outside
    def get_current_desktop(self):
        wmctrl_desktop = self.wmctrl.get_current_desktop()
        current_desktop = self._convert_to_desktop(wmctrl_desktop)
        return current_desktop

    def _convert_to_desktop(self, wmctrl_desktop):
        Desktop = namedtuple('Desktop', 'x y width height no')
        workarea = wmctrl_desktop['workarea']
        no = str(int(wmctrl_desktop['desktop_id']) + 1)
        desktop = Desktop(
            workarea.x,
            workarea.y,
            workarea.width,
            workarea.height,
            no)
        return desktop

    def get_windows(self):
        windows = self.wmctrl.get_windows()
        return windows

    def move_window(self, window, new_desktop, placement_type):
        current_desktop = self.get_current_desktop()
        self.logger.debug("Attempting to move  window " + window.title)

        self.wmctrl.remove_vert_and_horz_max(window.wid)
        if current_desktop.no != new_desktop.no:
            new_desktop_id = str(int(new_desktop.no) - 1)
            self.wmctrl.move_window_to_desktop(window, new_desktop_id)

        self.wmctrl.move_window(window)
        self.logger.debug("Windows placement type is: " + placement_type)

    def focus_window(self, window_wid):
        self.logger.debug('Attempting to focus')
        self.wmctrl.focus_window(window_wid)

    def close_window(self, window):
        self.wmctrl.close_window(window)

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

    def get_config_dir(self):
        return '/.config/worksets/'
