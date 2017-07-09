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


class UnityWm():
    ''' This handles system calls on machines with the Ubuntu OS. It relies on wmctrl
        but due to Compiz/Ubuntus special workarounds are implemented:

            * uses dconf to get workspaces and uses this to translate wmctrls
                desktop in relation to Compiz where only one desktop exists.
            * relies on xdo-tool to place windows that are not maximized
            * adjusts for the launcher and top bar when placing windows
    '''

    def __init__(self):
        self.logger = logging.getLogger(' UnityWm ')
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
        Desktop = namedtuple('Desktop', 'x y width height no')
        desktops = []

        wmctrl_desktops = self.wmctrl.get_desktops()
        workspaces = self.get_workspaces()
        wmctrl_desktop = wmctrl_desktops[0]

        desktop_geometry = wmctrl_desktop['desktop_geometry']
        width = desktop_geometry.width // workspaces.horz
        height = desktop_geometry.height // workspaces.vert

        x = 0
        y = 0
        no = 1
        for workspace in range(workspaces.vert):
            for workspace in range(workspaces.horz):

                desktop = Desktop(
                    x,
                    y,
                    width,
                    height,
                    no)
                # Add
                desktops.append(desktop)
                x += width
                no += 1

            x = 0
            y += height

        return desktops

    def get_current_desktop(self):
        current_desktop_coordinates = self.wmctrl.get_desktops()[0]['viewport']
        current_x = current_desktop_coordinates.x
        current_y = current_desktop_coordinates.y
        desktops = self.get_desktops()
        for desktop in desktops:
            if (desktop.x == current_x and desktop.y == current_y):
                current_desktop = desktop

        return current_desktop

    def get_workspaces(self):
        Workspaces = namedtuple('Workspaces', 'horz vert total')
        dconf_horz = 'dconf read /org/compiz/profiles/unity/plugins/core/hsize'
        dconf_vert = 'dconf read /org/compiz/profiles/unity/plugins/core/vsize'

        workspaces_horz = int(subprocess.getoutput(dconf_horz))
        workspaces_vert = int(subprocess.getoutput(dconf_vert))
        workspaces_total = int(workspaces_vert) * int(workspaces_horz)
        workspaces = Workspaces(
            workspaces_horz,
            workspaces_vert,
            workspaces_total)

        return workspaces

    def get_windows(self):
        windows = self.wmctrl.get_windows()
        return windows

    def get_window(self):
        pass

    def move_window(self, window, new_desktop, placement_type):
        current_desktop = self.get_current_desktop()
        self.logger.debug("Attempting to move  window " + window.title)

        self.xdo_activate_window(window.title)
        self.wmctrl.remove_vert_and_horz_max(window.wid)
        if current_desktop.no != new_desktop.no:
            self.logger.debug("Moving viewport to desktop " + str(new_desktop.no))
            self.wmctrl.move_to_desktop(new_desktop)

        self.wmctrl.move_window(window)
        self.logger.debug("Windows placement type is: " + placement_type)

        if (placement_type == 'M' or
           placement_type == 'L' or
           placement_type == 'R' or
           placement_type == 'OTL' or
           placement_type == 'TTL' or
           placement_type == 'OTR' or
           placement_type == 'TTR'):
            self.logger.debug("adding vertical max to window.")
            self.wmctrl.add_vert_max(window.wid)

        if (placement_type == 'M' or
           placement_type == 'T' or
           placement_type == 'B'):
            self.logger.debug("adding horizontal max to window.")
            self.wmctrl.add_horz_max(window.wid)

        if placement_type != 'M':
            xdo_key = self.get_xdokey(placement_type)
            if xdo_key is not None:
                self.logger.debug('Using xdotool to place window - xdo_key is: ' + xdo_key)
                self.xdo_with_os(xdo_key)

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

    def get_xdokey(self, placement_type):
        return {
            'M': 'KP_Begin',
            'T': 'KP_Up',
            'B': 'KP_Down',
            'UL': 'KP_Home',
            'L': 'KP_Left',
            'LL': 'KP_End',
            'UR': 'KP_Prior',
            'R': 'KP_Right',
            'LR': 'KP_Next',
            'OTL': None,
            'TTL': None,
            'OTR': None,
            'TTR': None
        }[placement_type]

    def xdo_press_key(self, xdo_key):
        self.logger.debug("Uses xdotool, sets modifiers...")
        subprocess.Popen(
            ['xdotool', 'keydown', '--clearmodifiers', 'ctrl+alt'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)
        self.logger.debug("Uses xdotool, presses key...")
        subprocess.Popen(
            ['xdotool', 'key', xdo_key],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)
        self.logger.debug("Uses xdotool, clears modifiers...")
        subprocess.Popen(
            ['xdotool', 'keyup', 'ctrl+alt'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

    def xdo_with_os(self, xdo_key):
        os.system('xdotool keydown --clearmodifiers ctrl+alt')
        os.system('xdotool key ' + xdo_key)
        os.system('xdotool keyup ctrl+alt')

    def xdo_activate_window(self, window_name):
        self.logger.debug('Using xdotool to activate window')
        os.system('xdotool search --name "' + window_name + '" windowactivate')

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
