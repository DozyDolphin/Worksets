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
from collections import namedtuple
from worksets.window import Window


class Wmctrl():
    '''This is an incomplete Wmctrl interface in python, having only
       the features implemented needed for Unity worksets'''

    def __init__(self):
        self.logger = logging.getLogger(' Wmctrl')
        self.app = 'wmctrl'
        self.Geometry = namedtuple('Geometry', 'x y width height')
        self.Coordinates = namedtuple('Coordinates', 'x y')
        self.Dimensions = namedtuple('Dimensions', ' width height')

    def get_wm_and_env_info(self):
        param = '-m'
        output = subprocess.getoutput(self.app + param)
        wm_and_environment = self._parse_wm_and_env_info(output)
        return wm_and_environment

    def _parse_wm_and_env_info(self, input):
        wm_and_environment = {}
        input_lines = input.split('\n')

        for line in input_lines:
            key, value = line.split(':', 1)
            if key == 'Window manager\'s "showing the desktop" mode':
                key = "show_desktop_mode"
            wm_and_environment[key.lower()] = value.lstrip()

        return wm_and_environment

    def get_windows(self):
        argument = '-l'
        options = '-pGx'
        out = subprocess.Popen(
            [self.app, argument, options], stdout=subprocess.PIPE)
        output_bytecode = out.stdout.read()
        output = output_bytecode.decode()
        output = output[2:-1]
        windows = self.parse_window_output(output)
        return windows

    def parse_window_output(self, window_input):
        windows = []
        input_lines = window_input.split('\n')

        for line in input_lines:
            raw = line.split(' ')
            interm = [i for i in raw if i != '']
            title_list = interm[9:]
            title = ' '.join(title_list)

            clean = interm[:9]
            clean.append(title)
            attributes = {}
            keys = ['window_id', 'desktop_id', 'pid', 'x', 'y', 'width',
                    'height', 'wm_class', 'client_machine', 'title']

            for i, value in enumerate(keys):
                attributes[value] = clean[i]

            window = Window(
                attributes['window_id'],
                attributes['pid'],
                # desktop_id should be set later with desktop object
                attributes['desktop_id'],
                attributes['wm_class'],
                attributes['title'],
                attributes['client_machine'],
                attributes['x'],
                attributes['y'],
                attributes['width'],
                attributes['height'])
            windows.append(window)

        return windows

    def get_desktops(self):
        desktops = []
        output = self._get_desktops_raw()
        desktop_strings = output.split('\n')
        for desktop_string in desktop_strings:
            desktop = self._parse_desktop_string(desktop_string)
            desktops.append(desktop)
        return desktops

    def _get_desktops_raw(self):
        param = ' -d'
        output = subprocess.getoutput(self.app + param)
        return output

    def _parse_desktop_string(self, desktop_string):

        desktop = {}
        raw_list = desktop_string.split(' ')
        clean = [i for i in raw_list if i != '']
        self.logger.debug('desktop_string som clean list er: ' + str(clean))
        wa_sizes = [
            int(wa_size)
            for wa_size in clean[8].split('x')]
        wa_width, wa_height = wa_sizes

        wa_coordinates = [
            int(wa_coordinate)
            for wa_coordinate in clean[7].split(',')]
        wa_x, wa_y = wa_coordinates
        workarea = self.Geometry(wa_x, wa_y, wa_width, wa_height)

        if clean[5] == 'N/A':
            vp_x, vp_y = [0, 0]
        else:
            vp_coordinates = [
                int(coordinate)
                for coordinate in clean[5].split(',')]
            vp_x, vp_y = vp_coordinates
        viewport = self.Coordinates(vp_x, vp_y)

        dg_sizes = [
            int(dg_size)
            for dg_size in clean[3].split('x')]
        dg_width, dg_height = dg_sizes
        # This doesn't take into account if multiple desktops - which
        # doesn't exist in unity - has a coordinate. This will lead to
        # unexpected behaviour if that is the case.

        desktop_geometry = self.Geometry(0, 0, dg_width, dg_height)

        if len(clean) > 9:
            if len(clean) == 10:
                title = clean[9]
            elif len(clean) == 11:
                title = clean[9] + ' ' + clean[10]
        else:
            title = ''

        desktop['title'] = title
        desktop['workarea'] = workarea
        desktop['viewport'] = viewport
        desktop['desktop_geometry'] = desktop_geometry
        desktop['desktop_id'] = clean[0]

        return desktop

    def switch_to_desktop(self, desktop_id):
        argument = '-s'
        parameters = desktop_id
        subprocess.Popen([self.app, argument, parameters],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE)

    # Should be renamed to change_wiewport (and reflected in unity_wm)
    def move_to_desktop(self, desktop):
        argument = '-o'
        parameters = str(desktop.x) + ',' + str(desktop.y)
        subprocess.Popen([self.app, argument, parameters],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE)

    def move_window(self, window):
        gravity = '0'
        position = (
            gravity + ',' +
            str(window.x) + ',' +
            str(window.y) + ',' +
            str(window.width) + ',' +
            str(window.height))

        subprocess.Popen(
            [self.app, '-i', '-r', window.wid, '-e', position],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

    def move_window_to_desktop(self, window, desktop_id):
        subprocess.Popen(
            [self.app, '-i', '-r', window.wid, '-t', desktop_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

    def focus_window(self, window_wid):
        self.logger.debug('calling wmctrl with command: ')
        self.logger.debug('wmctrl -i -a ' + window_wid)
        subprocess.Popen(
            [self.app, '-i', '-a', window_wid],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

    def close_window(self, window):
        subprocess.Popen(
            [self.app, '-i', '-c', str(window.wid)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

    def remove_vert_and_horz_max(self, wid):
        is_vert_maxed = subprocess.Popen(
            ['xprop', '-id', wid, '|', 'grep', '-q', '_NET_WM_STATE_MAXIMIZED_VERT'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

        is_horz_maxed = subprocess.Popen(
            ['xprop', '-id', wid, '|', 'grep', '-q', '_NET_WM_STATE_MAXIMIZED_VERT'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

        if is_vert_maxed:
            self.logger.debug('window was vertically maximized ...removing')
        subprocess.Popen(
            [self.app, '-i', '-r', wid, '-b', 'remove,maximized_vert'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

        if is_horz_maxed:
            self.logger.debug('window was horizontically maximized ...removing')   
            subprocess.Popen(
                [self.app, '-i', '-r', wid, '-b', 'remove,maximized_horz'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)

    def add_vert_max(self, wid):
        subprocess.Popen(
            [self.app, '-i', '-r', wid, '-b', 'add,maximized_vert'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

    def add_horz_max(self, wid):
        subprocess.Popen(
            [self.app, '-i', '-r', wid, '-b', 'add,maximized_horz'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

    def get_current_desktop(self):
        '''Find the desktop marked with an * in the output of wmctrl -d'''
        current_desktop = None
        desktop_output = self._get_desktops_raw()
        desktop_strings = desktop_output.split('\n')
        for desktop_string in desktop_strings:
            if '*' in desktop_string:
                current_desktop = self._parse_desktop_string(desktop_string)
        return current_desktop
