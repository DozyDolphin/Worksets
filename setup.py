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
from os import path
from setuptools import setup
from setuptools import find_packages

package_dir = path.abspath(path.dirname(__file__))

with open(path.join(package_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='worksets',

    version='0.1.1',

    description='Worksets helps you to quickly launch and arrange multiple applications in your desktop environment to support a specific workflow.',

    author='Anders Lykke Gade',

    author_email='worksets@gmail.com',

    url='https://www.github.com',

    download_url='https://www.github.com',

    license='GPLv3',

    packages=find_packages(
            exclude=('__pycache__', 'tests')),
    include_package_data=True,
    package_data={'': ['LICENSE',
                       'CHANGES.txt',
                       'README.md',
                       'README.rst',
                       '*.svg',
                       '*.mo']},

    install_requires=[
        'tinydb>=3.2.1'],

    zip_safe=False,

    entry_points={
        'gui_scripts': ['worksets = worksets.__main__:run']}
    )
