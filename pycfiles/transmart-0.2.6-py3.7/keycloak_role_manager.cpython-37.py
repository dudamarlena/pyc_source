# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/transmart/api/utils/keycloak_role_manager.py
# Compiled at: 2019-08-20 07:47:59
# Size of source mod 2**32: 5859 bytes
import requests, logging, click
from ..auth import KeyCloakAuth
logger = logging.getLogger('tm-api')

class KeyCloakRoleManagerException(Exception):
    pass


class KeyCloakRoleManager:
    __doc__ = '\n    The user for whom an offline token was generated requires \'ROLE_ADMIN\'\n    in transmart-api client in KeyCloak to see all studies.\n\n    Also required for this user is the \'manage-clients\' role in the \'realm-management\' client\n    to find the guid corresponding to transmart-api client and add roles.\n\n    Example usage:\n    \x08\n        import transmart as tm\n        from transmart.api.utils import KeyCloakRoleManager\n        host = \'https://transmart-dev.thehyve.net\'\n        kc_url = "https://keycloak-dwh-test.thehyve.net"\n        kc_realm = "transmart-dev"\n\n        offline_token = None\n\n        api = tm.get_api(\n            host = host,\n            api_version = 2,\n            offline_token = offline_token,\n            kc_url=kc_url,\n            kc_realm=kc_realm,\n            print_urls = True,\n            interactive = True\n        )\n\n        kc_manager = KeyCloakRoleManager(api)\n        # The following adds roles for all studies. To add roles\n        # for a specific study use kc_manager.add_single_study_roles()\n        kc_manager.add_all_studies()\n\n    '
    STUDY_ROLES = {'MEASUREMENTS':'Observations for ', 
     'COUNTS_WITH_THRESHOLD':'Threshold summary level for '}

    def __init__(self, api):
        if not isinstance(api.auth, KeyCloakAuth):
            msg = 'Expected to be authenticated via KeyCloakAuth, but got {}.'.format(type(api.auth))
            raise TypeError(msg)
        self.api = api
        self.url = self.api.auth.url
        self.realm = self.api.auth.realm
        self.client_name = self.api.auth.client_id
        self._client_id = self.get_client_guid()
        self.roles_url = '{}/auth/admin/realms/{}/clients/{}/roles'.format(self.url, self.realm, self._client_id)

    @property
    def _headers(self):
        return {'Authorization': 'Bearer ' + self.api.auth.access_token}

    def get_client_guid(self):
        print('Querying for client guid.')
        r = requests.get(url=('{}/auth/admin/realms/{}/clients'.format(self.url, self.realm)), headers=(self._headers))
        if r.status_code == 403:
            msg = "Access denied. Do you have the 'manage-clients' role in the 'realm-management'?"
            raise KeyCloakRoleManagerException(msg)
        r.raise_for_status()
        clients = [c.get('id') for c in r.json() if c.get('clientId') == self.client_name]
        if len(clients) == 0:
            msg = 'Client {!r} not found in KeyCloak'.format(self.client_name)
            raise KeyCloakRoleManagerException(msg)
        return clients[0]

    def get_current_roles(self):
        """ Get the set of all study roles currently in KeyCloak. """
        r = requests.get(url=(self.roles_url), headers=(self._headers))
        r.raise_for_status()
        return {role['name'] for role in r.json()}

    @staticmethod
    def get_role_representation(name, description):
        return {'name':name, 
         'scopeParamRequired':'', 
         'description':description}

    def add_single_study_roles(self, study_id: str, study_description: str=None):
        """
        Try to add all roles in self.STUDY_ROLES to KeyCloak for a given
        study id. If the role already exists, nothing happens.

        :param study_id: transmart study_id
        :param study_description: a optional name for the study which will
            be used in the role description in KeyCloak.
        """
        if not study_description:
            study_description = study_id
        for role, human_level in self.STUDY_ROLES.items():
            name = '{}|{}'.format(study_id, role)
            desc = human_level + study_description
            r = requests.post(url=(self.roles_url),
              headers=(self._headers),
              json=(self.get_role_representation(name, desc)))
            if 200 <= r.status_code <= 299:
                print('Added role {!r} for {!r}.'.format(role, study_id))

    def add_all_studies(self):
        """
        Calls self.add_single_study_roles() for all studies in transmart.
        """
        study_ids = [s.get('studyId') for s in self.api.get_studies(as_json=True).get('studies') if s.get('secureObjectToken') != 'PUBLIC']
        for study in study_ids:
            self.add_single_study_roles(study)


def run_role_manager(transmart, kc_url, realm, offline_token=None, study=None):
    import transmart as tm
    api = tm.get_api(host=transmart,
      api_version=2,
      offline_token=offline_token,
      kc_url=kc_url,
      kc_realm=realm,
      print_urls=True,
      interactive=False)
    kc_manager = KeyCloakRoleManager(api)
    if study:
        kc_manager.add_single_study_roles(study)
    else:
        kc_manager.add_all_studies()


@click.command()
@click.option('-t', '--transmart', required=True, help='tranSMART host url, e.g. https://transmart-dev.thehyve.net.')
@click.option('-k', '--kc-url', required=True, help='KeyCloak host, e.g. https://keycloak-dwh-test.thehyve.net.')
@click.option('-r', '--realm', help='KeyCloak realm.', required=True)
@click.option('-o', '--offline-token', help='KeyCloak offline token, will be asked for if not provided.')
@click.option('-s', '--study', default=None, help='Add roles for this study IDs. If not provided, add all studies.')
@click.version_option(prog_name='Add roles from tranSMART to KeyCloak.')
def _role_manager_entry_point(*args, **kwargs):
    run_role_manager(*args, **kwargs)