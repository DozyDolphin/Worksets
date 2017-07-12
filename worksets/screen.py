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
import operator
import collections


class Screen():

    def __init__(self, publisher, wm, db):
        self.logger = logging.getLogger('Screen')
        self.publisher = publisher
        self.wm = wm
        self.db = db
        self.update_screen_config()
        self._active_worksets = []

    def update_screen_config(self):
        self.logger.debug("Aquiring screen configuration (desktops & monitors)")
        self.desktops = self.wm.get_desktops()
        self.monitors = self.sort_monitors(self.wm.get_monitors())

    def update_active_worksets(self):
        if self._active_worksets:
            self.logger.debug("There are active worksets!")
            windows = self.wm.get_windows()
            w_ids = [window.wid for window in windows]
            for workset in self._active_worksets:
                workset.update_and_test_active(w_ids)

            self._active_worksets = [workset for workset
                                     in self._active_worksets
                                     if workset.active is True]
        else:
            self.logger.debug("No active worksets found!")

    def get_active_workset_names(self):
        return [workset.name for workset in self._active_worksets]

    def activate_workset(self, workset_name):
        self.logger.debug(" Looking for workset " + workset_name)
        workset = self.db.get_workset_by_name(workset_name)
        if workset is not None:
            self.logger.debug(" Activating workset " + workset.name)
            workset.activate(self.desktops, self.monitors, self.wm)
            self._active_worksets.append(workset)

    def deactivate_workset(self, workset_name):
        """ Look for workset_name in active_worksets and
           if found, deactivate it.
        """
        for workset in self._active_worksets:
            if workset.name == workset_name:
                workset.deactivate(self.wm)

    def run_app(self, app):
        """ Run application (for test in app_dialog)."""
        self.logger.debug("Running application " + app.name)
        window = self.wm.run_app_and_get_window(app)
        if window is not None:
            self.logger.debug("A window was returned: " + window.information())
            placement = app.get_placement(self.desktops, self.monitors)
            window.move(self.wm, placement)
            self.wm.focus_window(window.wid)

    def run_workset(self, workset):
        """ Run workset (for test in workset_dialog)."""
        self.logger.debug("Activating workset " + workset.name)
        workset.activate(self.desktops, self.monitors)

    def sort_monitors(self, monitors):
        """ Sort monitors so that their placement is numbered upwards
        from top to bottom and left to right relative to their position for the
        user (hopefully)
        """

        monitors_active = [monitor
                           for monitor in monitors
                           if monitor.active is True]

        # Maybe account for multiple cloned screens on 0,0?
        upper_left_monitor_height = [monitor.height
                                     for monitor in monitors_active
                                     if monitor.y == 0 and monitor.x == 0]

        # If the screens upper left corners x position is less than two thirds down from
        # upper_left_monitors height it is counted as being on the same row.
        y_limit = int((upper_left_monitor_height[0] / 3) * 2)
        rows_of_monitors = []

        while monitors_active:
            # Moves all monitors with y position lower than the y_limit to row from monitors_active
            # This can be done simpler in a more straight forward way?
            row = [monitor
                   for index, monitor in enumerate(monitors_active)
                   if monitor.y < y_limit]
            monitors_active = [monitor
                               for monitor in monitors_active
                               if monitor not in row]
            rows_of_monitors.append(row)

            if monitors_active:
                monitors_active = sorted(monitors_active,
                                         key=operator.attrgetter('y', 'x'))
                upper_left_monitor_height = monitors_active[0].height
                upper_left_monitor_position = monitors_active[0].y
                y_limit = (upper_left_monitor_position +
                           int((upper_left_monitor_height / 3) * 2))

        monitor_number = 1
        monitors_sorted = collections.OrderedDict()

        for row in rows_of_monitors:
            row = sorted(row, key=operator.attrgetter('x'))

            for monitor in row:
                monitors_sorted[str(monitor_number)] = monitor
                monitor_number += 1

        for key, monitor in monitors_sorted.items():
            self.logger.info("Nr: " + key +
                             " Name: " + monitor.name +
                             " x: " + str(monitor.x) +
                             " y: " + str(monitor.y))

        return monitors_sorted
