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


from collections import OrderedDict
from collections import namedtuple


def get_placements():
    '''
    gets the description of a placement for the GUI (key) with the
    corresponding placement type identifier used by the program (value)
    '''
    placements_tuple = [
        (_('Maximized'), 'M'),
        (_('Top'), 'T'),
        (_('Bottom'), 'B'),
        (_('Upper left'), 'UL'),
        (_('Left'), 'L'),
        (_('Lower left'), 'LL'),
        (_('One third left'), 'OTL'),
        (_('Two thirds left'), 'TTL'),
        (_('Upper right'), 'UR'),
        (_('Right'), 'R'),
        (_('Lower right'), 'LR'),
        (_('One third right'), 'OTR'),
        (_('Two thirds right'), 'TTR')]

    placements = OrderedDict(placements_tuple)
    return placements


def create(type_of_placement, desktop, monitor):
    Placement = namedtuple(
        'Placement',
        'type, desktop, monitor, x, y, width, height')  # add desktop nr.

    #  By default 'M'aximized
    x = monitor.x
    y = monitor.y
    width = monitor.width
    height = monitor.height

    if type_of_placement == 'T':  # Top
        height = (monitor.height // 2)

    elif type_of_placement == 'B':  # Bottom
        y = monitor.y + (monitor.height // 2)
        height = monitor.height // 2

    elif type_of_placement == 'UL':  # Upper left
        width = monitor.width // 2
        height = monitor.height // 2

    elif type_of_placement == 'L':  # Left
        width = monitor.width // 2

    elif type_of_placement == 'LL':  # Lower left
        y = monitor.y + (monitor.height // 2)
        width = monitor.width // 2
        height = monitor.height // 2

    elif type_of_placement == 'UR':  # Upper right
        x = monitor.x + (monitor.width // 2)
        width = monitor.width // 2
        height = monitor.height // 2

    elif type_of_placement == 'R':  # Right
        x = monitor.x + (monitor.width // 2)
        width = monitor.width // 2

    elif type_of_placement == 'LR':  # Lower right
        x = monitor.x + (monitor.width // 2)
        y = monitor.y + (monitor.height // 2)
        width = monitor.width // 2
        height = monitor.height // 2

    elif type_of_placement == 'OTL':  # One third left
        width = (monitor.width // 3)

    elif type_of_placement == 'TTL':  # Two thirds left
        width = (monitor.width // 3) * 2

    elif type_of_placement == 'OTR':  # One third right
        x = monitor.x + ((monitor.width // 3) * 2)
        width = (monitor.width // 3)

    elif type_of_placement == 'TTR':  # Two thirds right
        x = monitor.x + (monitor.width // 3)
        width = (monitor.width // 3) * 2

    placement = Placement(type_of_placement,
                          desktop,
                          monitor,
                          x,
                          y,
                          width,
                          height)
    return placement
