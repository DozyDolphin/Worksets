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
from . import placement_factory
from .app import App
from .workset import Workset


class Controller():

    def __init__(self, wm, settings, db, screen):
        self.logger = logging.getLogger('Controller')
        self.wm = wm
        self.settings = settings
        self.db = db
        self.screen = screen

    def activate_workset(self, workset_name):
        self.screen.activate_workset(workset_name)

    def deactivate_workset(self, workset_name):
        self.screen.deactivate_workset(workset_name)

    def get_worksets(self):
        return self.db.get_worksets()

    def get_active_workset_names(self):
        return self.screen.get_active_workset_names()

    def update_active_worksets(self):
        self.screen.update_active_worksets()

    def update_screen_config(self):
        self.screen.update_screen_config()

    def get_placements(self):
        return placement_factory.get_placements()

    def get_monitors(self):
        return self.screen.monitors

    def get_desktops(self):
        return self.screen.desktops

    def get_version(self):
        return self.settings.WORKSETS_VERSION

    def test_app(self, app):
        self.screen.run_app(app)

    def create_app(self, app_data):
        placements = self.get_placements()
        placement_str = (app_data['desktop'] +
                         '.' +
                         app_data['monitor'] +
                         '.' +
                         placements[app_data['placement']])
        app = App(app_data['name'],
                  placement_str,
                  app_data['executable'],
                  app_data['parameters'],
                  app_data['creates_window'],
                  app_data['has_splash'],
                  app_data['uses_existing_window'])
        return app

    def test_app_data(self, app_data, apps):
        if app_data['name'] == '':
            raise NameError(_('Name cannot be empty.'))

        app_names = [app.name for app in apps if app.name == app_data['name']]
        if app_names:
            if 'org_name' in app_data:
                if not app_data['org_name'] == app_names[0]:
                    raise NameError(_('Name must be unique'))
            else:
                raise NameError_(('Name must be unique'))

        if not self.wm.test_executable(app_data['executable']):
            raise OSError(_("Program doesn't seem to exist"))

    def remove_workset(self, workset):
        self.db.remove(workset)

    def remove_workset_by_name(self, name):
        self.db.remove_by_name(name)

    def rearrange_worksets(self, workset_names):
        self.db.rearrange_worksets(workset_names)

    def save_or_update_workset(self, workset_data):
        self._test_workset_data(workset_data)
        workset = self._create_workset(workset_data)
        if workset.db_eid == -1:
            self.db.insert(workset)
        else:
            self.db.update(workset)

    def _test_workset_data(self, workset_data):
        if workset_data['name'] == '':
            raise NameError(_('Name cannot be empty.'))
        if not self.db.test_worksetname_unique(workset_data['name'],
                                               workset_data['db_eid']):
            raise NameError(_('Name has to be unique'))

    def _create_workset(self, workset_data):
        self.logger.debug("Creating workset from workset_data with applications: " +
                          str(workset_data['apps']))
        workset = Workset(workset_data['name'],
                          workset_data['apps'],
                          workset_data['init_script'],
                          workset_data['db_eid'])
        self.logger.debug("Workset created - it holds the applications: " +
                          str(workset.apps))
        return workset

    def test_workset(self, workset_data):
        self._test_workset_data(workset_data)
        workset = self._create_workset(workset_data)
        self.screen.run_workset(workset)

    def get_languages(self):
        return self.settings.available_languages

    def get_language(self):
        return self.settings.language

    def set_language(self, language_name):
        self.settings.change_language(language_name)

    def get_script_dir(self):
        return self.settings.script_dir

    def get_log_enabled(self):
        return self.settings.log_enabled

    def get_log_to_console(self):
        return self.settings.log_to_console

    def get_log_level(self):
        return self.settings.log_level

    def get_log_levels(self):
        return self.settings.get_log_levels()

    def get_log_dir(self):
        return self.settings.log_dir

    def save_settings(self, settings_data):
        self.settings.save_settings(settings_data)
