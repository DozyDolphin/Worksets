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

from . import placement_factory


class App():

    """App class docstring.

    App class provides an object to hold the data for an application. 
    Holds methods to get the full command (executable and parameters)
    and to convert the placement string to a named tuple.

    """

    def __init__(self,
                 name,
                 placement_str,
                 executable,
                 parameters='',
                 creates_window=True,
                 has_splash=False,
                 uses_existing_window=False):
        self.name = name
        self.executable = executable
        self.parameters = []
        if parameters:
            self.parameters = parameters.split(' ')
        self.creates_window = creates_window
        self.has_splash = has_splash
        self.uses_existing_window = uses_existing_window
        self.placement_desktop, self.placement_monitor, self.placement_type = placement_str.split('.')

    def get_full_cmd_as_list(self):
        cmd = [self.executable] + self.parameters
        return cmd

    def get_placement(self, desktops, monitors):
        """A leftover from the initial cli program is that
           placement is of windows is given as a string in the format [desktop].[monitor].[placementtype].
           This needs to be converted to the actual desktops and monitors during use."""
        desktop = next((
            desktop
            for desktop in desktops
            if str(desktop.no) == self.placement_desktop),
            None)

        monitor = monitors.get(self.placement_monitor)

        placement = placement_factory.create(
            self.placement_type,
            desktop,
            monitor)

        return placement
