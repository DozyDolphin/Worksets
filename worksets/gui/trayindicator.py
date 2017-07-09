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

import functools
import logging

# import time
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot
from .worksetdialog import WorksetDialog
from .manageworksets import ManageWorksets
from .settingsdialog import SettingsDialog


class TrayIndicator(QSystemTrayIcon):

    def __init__(self, icon, controller, publisher, parent=None):
        super().__init__(icon, parent)
        self.logger = logging.getLogger(' TrayIndicator')
        try:
            if not QSystemTrayIcon.isSystemTrayAvailable():
                raise EnvironmentError('System tray not available')
        except EnvironmentError as env_error:
            self.logger.critical('Error - System tray not available')
            message_tuple = [_('System tray not available.'),
                             _('Worksets relies on the system tray - the application will terminate.\n\nPlease enable the system tray and try again.'),
                             '',
                             'Critical',
                             True]
            publisher.user_message('MESSAGE', message_tuple)

        self.controller = controller
        self.publisher = publisher
        self.publisher.register(['UPDATED', 'INSERTED', 'REMOVED'],
                                self,
                                self.update_menu)

        self.active_mw_dialog = None
        self.active_settings_dialog = None
        self.menu = QMenu(parent)
        # Work around since tray.activated signal doesn't work on Ubuntu Unity
        self.menu.aboutToShow.connect(self.icon_activated)
        self.build_menu()
        self.setContextMenu(self.menu)
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.update_menu2)
        #self.timer.start(10000)

    def icon_activated(self):
        self.update_menu("Updating menu on click")
        self.controller.update_active_worksets()
        workset_names = self.controller.get_active_workset_names()
        self.update_active(workset_names)


    def build_menu(self, workset_names = None):
        self.menu.clear()
        worksets = self.controller.get_worksets()
        for workset in worksets:
            action = QAction(workset.name, self)
            action.setCheckable(True)

            if workset_names is not None:
                if action.text() in workset_names:
                    action.setChecked(True)
            self.menu.addAction(action)
            action.triggered.connect(functools.partial(
                self.handle_workset,
                action))

        self.menu.addSeparator()

        create_action = self.menu.addAction(_("Manage worksets"))
        create_action.triggered.connect(self.manage_worksets)

        settings_action = self.menu.addAction(_("Settings"))
        settings_action.triggered.connect(self.settings)

        exit_action = self.menu.addAction(_("Quit"))
        exit_action.triggered.connect(self.close)

    def update_menu(self, message):
        # Change to logger
        self.logger.debug("TrayIndicator: " + message)
        workset_names = self.controller.get_active_workset_names()
        self.build_menu(workset_names)

    def update_active(self, workset_names):
        for action in self.menu.actions():
            if action.isCheckable() is True:
                if action.text() not in workset_names and action.isChecked():
                    self.logger.debug(action.text() + " is no longer active.")
                    action.setChecked(False)

    def handle_workset(self, action):
        if action.isChecked():
            self.controller.activate_workset(action.text())
        elif not action.isChecked():
            self.controller.deactivate_workset(action.text())

    def close(self):
        # remember to test for all windows open
        if self.active_mw_dialog is None:
            self.publisher.dispatch('EXIT', 'The user pressed Quit')
        else:
            self.active_mw_dialog.activateWindow()

    def manage_worksets(self):
        self.logger.debug('Manage Worksets dialog activated')
        if self.active_mw_dialog is None:
            self.active_mw_dialog = ManageWorksets(self.controller, self.publisher)
            self.active_mw_dialog.exec_()

            self.active_mw_dialog = None
        else:
            self.active_mw_dialog.activateWindow()

    def settings(self):
        self.logger.debug('Manage Worksets dialog activated')
        if self.active_settings_dialog is None:
            self.active_settings_dialog = SettingsDialog(self.controller)
            self.active_settings_dialog.exec_()

            self.active_settings_dialog = None
        else:
            self.active_settings_dialog.activateWindow()
