# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgalan/projects/redongo/redongo/utils.py
# Compiled at: 2016-10-27 06:20:38
import general_exceptions
try:
    import cPickle as pickle
except:
    import pickle

def get_application_settings(application_name, redis):
    if not application_name:
        raise general_exceptions.Register_NoApplicationName("Can't set application settings: No application name")
    try:
        application_settings = pickle.loads(redis.get(('redongo_{0}').format(application_name)))
        fields_to_validate = [
         'mongo_host',
         'mongo_port',
         'mongo_database',
         'mongo_collection',
         'mongo_user',
         'mongo_password',
         'bulk_size',
         'bulk_expiration',
         'serializer_type']
        for f in fields_to_validate:
            if not application_settings.get(f, None):
                raise general_exceptions.ApplicationSettingsError(('No {0} value in {1} application settings').format(f, application_name))

        return application_settings
    except TypeError:
        raise general_exceptions.ApplicationSettingsError(('Not existing conf for application {0}').format(application_name))
    except ValueError:
        raise general_exceptions.ApplicationSettingsError(('Invalid existing conf for application {0}').format(application_name))

    return