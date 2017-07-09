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
import os
import sys
import importlib
import subprocess


def test_dependencies():
    dependencies = {'*nix': ['wmctrl', 'xdotool'],
                    'python': ['tinydb']}
    missing_dependencies = False
    dep_err_msgs = []

    for dependency in dependencies['*nix']:
        DEVNULL = open(os.devnull, 'w')
        result = subprocess.call(['which', dependency], stdout=DEVNULL)
        if not result == 0:
            dep_err_msgs.append('Linux application: ' + dependency)
            missing_dependencies = True

    for dependency in dependencies['python']:
        loader = importlib.find_loader(dependency)
        result = loader is not None
        if not result:
            dep_err_msgs.append('Python package: ' + dependency)
            missing_dependencies = True

    if missing_dependencies:
        print('Worksets will not work - dependencies missing:')
        for each in dep_err_msgs:
            print(each)
        sys.exit()

def run():
    os.chdir(os.path.dirname(__file__))

    main = Main()
    main()  

test_dependencies()

from .main import Main

run()

