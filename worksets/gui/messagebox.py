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

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt


class MessageBox(QWidget):

    message_type = {'Question': QMessageBox.Question,
                    'Information': QMessageBox.Information,
                    'Warning': QMessageBox.Warning,
                    'Critical': QMessageBox.Critical}

    def __init__(self, primary_screen_size, message_list):
        super().__init__()
        self.width = 520
        self.height = 400
        self.left = (primary_screen_size.width() - self.width) / 2
        self.top = (primary_screen_size.height() - self.height) / 2

        self.setupUi(message_list)

    def setupUi(self, message_list):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.msg = QMessageBox()
        self.msg.setIcon(self.message_type[message_list[3]])
        self.msg.setWindowTitle('Worksets')
        self.msg.setText(message_list[0])
        self.msg.setInformativeText(message_list[1])
        self.msg.setDetailedText(message_list[2])
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec()
