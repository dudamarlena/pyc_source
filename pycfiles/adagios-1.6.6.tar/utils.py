# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/adagios/adagios/../adagios/utils.py
# Compiled at: 2018-05-16 10:07:32
import adagios.status.utils, adagios, pynag.Model, adagios.exceptions, adagios.settings, os, pynag.Utils.misc
from multiprocessing.pool import ThreadPool
from django.utils.translation import ugettext as _
SELENIUM_DRIVER = None

def wait(object_type, WaitObject, WaitCondition, WaitTrigger, **kwargs):
    livestatus = adagios.status.utils.livestatus(None)
    livestatus.get(object_type, WaitObject=WaitObject, WaitCondition=WaitCondition, WaitTrigger=WaitTrigger, **kwargs)
    print WaitObject
    return


def wait_for_objects(object_type, object_list, condition=None, trigger='check'):
    if not condition:
        condition = 'last_check > %s' % int(0)
    callback = lambda x: wait(object_type, WaitObject=x, WaitCondition=condition, WaitTrigger=trigger)
    for WaitObject in object_list:
        callback(WaitObject)


def wait_for_service(host_name, service_description, condition='last_check >= 0', trigger='check'):
    livestatus = adagios.status.utils.livestatus(None)
    waitobject = '%s;%s' % (host_name, service_description)
    livestatus.get_services(host_name=host_name, service_description=service_description, WaitCondition=condition, WaitObject=waitobject)
    return


class Task(object):

    def __init__(self, num_processes=5):
        self._tasks = []
        adagios.tasks.append(self)
        self._pool = ThreadPool(processes=num_processes)

    def add(self, function, *args, **kwargs):
        print 'Adding Task:', locals()
        result = self._pool.apply_async(function, args, kwargs)
        self._tasks.append(result)

    def status(self):
        all_tasks = self._tasks
        for i in all_tasks:
            print i.ready()

        completed_tasks = filter(lambda x: x.ready(), all_tasks)
        return ('{done}/{total} done.').format(done=len(completed_tasks), total=len(all_tasks))

    def get_id(self):
        return hash(self)

    def ready(self):
        """ Returns True if all the Tasks in this class have finished running. """
        return max(map(lambda x: x.ready(), self._tasks))


def update_eventhandlers(request):
    """ Iterates through all pynag eventhandler and informs them who might be making a change
    """
    remote_user = request.META.get('REMOTE_USER', 'anonymous')
    for i in pynag.Model.eventhandlers:
        i.modified_by = remote_user

    try:
        from pynag.Utils import GitRepo
        import okconfig
        okconfig.git = GitRepo(directory=os.path.dirname(adagios.settings.nagios_config), auto_init=False, author_name=remote_user)
    except Exception:
        pass


def get_available_themes():
    """ Returns a tuple with the name of themes that are available in media/theme directory """
    theme_dir = os.path.join(adagios.settings.STATIC_ROOT, adagios.settings.THEMES_FOLDER)
    result = []
    for root, dirs, files in os.walk(theme_dir):
        if adagios.settings.THEME_ENTRY_POINT in files:
            result.append(os.path.basename(root))

    return result


class FakeAdagiosEnvironment(pynag.Utils.misc.FakeNagiosEnvironment):
    _adagios_settings_copy = None

    def __init__(self, *args, **kwargs):
        super(FakeAdagiosEnvironment, self).__init__(*args, **kwargs)

    def update_adagios_global_variables(self):
        """ Updates common adagios.settings to point to a temp directory.

         If you are are doing unit tests which require specific changes, feel free to update
         adagios.settings manually after calling this method.
        """
        self._adagios_settings_copy = adagios.settings.__dict__.copy()
        adagios.settings.adagios_configfile = self.adagios_config_file
        adagios.settings.USER_PREFS_PATH = self.adagios_config_dir + '/userdata'
        adagios.settings.nagios_config = self.cfg_file
        adagios.settings.livestatus_path = self.livestatus_socket_path
        adagios.settings.reload_configfile(self.adagios_config_file)

    def restore_adagios_global_variables(self):
        """ Restores adagios.settings so it looks like before update_adagios_global_variables() was called
        """
        adagios.settings.__dict__.clear()
        adagios.settings.__dict__.update(self._adagios_settings_copy)

    def create_minimal_environment(self):
        """ Behaves like FakeNagiosEnvironment except also creates adagios config directory """
        super(FakeAdagiosEnvironment, self).create_minimal_environment()
        self.adagios_config_dir = os.path.join(self.tempdir, 'adagios')
        self.adagios_config_file = os.path.join(self.adagios_config_dir, 'adagios.conf')
        os.makedirs(self.adagios_config_dir)
        with open(self.adagios_config_file, 'w') as (f):
            f.write('')

    def terminate(self):
        """ Behaves like FakeNagiosEnvironment except also restores adagios.settings module """
        if self._adagios_settings_copy:
            self.restore_adagios_global_variables()
        super(FakeAdagiosEnvironment, self).terminate()


def get_test_environment():
    """Get a fake adagios environment for testing purposes.

    Convenvience method for getting and starting a fake nagios environment.

    Returns:
        FakeAdagiosEnvironment instance.
    """
    environment = FakeAdagiosEnvironment()
    environment.create_minimal_environment()
    environment.update_model()
    environment.update_adagios_global_variables()
    environment.configure_livestatus()
    return environment