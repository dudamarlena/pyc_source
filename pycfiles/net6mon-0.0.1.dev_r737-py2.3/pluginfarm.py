# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/net6mon/pluginfarm.py
# Compiled at: 2006-06-20 07:07:59
"""
    Pluginfarm module
    Ce module contient les objets utilisés pour la gestion des plugins
"""
import sys, os, time, thread, copy, pkg_resources
from net6mon.env import Environment
from net6mon.sql import SQLMapper
_plugin_entry_point = 'net6mon.plugins'

class pluginFarm(object):
    """
    Cette classe est une sorte de '''ferme à plugin'''
        
    C'est cette classe qui est chargée de trouver/charger/instancier/lister
    des plugins mais aussi de réaliser les appels à ces instances
    """
    __module__ = __name__

    def __init__(self, env, plugin_dir=[]):
        if pkg_resources is None:
            raise 'setuptools must be installed'
        self._env = env
        self._plugin_instances = []
        self._plugin_dir = []
        self._plugin_dir.append(self._env.config.plugin_dir)
        self._plugin_env = pkg_resources.Environment(self._plugin_dir + sys.path + plugin_dir)
        self._available_plugins = []
        self._get_available_plugins()
        self._env.log.debug('Starting plugin farm')
        return

    def list_plugins(self):
        """ 
            Liste les plugins disponibles
        """
        for name in self._plugin_env:
            egg = self._plugin_env[name][0]
            self._env.log.debug('---Listing plugins availables---')
            for name in egg.get_entry_map(_plugin_entry_point):
                entry_point = egg.get_entry_info(_plugin_entry_point, name)
                self._env.log.debug('Plugin name %s ', str(entry_point.name))

    def _get_available_plugins(self):
        """
        Initialise self._available_plugins pour y stocker la liste de tout les noms de plugins
        disponibles.

        """
        self._env.log.debug('getting available plugins')
        for name in self._plugin_env:
            egg = self._plugin_env[name][0]
            for name in egg.get_entry_map(_plugin_entry_point):
                entry_point = egg.get_entry_info(_plugin_entry_point, name)
                if entry_point.name not in self._available_plugins:
                    self._available_plugins.append(entry_point.name)
                self._env.log.debug('available plugin type: %s', entry_point.name)

        return self._available_plugins

    def get_instance_config(self, instance_name):
        """
        retourne le dictionaire représentant la configuration d'une instance
        """
        for i in self._plugin_instances:
            if i['plugin_instance_name'] == instance_name:
                return i['plugin_instance_config']

        return 1

    def set_instance_config(self, instance_name, instance_config):
        """ 
        Met a jour la configuration d'un plugin
        """
        for i in self._plugin_instances:
            if i['plugin_instance_name'] == instance_name:
                i['plugin_instance_config'] = instance_config
                return True

        return 1

    def get_instance_description(self, instance_name):
        """
        Retourne la description d'une instance
        """
        for i in self._plugin_instances:
            if i['plugin_instance_name'] == instance_name:
                return i['plugin_instance_description']

        return 1

    def set_instance_description(self, instance_name, description):
        """
        Met a jour la description d'une instance
        """
        for i in self._plugin_instances:
            if i['plugin_instance_name'] == instance_name:
                i['plugin_instance_description'] = description
                return True

        return 1

    def get_instance_interval(self, instance_name):
        """
        Retourne l'interval d'execution d'une instance 
        """
        for i in self._plugin_instances:
            if i['plugin_instance_name'] == instance_name:
                return i['interval']

        return 1

    def set_instance_interval(self, instance_name, interval):
        """ 
        Met a jour l'interval d'execution d'une instance
        """
        for i in self._plugin_instances:
            if i['plugin_instance_name'] == instance_name:
                i['interval'] = interval
                return True

        return 1

    def get_instance_type(self, instance_name):
        """
        Retourne le type de plugin d'une instance
        """
        for i in self._plugin_instances:
            if i['plugin_instance_name'] == instance_name:
                return i['plugin_name']

        return 1

    def get_instance_list(self):
        """
        Retourne la liste des instances en cours 

        """
        instance_list = []
        for il in self._plugin_instances:
            cri = {}
            for i in il.keys():
                if i is not 'plugin_instance':
                    cri[i] = il[i]

            instance_list.append(cri)

        return instance_list

    def instanciate_plugin(self, plugin_name, instance_name, instance_description='', instance_config={}, interval=0):
        """
            Cette fonction instancie un plugin
            @param plugin_name: nom du plugin à instancier
            @param instance_name: nom de l'instance de ce plugin
            @param instance_description: description de l'instance
        """
        for egg_name in self._plugin_env:
            egg = self._plugin_env[egg_name][0]
            for name in egg.get_entry_map(_plugin_entry_point):
                if name == plugin_name:
                    egg.activate()
                    entry_point = egg.get_entry_info(_plugin_entry_point, plugin_name)
                    mod = entry_point.load()
                    plg = mod(plugin_name, instance_name, instance_config, self._env.log, os.path.join(self._env.config.database_dir, instance_name + '.db'))
                    self._env.log.debug('Instantiating plugin: name=%s, instance_name=%s, instance_description=%s, call evey %ss', plugin_name, instance_name, instance_description, interval)
                    self._plugin_instances.append({'plugin_name': plugin_name, 'plugin_instance': plg, 'plugin_instance_name': instance_name, 'plugin_instance_description': instance_description, 'plugin_instance_config': instance_config, 'interval': int(interval), 'last_call': 0})
                    return True

        return None
        return

    def list_instances(self):
        """ 
            Liste les instances de plugins en cours dans la ferme

        """
        self._env.log.debug('Currently instancied plugins: ')
        for i in self._plugin_instances:
            self._env.log.debug('---------------------------------------------------------\nplugin name:                 %s\nplugin instance name:        %s\nplugin instance description: %s\n                                ', str(i['plugin_name']), str(i['plugin_instance_name']), str(i['plugin_instance_description']))

    def get_instance_result(self, instance_name):
        """
        Execute une instance puis vas chercher le resultat dans la base de données de l'instance
        """
        ts = '%s' % time.time()
        ts = ts.split('.')[0]
        print self._plugin_instances
        for i in self._plugin_instances:
            if i['plugin_instance_name'] == instance_name:
                i['plugin_instance'].get_result()
                return self.get_instance_result_at_date(instance_name, ts)

        return 1

    def get_instance_result_at_date(self, instance_name, date):
        """
        Cherche le resultat d'une instance dans ca base de donnée à une date précise
        """
        dbname = os.path.join(self._env.config.database_dir, '%s.db' % instance_name)
        if not os.path.exists(dbname):
            raise 'Database does not exists (%s)' % dbname
        ptype = self._get_instance_type(instance_name)
        db = SQLMapper(dbname, ptype, instance_name)
        row = db.get_row_at_date(date)
        schema = db._get_table_schema()
        ret = (schema, [row])
        return ret

    def get_instance_table_creation_query(self, instance_name):
        for i in self._plugin_instances:
            if i['plugin_instance_name'] == instance_name:
                return i['plugin_instance'].get_tbl_creation_query()

        return 1

    def get_instance_results(self, instance_name):
        """
        Renvois touts les enregistrements de la base d'une instance
        """
        dbname = os.path.join(self._env.config.database_dir, '%s.db' % instance_name)
        if not os.path.exists(dbname):
            raise 'Database does not exists (%s)' % dbname
        ptype = self._get_instance_type(instance_name)
        db = SQLMapper(dbname, ptype, instance_name)
        row = db.get_rows()
        schema = db._get_table_schema()
        ret = (schema, row)
        return ret

    def get_instance_results_between(self, instance_name, date_start, date_stop):
        """
        Renvoi tout les enregistrement de la base d'une instance dans un interval de dates
        """
        dbname = os.path.join(self._env.config.database_dir, '%s.db' % instance_name)
        if not os.path.exists(dbname):
            raise 'Database does not exists (%s)' % dbname
        ptype = self._get_instance_type(instance_name)
        db = SQLMapper(dbname, ptype, instance_name)
        row = db.get_rows_between_dates(date_start, date_stop)
        schema = db._get_table_schema()
        ret = (schema, row)
        return ret

    def purge_instance_table(self, instance_name):
        dbname = os.path.join(self._env.config.database_dir, '%s.db' % instance_name)
        if not os.path.exists(dbname):
            raise 'Database does not exists (%s)' % dbname
        ptype = self._get_instance_type(instance_name)
        db = SQLMapper(dbname, ptype, instance_name)
        db.purge_rows()
        return True

    def purge_instance_table_from(self, instance_name, date_from):
        dbname = os.path.join(self._env.config.database_dir, '%s.db' % instance_name)
        if not os.path.exists(dbname):
            raise 'Database does not exists (%s)' % dbname
        ptype = self._get_instance_type(instance_name)
        db = SQLMapper(dbname, ptype, instance_name)
        db.purge_rows_from(date_from)
        return True

    def purge_instance_table_between(self, instance_name, date_from, date_stop):
        dbname = os.path.join(self._env.config.database_dir, '%s.db' % instance_name)
        if not os.path.exists(dbname):
            raise 'Database does not exists (%s)' % dbname
        ptype = self._get_instance_type(instance_name)
        db = SQLMapper(dbname, ptype, instance_name)
        db.purge_rows_between(date_from, date_stop)
        return True

    def purge_all_instance_table(self, date_from):
        for i in self._plugin_instances:
            self.purge_instance_table(i['plugin_instance_name'])

        return True

    def purge_all_instance_table_from(self, date_from):
        for i in self._plugin_instances:
            self.purge_instance_table_from(i['plugin_instance_name'], date_from)

        return True

    def purge_all_instance_table_between(self, date_from, date_stop):
        for i in self._plugin_instances:
            self.purge_instance_table_between(i['plugin_instance_name'], date_from, date_stop)

        return True

    def _get_instance_type(self, instance_name):
        for i in self._plugin_instances:
            if i['plugin_instance_name'] == instance_name:
                return i['plugin_name']

        return 1

    def load_instances(self):
        for i in self._env.config.plugins.keys():
            self._env.log.debug('%s plugin found in config file, loading...', i)
            itype = self._env.config.get_plugin_instance_type(i)
            if itype not in self._available_plugins:
                self._env.log.error('plugin type %s does not exists', itype)
                raise 'Bad plugin configuration'
            if self._env.config.plugins[i].has_key('description'):
                idesc = self._env.config.plugins[i]['description']
            else:
                idesc = 'no desc'
            if self._env.config.plugins[i].has_key('interval'):
                interval = self._env.config.plugins[i]['interval']
            else:
                interval = 0
            iconf = self._env.config.get_plugin_instance_config(i)
            if self.instanciate_plugin(itype, i, idesc, iconf, interval) is None:
                self._env.log.error('%s plugin not instancied successfully' % i)

        return

    def add_instance(self, instance_name, plugin_type, interval, description, config={}):
        if plugin_type not in self._available_plugins:
            self._env.log.error('No such plugin type available')
            return 1
        return self.instanciate_plugin(plugin_type, instance_name, description, config, interval)

    def remove_instance(self, instance_name):
        for i in self._plugin_instances:
            if self._plugin_instance['plugin_instance_name'] == instance_name:
                del self._plugin_instances[i]['plugin_instance']
                del self._plugin_instances[i]
                return True

        self._env.log.error("No instance '%s' found" % instance_name)
        return 1

    def schedule_forever(self):
        while True:
            current_time = int(time.time())
            for inst in self._plugin_instances:
                if current_time - inst['last_call'] >= inst['interval']:
                    self._env.log.debug('Launching %s get_result.' % inst)
                    thread.start_new_thread(inst['plugin_instance'].get_result, ())
                    inst['last_call'] = int(time.time())

            time.sleep(1)

    def get_actives_instances(self):
        pass


def test_farm():
    env = Environment('netmon.conf')
    pf = pluginFarm(env)
    pf.load_instances()
    pf._get_available_plugins()
    pf.list_instances()
    pf.get_actives_instances()
    pf.schedule_forever()
    print pf.get_instance_result_at_date('foo', 0)


if __name__ == '__main__':
    test_farm()