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
import sys
import os
from PyQt5.QtWidgets import QApplication, QErrorMessage
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from .messagebox import MessageBox
from .trayindicator import TrayIndicator



class Gui():
    '''
    This class is primarily to separate pyqt gui part from the rest of
    the application. Initially it was an invisible main window. Since
    it is no longer setQuitOnLastWindowClosed=false and separate exit
    functionality is needed.
    '''

    def __init__(self, publisher):
        self.logger = logging.getLogger('Gui')
        publisher.register(['EXIT'], self, self.exit)
        publisher.register(['MESSAGE'], self, self.show_message)
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)

    def show_message(self, message_list):
        primary_screen_size = self.app.primaryScreen().size()
        message_box = MessageBox(primary_screen_size, message_list)
        if message_list[4] is True:
            self.logger.critical('Application terminated with the message: ' + message_list[0])
            self.exit(message_list[0])

    def start(self, controller, publisher):
        self.logger = logging.getLogger('Gui')
        self.tray = TrayIndicator(QIcon('icons/worksets_monochrome_icon_dark.svg'),
                                  controller, publisher)
        self.tray.show()
        sys.exit(self.app.exec_())

    def exit(self, message):
        # self.logger.info('Application terminated: ' + message)
        self.app.quit()
        # If exit before qt-part is running
        sys.exit()
