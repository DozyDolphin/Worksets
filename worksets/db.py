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
import os.path
from tinydb import TinyDB, Query
from .app import App
from .workset import Workset


class Db():

    def __init__(self, publisher, settings):
        self.logger = logging.getLogger(' Db')
        try:
            if not os.path.exists(settings.db_dir):
                self.logger.info("db directory doesn't exist - creating...")
                os.makedirs(settings.db_dir)
        except IOError as e:
            self.logger.critical("Couldn't create directory " + settings.db_dir + " : " + str(e))
        self.db_file = 'db.json'
        db_path = settings.db_dir + '/' + self.db_file
        self.publisher = publisher
        try:
            if not os.path.isfile(db_path):
                self.logger.info("db file doesn't exist - creating...")
                self.db = TinyDB(db_path)
                self.db.table('worksets')
                self.db.purge_table('default')
        except IOError as e:
            self.logger.critical("Couldn't create db file: " + str(e))
        self.db = TinyDB(db_path)
        self.w_query = Query()

    def get_worksets(self):
        table = self.db.table('worksets')
        worksets = []
        for workset_dict in table.all():
            workset = self._convert_to_workset(workset_dict)
            worksets.append(workset)
        return worksets

    def insert(self, workset):
        table = self.db.table('worksets')
        workset_dict = self._convert_to_dict(workset)
        table.insert(workset_dict)
        self.publisher.dispatch('INSERTED', "Workset has been saved!")

    def update(self, workset):
        table = self.db.table('worksets')
        workset_dict = self._convert_to_dict(workset)
        table.update(workset_dict, eids=[workset.db_eid])
        self.publisher.dispatch('UPDATED', "Workset has been updated!")

    def remove(self, workset):
        table = self.db.table('worksets')
        table.remove(eids=[workset.db_eid])
        self.publisher.dispatch('REMOVED', "Workset has been deleted!")

    def rearrange_worksets(self, workset_names):
        old_workset_dicts = self.db.table('worksets').all()
        new_workset_dicts = sorted(old_workset_dicts, key=lambda dict: workset_names.index(dict['name']))
        # This is not the right way to make sure nothing goes wrong
        try:
            self.db.purge_table('worksets')
            self.db.table('worksets')
            self.db.table('worksets').insert_multiple(new_workset_dicts)
            self.publisher.dispatch('UPDATED', "Worksets has been rearranged!")
        except Exception as e:
            self.logger.critical("An error occurred trying to rearrange the worksets: " + str(e))

    def get_workset_by_name(self, name):
        workset = None
        table = self.db.table('worksets')
        result = table.search(self.w_query.name == name)
        # Should test if more than one in list here
        workset_dict = result[0]
        workset = self._convert_to_workset(workset_dict)
        return workset

    def test_worksetname_unique(self, name, db_eid):
        table = self.db.table('worksets')
        result = table.get(self.w_query.name == name)
        if not result:
            return True
        elif result.eid == int(db_eid):
            return True
        else:
            return False


    def remove_by_name(self, name):
        table = self.db.table('worksets')
        workset = Query()
        if workset.name == name:
            table.remove(workset.name == name)
            self.publisher.dispatch('REMOVED', "Workset has been deleted!")

    def _convert_to_workset(self, workset_dict):
        apps = []
        for app_dict in workset_dict['apps']:
            app = App(
                app_dict['name'],
                app_dict['placement'],
                app_dict['executable'],
                app_dict['parameters'],
                app_dict['creates_window'],
                app_dict['has_splash'],
                app_dict['uses_existing_window'])
            apps.append(app)

        workset = Workset(
            workset_dict['name'],
            apps,
            workset_dict['init_script'],
            workset_dict.eid)
        return workset

    def _convert_to_dict(self, workset):
        apps = []
        for each in workset.apps:
            name = each.name
            placement = (each.placement_desktop + '.' +
                         each.placement_monitor + '.' +
                         each.placement_type)
            executable = each.executable
            parameters = ' '.join(each.parameters)
            creates_window = each.creates_window
            has_splash = each.has_splash
            uses_existing_window = each.uses_existing_window
            app = {'name': name,
                   'placement': placement,
                   'executable': executable,
                   'parameters': parameters,
                   'creates_window': creates_window,
                   'has_splash': has_splash,
                   'uses_existing_window': uses_existing_window}
            apps.append(app)
        workset_name = workset.name
        init_script = workset.init_script

        workset_dict = {'name': workset_name,
                        'init_script': init_script,
                        'apps': apps}
        return workset_dict
