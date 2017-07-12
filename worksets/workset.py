"""
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
"""

import logging
import subprocess
import time


class Workset():

    """Workset class docstring.

    A Workset can either be active or inactive. When activated it will run
    all applications contained in the apps attribute and place the windows
    according to their specified location - these windows will be held in the
    windows attribute. When deactivated all windows that the set administrates
    will be closed gracefully and removed from the windows attribute.

    Worksets are configured and saved by the user or read from the db at launch
    if already configured. They are held by the Screen which administrates
    them.

    """

    def __init__(self, name, apps=[], init_script='', db_eid=None):
        self.logger = logging.getLogger('Workset')
        self.active = False
        self.db_eid = -1
        self.name = name
        self.init_script = init_script
        self.apps = apps
        if db_eid is not None:
            self.db_eid = db_eid
        self.windows = []

    def activate(self, desktops, monitors, wm):
        """ Activates the set by running all apps contained in self.apps,
            and placing them on the Screen according to their specified
            location. If the set has an init script this will be run first.
        """
        self.logger.debug("Activating workset " + self.name)
        if self.init_script:
            self._run_init_script()

        wid_of_last_window = None
        for app in self.apps:
            placement = app.get_placement(desktops, monitors)
            if app.creates_window is True:
                window = wm.run_app_and_get_window(app)
                if window is not None:
                    time.sleep(1)
                    window.move(wm, placement)
                    wid_of_last_window = window.wid
                    self.logger.debug('window.wid is: ' + window.wid + " wid_of_last_window is: " + wid_of_last_window)
                    self.windows.append(window)
                else:
                    self.logger.warning('No window could be found for application ' +
                                        app.name)
            else:
                wm.run_app(app)
        if wid_of_last_window:
            self.logger.debug("Focusing window")
            wm.focus_window(wid_of_last_window)
        self.logger.debug("Workset " + self.name + " is now active")
        self.active = True

    def update_and_test_active(self, w_ids):
        """ Use the supplied window ids of current windows registered on the desktop
           to update the workset list of active windows. If none is left, workset is
           set as inactive.
        """
        self.logger.debug("Tests if workset still has active windows.")
        self.windows = [window for window in self.windows if window.wid in w_ids]
        self.logger.debug(str(len(self.windows)) +
                          " Active windows was found.")
        if not self.windows:
            self.logger.debug("Workset no longer active.")
            self.active = False

    def deactivate(self, wm):
        """ Closes all active windows in the set gracefully. """
        self.logger.debug("Terminating applications/windows in the " +
                          self.name +
                          " workset.")
        for window in self.windows:
            window.close(wm)
        self.active = False

    def _run_init_script(self):
        """ Run the init_script of the workset."""
        self.logger.debug('Executing supplied script: ' + self.init_script)
        try:
            result = subprocess.run([self.init_script],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            # result = subprocess.run([self.init_script])

            stdout = result.stdout.decode('utf-8')
            stderr = result.stderr.decode('utf-8')

            if not stdout == '':
                self.logger.info("Execution of init_script returned: " +
                                 stdout.rstrip())
            if not stderr == '':
                self.logger.warning("Execution of init script ERROR: " +
                                    stderr)
            else:
                self.logger.debug("Supplied script executed successfully.")
        except PermissionError:
            self.logger.warning("Execution of script failed - not permitted to execute file.")

