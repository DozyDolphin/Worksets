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
    ''' This handles system calls on machines with Gnome-shell. It relies on wmctrl.

    '''

    header_bar_windows = ['evince','nautilus','gnome-tweak-tool']

    def __init__(self):
        self.logger = logging.getLogger(' GnomeShellWm ')
        self.wmctrl = Wmctrl()

    def get_desktops(self):
        wmctrl_desktops = self.wmctrl.get_desktops()
        desktops = []
        for wmctrl_desktop in wmctrl_desktops:
            self.logger.debug
            desktop = self._convert_to_desktop(wmctrl_desktop)
            desktops.append(desktop)
        return desktops

    # this should be private in all wm's if not used outside
    def _get_current_desktop(self):
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
        current_desktop = self._get_current_desktop()
        self.logger.debug("Attempting to move  window " + window.title)

        self.wmctrl.remove_vert_and_horz_max(window.wid)
        if current_desktop.no != new_desktop.no:
            new_desktop_id = str(int(new_desktop.no) - 1)
            self.wmctrl.move_window_to_desktop(window, new_desktop_id)
        self.hack_for_gtk3_windows(window)
        self.wmctrl.move_window(window)
        self.logger.debug("Windows placement type is: " + placement_type)

    def hack_for_gtk3_windows(self, window):
        wm_name = window.wm_class.split('.')
        if wm_name[0] in self.header_bar_windows:
            print("HACK NECESSARY")
            window.x = str(int(window.x) - 25)
            window.y = str(int(window.y) - 25)
            window.width = str(int(window.width) + 50)
            window.height = str(int(window.height) + 25)

    def focus_window(self, window_wid):
        self.logger.debug('Attempting to focus')
        self.wmctrl.focus_window(window_wid)

    def close_window(self, window):
        self.wmctrl.close_window(window)

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
