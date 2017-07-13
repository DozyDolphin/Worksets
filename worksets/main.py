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
import subprocess
import os
import sys
import logging

from .publisher import Publisher
from .gui.gui import Gui
from .system.wm import Wm
from .settings import Settings
from .db import Db
from .screen import Screen
from .controller import Controller


class Main():

    def __init__(self):
        publisher = Publisher(['UPDATED',
                               'ACTIVE_WORKSETS_UPDATED',
                               'INSERTED',
                               'REMOVED',
                               'EXIT',
                               'MESSAGE'
                               ])
        # Test Access to environment
        # Logger
        gui = Gui(publisher)
        wm = Wm(publisher)
        settings = Settings(publisher, wm)
        db = Db(publisher, settings)
        screen = Screen(publisher, wm, db)
        controller = Controller(wm, settings, db, screen)
        gui.start(controller, publisher)

