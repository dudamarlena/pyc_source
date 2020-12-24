# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/keybaseapi/api.py
# Compiled at: 2015-08-31 06:25:26
# Size of source mod 2**32: 11980 bytes
"""The core Keybase.io API module.
What this does:
    - Allows you to get data from the keybase site.
    - Turns the data into actual readable data, not weird mangled JSON.

"""
import re
from warnings import warn
import pgp, pgp.message, requests
from configmaster.ConfigKey import ConfigKey
from .exc import VerificationError, UserNotFoundError
headers = {'User-Agent': 'keybase-python3 API interfacer (by https://keybase.io/eyes)'}

class _Keybase(object):
    __doc__ = '\n    The base class for all Keybase API classes.\n    '
    API_VERSION = '1.0'

    def _make_request(self, url: str, params: dict, method: str='GET') -> requests.Response:
        """
        Makes a request to the keybase API. Internal method.
        """
        if method == 'GET':
            return requests.get('https://keybase.io/_/api/{}/{}'.format(self.API_VERSION, url), params=params, headers=headers)
        else:
            if method == 'POST':
                return requests.get('https://keybase.io/_/api/{}/{}'.format(self.API_VERSION, url), data=params, headers=headers)
            return

    def _translate_into_configkey(self, data: requests.Response) -> ConfigKey:
        """
        Transforms data into a ConfigKey object.
        """
        if isinstance(data, requests.Response):
            if 'application/json' in data.headers['Content-Type']:
                c = ConfigKey()
                c.load_from_dict(data.json())
                return c
            else:
                return
        else:
            if isinstance(data, dict):
                c = ConfigKey()
                c.load_from_dict(data)
                return c
            else:
                return

    def _get(self, url: str, params: dict) -> ConfigKey:
        """
        Makes a GET request.
        """
        return self._translate_into_configkey(self._make_request(url, params, 'GET'))

    def _post(self, url: str, params: dict) -> ConfigKey:
        """
        Makes a POST request.
        """
        return self._translate_into_configkey(self._make_request(url, params, 'POST'))

    def verify_data(self, pgp_message: str) -> bool:
        """
        Verifies a PGP message against the public key on file.

        Params:
            - pgp_message: The message to verify. This should be a fully contained message, either compressed or uncompressed, including the data to use and the signature.

        Returns:
            - A boolean, stating if the message was verified or not.

        """
        raise NotImplementedError

    def encrypt_data(self, message: str) -> pgp.message.EncryptedMessageWrapper:
        """"
        Encrypt data for the public key on file.

        Params:
            - message: The message to encrypt. This can be anything, but ideally it is string data.
            For security purposes, this parameter will attempt to be deleted after usage.
            THIS DATA MAY RETAIN IN MEMORY AFTER RETURNING FROM THE FUNCTION. DO NOT USE THIS TO HANDLE SENSITIVE DATA WITHOUT THE APPROPRIATE PRECAUTIONS.

        Returns:
            - a pgp.message.EncryptedMessageWrapper object.

        """
        raise NotImplementedError


class User(_Keybase):
    __doc__ = '\n    A class for getting information about keybase Users.\n\n    This supports things such as twitter://user or github://user.\n\n    Note that if the search returns multiple results, the first one will be picked.\n    '

    def encrypt_data(self, message: str) -> pgp.message.EncryptedMessageWrapper:
        raise NotImplementedError('python-pgp does not currently support encrypting.')

    def verify_data(self, pgp_message: str) -> bool:
        return self._verify_msg(pgp_message)

    def __init__(self, username: str, trust_keybase: bool=False,
                 autofetch: bool=True) -> None:
        """
        Create a new instance of a Keybase user.

        Params:
            - Username: The username to look up.
                This can be either a normal string username (`max`), or a username with a method (`github://maxtaco`).

            - trust_keybase: Should we pretend that keybase is correct, or do we locally verify the signatures?
                By default, we locally verify the signatures.

            - autofetch: Should we download the keybase data automagically, or should we not and just let the user replace the data?
                By default, the data is automatically fetched.
        """
        self.username = username
        if '://' in username:
            self.method = username.split('://')[0]
            self.username = username.split('://')[(-1)]
        else:
            self.method = 'usernames'
        self.fetched = False
        self.raw_keybase_data = None
        self.trust = trust_keybase
        if trust_keybase:
            warn('Trusting Keybase servers for this API request...')
        self.valid = False
        self.raw_public_key = None
        self.public_key = None
        self.fingerprint = ''
        self.keyalgo = 1
        self.keybits = 0
        self.proofs = ConfigKey()
        self.fullname = ''
        self.location = ''
        self.bio = ''
        if autofetch:
            self._get_info()

    def _get_info(self):
        discovery = self._get('user/lookup.json', {self.method: self.username})
        self.raw_keybase_data = discovery
        self._map_data()

    def _map_data(self):
        if self.raw_keybase_data.status.code != 0:
            self.fetched = False
            return
        self.fetched = True
        if len(self.raw_keybase_data.them) <= 0:
            raise UserNotFoundError(self.method + '://' + self.username)
        person = self.raw_keybase_data.them[0]
        self.real_name = person.profile.full_name
        self.location = person.profile.location
        self.bio = person.profile.bio
        self.username = person.basics.username
        self.raw_public_key = person.public_keys.primary.bundle
        self.public_key = pgp.read_key(self.raw_public_key)
        self.fingerprint = person.public_keys.primary.key_fingerprint.upper()
        self.keyalgo = person.public_keys.primary.key_algo
        self.keybits = person.public_keys.primary.key_bits
        self.subkeys = set(key[-16:] for key in person.public_keys.sibkeys)
        for proof in person.proofs_summary.all:
            self.proofs[proof.proof_id] = ConfigKey()
            self.proofs[proof.proof_id].load_from_dict(proof)

        self.valid = True

    def _verify_msg(self, msg: str) -> bool:
        try:
            loaded_msg = pgp.read_message(msg, armored=True)
        except ValueError as e:
            raise VerificationError('Message was invalid') from e

        for sig in loaded_msg.get_message().signatures:
            if self.fingerprint[-16:] in sig.issuer_key_ids:
                signature = sig
                key_to_use = self.public_key
                break
            else:
                for subkey in self.public_key.subkeys:
                    if subkey.fingerprint[-16:] in sig.issuer_key_ids:
                        key_to_use = subkey
                        signature = sig
                        break
                else:
                    continue

                break
        else:
            raise VerificationError('Could not find a valid self signature in proof')

        return key_to_use.verify(signature, loaded_msg.get_message().message)

    def _find_pgp_data(self, data: str) -> str:
        d = data[data.find('-----BEGIN PGP MESSAGE-----'):data.find('-----END PGP MESSAGE-----') + 26]
        d = d.replace('<span class="hljs-horizontal_rule">', '')
        d = d.replace('<span>', '')
        d = d.replace('</span>', '')
        d = d.replace('"', '')
        d = d.replace('<', '').replace('>', '')
        return d

    def verify_proofs(self) -> bool:
        """
        Verify the proofs of this user.

        This scans the available proof locations to find the PGP messages stored within, then verifies the signatures.

        Returns:
            True if verification succeeded.
            False if there was no proofs to verify.

        Raises:
            VerificationError if the proofs failed to verify/validate.
        """
        if len(self.proofs.items()) == 0:
            return False
        if self.trust:
            warn('Blindly trusting Keybase servers that the proofs are valid...')
            for proof in self.proofs.values():
                if proof.state == 1:
                    continue
                else:
                    raise VerificationError('Proof {} could not be verified!'.format(proof.proof_type + '/' + proof.nametag))

            return True
        for proof in self.proofs.values():
            if proof.proof_type == 'github':
                gist_id = proof.proof_url.split('/')[(-1)]
                request_url = 'https://gist.githubusercontent.com/{}/{}/raw'.format(proof.nametag, gist_id)
                r = requests.get(request_url, headers=headers)
                if r.status_code != 200:
                    raise VerificationError('Proof URL could not be validated')
                else:
                    data = r.text
                    key = self._find_pgp_data(data)
                    if not self._verify_msg(key):
                        raise VerificationError('Proof {} could not be verified!'.format(proof.proof_type + '/' + proof.nametag))
            elif proof.proof_type == 'reddit':
                r = requests.get(proof.proof_url + '/.json', headers=headers)
                js = r.json()
                to_search_mtree = js[0]['data']['children'][0]['data']
                if to_search_mtree['author'].lower() != proof.nametag.lower():
                    raise VerificationError('Proof {} username does not match')
                data = self._find_pgp_data(to_search_mtree['selftext'])
                ndata = []
                for line in data.split('\n'):
                    ndata.append(line.lstrip(' '))

                ndata = '\n'.join(ndata)
                if not self._verify_msg(ndata):
                    raise VerificationError('Proof {} could not be verified!'.format(proof.proof_type + '/' + proof.nametag))
            elif proof.proof_type in ('generic_web_site', 'dns', 'coinbase'):
                data = requests.get(proof.proof_url, headers=headers)
                data = self._find_pgp_data(data.text)
                if not self._verify_msg(data):
                    raise VerificationError('Proof {} could not be verified!'.format(proof.proof_type + '/' + proof.nametag))
            else:
                warn('Cannot verify proofs of type {} current due to lack of keybase API support, without HTML scraping.'.format(proof.proof_type))

        return True