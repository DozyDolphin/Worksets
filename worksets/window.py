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


class Window():

    """Window class docstring.

    Window class provides an object to hold window data from wmctrl
    regarding a single window. Holds methods to move and close the window.

    """

    def __init__(self,
                 wid,
                 pid,
                 on_desktop,
                 wm_class,
                 title,
                 client_machine,
                 x,
                 y,
                 width,
                 height):
        self.logger = logging.getLogger(' Window')
        self.wid = wid
        self.pid = pid
        self.on_desktop = on_desktop
        self.wm_class = wm_class
        self.title = title
        self.client_machine = client_machine
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move(self, wm, placement):
        """Set coordinates and width and moves
           the window in accordance with the placement tuple.
        """
        self.x = placement.x
        self.y = placement.y
        self.width = placement.width
        self.height = placement.height
        wm.move_window(self, placement.desktop, placement.type)

    def close(self, wm):
        """Terminate the application gracefully
           (and thereby close the window).
        """
        self.logger.debug("Closing window: " + self.information())
        wm.close_window(self)

    def information(self):
        position = ("(" + str(self.x) + ", " +
                    str(self.y) + ", " +
                    str(self.width) + ", " +
                    str(self.height) + ")")
        window_info = ("Window id: " + self.wid +
                       " Process id: " + self.pid +
                       " Position: " + position +
                       " wm_class: " + self.wm_class +
                       " Window title: " + self.title)
        return window_info
