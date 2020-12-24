# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pretty_bad_protocol/_parsers.py
# Compiled at: 2018-07-27 14:54:13
"""Classes for parsing GnuPG status messages and sanitising commandline
options.
"""
from __future__ import absolute_import
from __future__ import print_function
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import re
from . import _util
from ._util import log
ESCAPE_PATTERN = re.compile('\\\\x([0-9a-f][0-9a-f])', re.I)
HEXADECIMAL = re.compile('^[0-9A-Fa-f]+$')

class ProtectedOption(Exception):
    """Raised when the option passed to GPG is disallowed."""
    pass


class UsageError(Exception):
    """Raised when incorrect usage of the API occurs.."""
    pass


def _check_keyserver(location):
    """Check that a given keyserver is a known protocol and does not contain
    shell escape characters.

    :param str location: A string containing the default keyserver. This
                         should contain the desired keyserver protocol which
                         is supported by the keyserver, for example, the
                         default is ``'hkp://wwwkeys .pgp.net'``.
    :rtype: :obj:`str` or :obj:`None`
    :returns: A string specifying the protocol and keyserver hostname, if the
              checks passed. If not, returns None.
    """
    protocols = [
     'hkp://', 'hkps://', 'http://', 'https://', 'ldap://',
     'mailto:']
    for proto in protocols:
        if location.startswith(proto):
            url = location.replace(proto, str())
            host, slash, extra = url.partition('/')
            if extra:
                log.warn("URI text for %s: '%s'" % (host, extra))
            log.debug("Got host string for keyserver setting: '%s'" % host)
            host = _fix_unsafe(host)
            if host:
                log.debug("Cleaned host string: '%s'" % host)
                keyserver = proto + host
                return keyserver
            return

    return


def _check_preferences(prefs, pref_type=None):
    """Check cipher, digest, and compression preference settings.

    MD5 is not allowed. This is `not 1994`__. SHA1 is allowed_ grudgingly_.

    __ http://www.cs.colorado.edu/~jrblack/papers/md5e-full.pdf
    .. _allowed: http://eprint.iacr.org/2008/469.pdf
    .. _grudgingly: https://www.schneier.com/blog/archives/2012/10/when_will_we_se.html
    """
    if prefs is None:
        return
    else:
        cipher = frozenset(['AES256', 'AES192', 'AES128',
         'CAMELLIA256', 'CAMELLIA192',
         'TWOFISH', '3DES'])
        digest = frozenset(['SHA512', 'SHA384', 'SHA256', 'SHA224', 'RMD160',
         'SHA1'])
        compress = frozenset(['BZIP2', 'ZLIB', 'ZIP', 'Uncompressed'])
        trust = frozenset(['gpg', 'classic', 'direct', 'always', 'auto'])
        pinentry = frozenset(['loopback'])
        all = frozenset([cipher, digest, compress, trust, pinentry])
        if isinstance(prefs, str):
            prefs = set(prefs.split())
        elif isinstance(prefs, list):
            prefs = set(prefs)
        else:
            msg = 'prefs must be list of strings, or space-separated string'
            log.error('parsers._check_preferences(): %s' % message)
            raise TypeError(message)
        if not pref_type:
            pref_type = 'all'
        allowed = str()
        if pref_type == 'cipher':
            allowed += (' ').join(prefs.intersection(cipher))
        if pref_type == 'digest':
            allowed += (' ').join(prefs.intersection(digest))
        if pref_type == 'compress':
            allowed += (' ').join(prefs.intersection(compress))
        if pref_type == 'trust':
            allowed += (' ').join(prefs.intersection(trust))
        if pref_type == 'pinentry':
            allowed += (' ').join(prefs.intersection(pinentry))
        if pref_type == 'all':
            allowed += (' ').join(prefs.intersection(all))
        return allowed


def _fix_unsafe(shell_input):
    """Find characters used to escape from a string into a shell, and wrap them in
    quotes if they exist. Regex pilfered from Python3 :mod:`shlex` module.

    :param str shell_input: The input intended for the GnuPG process.
    """
    _unsafe = re.compile('[^\\w@%+=:,./-]', 256)
    try:
        if len(_unsafe.findall(shell_input)) == 0:
            return shell_input.strip()
        else:
            clean = "'" + shell_input.replace("'", '\'"\'"\'') + "'"
            return clean

    except TypeError:
        return

    return


def _hyphenate(input, add_prefix=False):
    """Change underscores to hyphens so that object attributes can be easily
    tranlated to GPG option names.

    :param str input: The attribute to hyphenate.
    :param bool add_prefix: If True, add leading hyphens to the input.
    :rtype: str
    :return: The ``input`` with underscores changed to hyphens.
    """
    ret = '--' if add_prefix else ''
    ret += input.replace('_', '-')
    return ret


def _is_allowed(input):
    """Check that an option or argument given to GPG is in the set of allowed
    options, the latter being a strict subset of the set of all options known
    to GPG.

    :param str input: An input meant to be parsed as an option or flag to the
                      GnuPG process. Should be formatted the same as an option
                      or flag to the commandline gpg, i.e. "--encrypt-files".

    :ivar frozenset gnupg_options: All known GPG options and flags.

    :ivar frozenset allowed: All allowed GPG options and flags, e.g. all GPG
                             options and flags which we are willing to
                             acknowledge and parse. If we want to support a
                             new option, it will need to have its own parsing
                             class and its name will need to be added to this
                             set.

    :raises: :exc:`UsageError` if **input** is not a subset of the hard-coded
             set of all GnuPG options in :func:`_get_all_gnupg_options`.

             :exc:`ProtectedOption` if **input** is not in the set of allowed
             options.

    :rtype: str
    :return: The original **input** parameter, unmodified and unsanitized, if
             no errors occur.
    """
    gnupg_options = _get_all_gnupg_options()
    allowed = _get_options_group('allowed')
    try:
        assert allowed.issubset(gnupg_options)
    except AssertionError:
        raise UsageError("'allowed' isn't a subset of known options, diff: %s" % allowed.difference(gnupg_options))

    if not isinstance(input, str):
        input = (' ').join([ x for x in input ])
    if isinstance(input, str):
        if input.find('_') > 0:
            if not input.startswith('--'):
                hyphenated = _hyphenate(input, add_prefix=True)
            else:
                hyphenated = _hyphenate(input)
        else:
            hyphenated = input
            try:
                assert hyphenated in allowed
            except AssertionError as ae:
                dropped = _fix_unsafe(hyphenated)
                log.warn("_is_allowed(): Dropping option '%s'..." % dropped)
                raise ProtectedOption("Option '%s' not supported." % dropped)
            else:
                return input

    return


def _is_hex(string):
    """Check that a string is hexadecimal, with alphabetic characters
    in either upper or lower case and without whitespace.

    :param str string: The string to check.
    """
    if HEXADECIMAL.match(string):
        return True
    return False


def _is_string(thing):
    """Python character arrays are a mess.

    If Python2, check if **thing** is an :obj:`unicode` or a :obj:`str`.
    If Python3, check if **thing** is a :obj:`str`.

    :param thing: The thing to check.
    :returns: ``True`` if **thing** is a string according to whichever version
              of Python we're running in.
    """
    if _util._py3k:
        return isinstance(thing, str)
    else:
        return isinstance(thing, basestring)


def _sanitise(*args):
    """Take an arg or the key portion of a kwarg and check that it is in the
    set of allowed GPG options and flags, and that it has the correct
    type. Then, attempt to escape any unsafe characters. If an option is not
    allowed, drop it with a logged warning. Returns a dictionary of all
    sanitised, allowed options.

    Each new option that we support that is not a boolean, but instead has
    some additional inputs following it, i.e. "--encrypt-file foo.txt", will
    need some basic safety checks added here.

    GnuPG has three-hundred and eighteen commandline flags. Also, not all
    implementations of OpenPGP parse PGP packets and headers in the same way,
    so there is added potential there for messing with calls to GPG.

    For information on the PGP message format specification, see
    :rfc:`1991`.

    If you're asking, "Is this *really* necessary?": No, not really -- we could
    just follow the security precautions recommended by `this xkcd`__.

     __ https://xkcd.com/1181/

    :param str args: (optional) The boolean arguments which will be passed to
                     the GnuPG process.
    :rtype: str
    :returns: ``sanitised``
    """

    def _check_option(arg, value):
        """Check that a single ``arg`` is an allowed option.

        If it is allowed, quote out any escape characters in ``value``, and
        add the pair to :ivar:`sanitised`. Otherwise, drop them.

        :param str arg: The arguments which will be passed to the GnuPG
                        process, and, optionally their corresponding values.
                        The values are any additional arguments following the
                        GnuPG option or flag. For example, if we wanted to
                        pass ``"--encrypt --recipient isis@leap.se"`` to
                        GnuPG, then ``"--encrypt"`` would be an arg without a
                        value, and ``"--recipient"`` would also be an arg,
                        with a value of ``"isis@leap.se"``.

        :ivar list checked: The sanitised, allowed options and values.
        :rtype: str
        :returns: A string of the items in ``checked``, delimited by spaces.
        """
        checked = str()
        none_options = _get_options_group('none_options')
        hex_options = _get_options_group('hex_options')
        hex_or_none_options = _get_options_group('hex_or_none_options')
        if not _util._py3k:
            if not isinstance(arg, list) and isinstance(arg, unicode):
                arg = str(arg)
        try:
            flag = _is_allowed(arg)
            assert flag is not None, '_check_option(): got None for flag'
        except (AssertionError, ProtectedOption) as error:
            log.warn('_check_option(): %s' % str(error))

        checked += flag + ' '
        if _is_string(value):
            values = value.split(' ')
            for v in values:
                if flag in none_options and v is None:
                    continue
                if flag in hex_options:
                    if _is_hex(v):
                        checked += v + ' '
                    else:
                        log.debug("'%s %s' not hex." % (flag, v))
                        if flag in hex_or_none_options and v is None:
                            log.debug("Allowing '%s' for all keys" % flag)
                    continue
                else:
                    if flag in ('--keyserver', ):
                        host = _check_keyserver(v)
                        if host:
                            log.debug('Setting keyserver: %s' % host)
                            checked += v + ' '
                        else:
                            log.debug('Dropping keyserver: %s' % v)
                        continue
                    val = _fix_unsafe(v)
                    try:
                        assert val is not None
                        assert not val.isspace()
                        assert v is not None
                        assert not v.isspace()
                    except:
                        log.debug('Dropping %s %s' % (flag, v))
                        continue

                if flag in ('--encrypt', '--encrypt-files', '--decrypt', '--decrypt-files',
                            '--import', '--verify'):
                    if _util._is_file(val) or flag == '--verify' and val == '-':
                        checked += val + ' '
                    else:
                        log.debug('%s not file: %s' % (flag, val))
                elif flag in ('--cipher-algo', '--personal-cipher-prefs', '--personal-cipher-preferences'):
                    legit_algos = _check_preferences(val, 'cipher')
                    if legit_algos:
                        checked += legit_algos + ' '
                    else:
                        log.debug("'%s' is not cipher" % val)
                elif flag in ('--compress-algo', '--compression-algo', '--personal-compress-prefs',
                              '--personal-compress-preferences'):
                    legit_algos = _check_preferences(val, 'compress')
                    if legit_algos:
                        checked += legit_algos + ' '
                    else:
                        log.debug("'%s' not compress algo" % val)
                elif flag == '--trust-model':
                    legit_models = _check_preferences(val, 'trust')
                    if legit_models:
                        checked += legit_models + ' '
                    else:
                        log.debug('%r is not a trust model', val)
                elif flag == '--pinentry-mode':
                    legit_modes = _check_preferences(val, 'pinentry')
                    if legit_modes:
                        checked += legit_modes + ' '
                    else:
                        log.debug('%r is not a pinentry mode', val)
                else:
                    checked += val + ' '
                    log.debug('_check_option(): No checks for %s' % val)

        return checked.rstrip(' ')

    is_flag = lambda x: x.startswith('--')

    def _make_filo(args_string):
        filo = arg.split(' ')
        filo.reverse()
        log.debug('_make_filo(): Converted to reverse list: %s' % filo)
        return filo

    def _make_groups--- This code section failed: ---

 L. 396         0  BUILD_MAP_0           0  None
                3  STORE_FAST            1  'groups'

 L. 397         6  SETUP_LOOP          412  'to 421'
                9  LOAD_GLOBAL           0  'len'
               12  LOAD_FAST             0  'filo'
               15  CALL_FUNCTION_1       1  None
               18  LOAD_CONST               1
               21  COMPARE_OP            5  >=
               24  POP_JUMP_IF_FALSE   420  'to 420'

 L. 398        27  LOAD_FAST             0  'filo'
               30  LOAD_ATTR             1  'pop'
               33  CALL_FUNCTION_0       0  None
               36  STORE_FAST            2  'last'

 L. 399        39  LOAD_DEREF            0  'is_flag'
               42  LOAD_FAST             2  'last'
               45  CALL_FUNCTION_1       1  None
               48  POP_JUMP_IF_FALSE   390  'to 390'

 L. 400        51  LOAD_GLOBAL           2  'log'
               54  LOAD_ATTR             3  'debug'
               57  LOAD_CONST               'Got arg: %s'
               60  LOAD_FAST             2  'last'
               63  BINARY_MODULO    
               64  CALL_FUNCTION_1       1  None
               67  POP_TOP          

 L. 401        68  LOAD_FAST             2  'last'
               71  LOAD_CONST               '--verify'
               74  COMPARE_OP            2  ==
               77  POP_JUMP_IF_FALSE   184  'to 184'

 L. 402        80  LOAD_GLOBAL           4  'str'
               83  LOAD_FAST             0  'filo'
               86  LOAD_ATTR             1  'pop'
               89  CALL_FUNCTION_0       0  None
               92  CALL_FUNCTION_1       1  None
               95  LOAD_FAST             1  'groups'
               98  LOAD_FAST             2  'last'
              101  STORE_SUBSCR     

 L. 404       102  LOAD_GLOBAL           0  'len'
              105  LOAD_FAST             0  'filo'
              108  CALL_FUNCTION_1       1  None
              111  LOAD_CONST               1
              114  COMPARE_OP            5  >=
              117  POP_JUMP_IF_FALSE   197  'to 197'
              120  LOAD_FAST             0  'filo'
              123  LOAD_GLOBAL           0  'len'
              126  LOAD_FAST             0  'filo'
              129  CALL_FUNCTION_1       1  None
              132  LOAD_CONST               1
              135  BINARY_SUBTRACT  
              136  BINARY_SUBSCR    
              137  LOAD_CONST               '-'
              140  COMPARE_OP            2  ==
            143_0  COME_FROM           117  '117'
              143  POP_JUMP_IF_FALSE   197  'to 197'

 L. 405       146  LOAD_FAST             1  'groups'
              149  LOAD_FAST             2  'last'
              152  DUP_TOPX_2            2  None
              155  BINARY_SUBSCR    
              156  LOAD_GLOBAL           4  'str'
              159  LOAD_CONST               ' - '
              162  CALL_FUNCTION_1       1  None
              165  INPLACE_ADD      
              166  ROT_THREE        
              167  STORE_SUBSCR     

 L. 406       168  LOAD_FAST             0  'filo'
              171  LOAD_ATTR             1  'pop'
              174  CALL_FUNCTION_0       0  None
              177  POP_TOP          
              178  JUMP_ABSOLUTE       197  'to 197'
              181  JUMP_FORWARD         13  'to 197'

 L. 408       184  LOAD_GLOBAL           4  'str'
              187  CALL_FUNCTION_0       0  None
              190  LOAD_FAST             1  'groups'
              193  LOAD_FAST             2  'last'
              196  STORE_SUBSCR     
            197_0  COME_FROM           181  '181'

 L. 409       197  SETUP_LOOP          217  'to 417'
              200  LOAD_GLOBAL           0  'len'
              203  LOAD_FAST             0  'filo'
              206  CALL_FUNCTION_1       1  None
              209  LOAD_CONST               1
              212  COMPARE_OP            4  >
              215  POP_JUMP_IF_FALSE   305  'to 305'
              218  LOAD_DEREF            0  'is_flag'
              221  LOAD_FAST             0  'filo'
              224  LOAD_GLOBAL           0  'len'
              227  LOAD_FAST             0  'filo'
              230  CALL_FUNCTION_1       1  None
              233  LOAD_CONST               1
              236  BINARY_SUBTRACT  
              237  BINARY_SUBSCR    
              238  CALL_FUNCTION_1       1  None
              241  UNARY_NOT        
            242_0  COME_FROM           215  '215'
              242  POP_JUMP_IF_FALSE   305  'to 305'

 L. 410       245  LOAD_GLOBAL           2  'log'
              248  LOAD_ATTR             3  'debug'
              251  LOAD_CONST               'Got value: %s'
              254  LOAD_FAST             0  'filo'
              257  LOAD_GLOBAL           0  'len'
              260  LOAD_FAST             0  'filo'
              263  CALL_FUNCTION_1       1  None
              266  LOAD_CONST               1
              269  BINARY_SUBTRACT  
              270  BINARY_SUBSCR    
              271  BINARY_MODULO    
              272  CALL_FUNCTION_1       1  None
              275  POP_TOP          

 L. 411       276  LOAD_FAST             1  'groups'
              279  LOAD_FAST             2  'last'
              282  DUP_TOPX_2            2  None
              285  BINARY_SUBSCR    
              286  LOAD_FAST             0  'filo'
              289  LOAD_ATTR             1  'pop'
              292  CALL_FUNCTION_0       0  None
              295  LOAD_CONST               ' '
              298  BINARY_ADD       
              299  INPLACE_ADD      
              300  ROT_THREE        
              301  STORE_SUBSCR     
              302  JUMP_BACK           200  'to 200'
              305  POP_BLOCK        

 L. 413       306  LOAD_GLOBAL           0  'len'
              309  LOAD_FAST             0  'filo'
              312  CALL_FUNCTION_1       1  None
              315  LOAD_CONST               1
              318  COMPARE_OP            2  ==
              321  POP_JUMP_IF_FALSE   417  'to 417'
              324  LOAD_DEREF            0  'is_flag'
              327  LOAD_FAST             0  'filo'
              330  LOAD_CONST               0
              333  BINARY_SUBSCR    
              334  CALL_FUNCTION_1       1  None
              337  UNARY_NOT        
            338_0  COME_FROM           321  '321'
              338  POP_JUMP_IF_FALSE   417  'to 417'

 L. 414       341  LOAD_GLOBAL           2  'log'
              344  LOAD_ATTR             3  'debug'
              347  LOAD_CONST               'Got value: %s'
              350  LOAD_FAST             0  'filo'
              353  LOAD_CONST               0
              356  BINARY_SUBSCR    
              357  BINARY_MODULO    
              358  CALL_FUNCTION_1       1  None
              361  POP_TOP          

 L. 415       362  LOAD_FAST             1  'groups'
              365  LOAD_FAST             2  'last'
              368  DUP_TOPX_2            2  None
              371  BINARY_SUBSCR    
              372  LOAD_FAST             0  'filo'
              375  LOAD_ATTR             1  'pop'
              378  CALL_FUNCTION_0       0  None
              381  INPLACE_ADD      
              382  ROT_THREE        
              383  STORE_SUBSCR     
              384  JUMP_ABSOLUTE       417  'to 417'
            387_0  COME_FROM           197  '197'
              387  JUMP_BACK             9  'to 9'

 L. 417       390  LOAD_GLOBAL           2  'log'
              393  LOAD_ATTR             5  'warn'
              396  LOAD_CONST               '_make_groups(): Got solitary value: %s'
              399  LOAD_FAST             2  'last'
              402  BINARY_MODULO    
              403  CALL_FUNCTION_1       1  None
              406  POP_TOP          

 L. 418       407  LOAD_FAST             2  'last'
              410  LOAD_FAST             1  'groups'
              413  LOAD_CONST               'xxx'
              416  STORE_SUBSCR     
              417  JUMP_BACK             9  'to 9'
              420  POP_BLOCK        
            421_0  COME_FROM             6  '6'

 L. 419       421  LOAD_FAST             1  'groups'
              424  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 387_0

    def _check_groups(groups):
        log.debug('Got groups: %s' % groups)
        checked_groups = []
        for a, v in groups.items():
            v = None if len(v) == 0 else v
            safe = _check_option(a, v)
            if safe is not None and not safe.strip() == '':
                log.debug('Appending option: %s' % safe)
                checked_groups.append(safe)
            else:
                log.warn("Dropped option: '%s %s'" % (a, v))

        return checked_groups

    if args is not None:
        option_groups = {}
        for arg in args:
            if not _util._py3k and isinstance(arg, basestring) or _util._py3k and isinstance(arg, str):
                log.debug('Got arg string: %s' % arg)
                if arg.find(' ') > 0:
                    filo = _make_filo(arg)
                    option_groups.update(_make_groups(filo))
                else:
                    option_groups.update({arg: ''})
            elif isinstance(arg, list):
                log.debug('Got arg list: %s' % arg)
                arg.reverse()
                option_groups.update(_make_groups(arg))
            else:
                log.warn("Got non-str/list arg: '%s', type '%s'" % (
                 arg, type(arg)))

        checked = _check_groups(option_groups)
        sanitised = (' ').join(x for x in checked)
        return sanitised
    else:
        log.debug('Got None for args')
        return


def _sanitise_list(arg_list):
    """A generator for iterating through a list of gpg options and sanitising
    them.

    :param list arg_list: A list of options and flags for GnuPG.
    :rtype: generator
    :returns: A generator whose next() method returns each of the items in
              ``arg_list`` after calling ``_sanitise()`` with that item as a
              parameter.
    """
    if isinstance(arg_list, list):
        for arg in arg_list:
            safe_arg = _sanitise(arg)
            if safe_arg != '':
                yield safe_arg


def _get_options_group(group=None):
    """Get a specific group of options which are allowed."""
    hex_options = frozenset(['--check-sigs',
     '--default-key',
     '--default-recipient',
     '--delete-keys',
     '--delete-secret-keys',
     '--delete-secret-and-public-keys',
     '--desig-revoke',
     '--export',
     '--export-secret-keys',
     '--export-secret-subkeys',
     '--fingerprint',
     '--gen-revoke',
     '--hidden-encrypt-to',
     '--hidden-recipient',
     '--list-key',
     '--list-keys',
     '--list-public-keys',
     '--list-secret-keys',
     '--list-sigs',
     '--recipient',
     '--recv-keys',
     '--send-keys',
     '--edit-key',
     '--sign-key'])
    unchecked_options = frozenset(['--list-options',
     '--passphrase-fd',
     '--status-fd',
     '--verify-options',
     '--command-fd'])
    other_options = frozenset(['--debug-level',
     '--keyserver'])
    dir_options = frozenset(['--homedir'])
    keyring_options = frozenset(['--keyring',
     '--primary-keyring',
     '--secret-keyring',
     '--trustdb-name'])
    file_or_none_options = frozenset(['--decrypt',
     '--decrypt-files',
     '--encrypt',
     '--encrypt-files',
     '--import',
     '--verify',
     '--verify-files',
     '--output'])
    pref_options = frozenset(['--digest-algo',
     '--cipher-algo',
     '--compress-algo',
     '--compression-algo',
     '--cert-digest-algo',
     '--personal-digest-prefs',
     '--personal-digest-preferences',
     '--personal-cipher-prefs',
     '--personal-cipher-preferences',
     '--personal-compress-prefs',
     '--personal-compress-preferences',
     '--pinentry-mode',
     '--print-md',
     '--trust-model'])
    none_options = frozenset(['--allow-loopback-pinentry',
     '--always-trust',
     '--armor',
     '--armour',
     '--batch',
     '--check-sigs',
     '--check-trustdb',
     '--clearsign',
     '--debug-all',
     '--default-recipient-self',
     '--detach-sign',
     '--export',
     '--export-ownertrust',
     '--export-secret-keys',
     '--export-secret-subkeys',
     '--fingerprint',
     '--fixed-list-mode',
     '--gen-key',
     '--import-ownertrust',
     '--list-config',
     '--list-key',
     '--list-keys',
     '--list-packets',
     '--list-public-keys',
     '--list-secret-keys',
     '--list-sigs',
     '--lock-multiple',
     '--lock-never',
     '--lock-once',
     '--no-default-keyring',
     '--no-default-recipient',
     '--no-emit-version',
     '--no-options',
     '--no-tty',
     '--no-use-agent',
     '--no-verbose',
     '--print-mds',
     '--quiet',
     '--sign',
     '--symmetric',
     '--throw-keyids',
     '--use-agent',
     '--verbose',
     '--version',
     '--with-colons',
     '--yes'])
    hex_or_none_options = hex_options.intersection(none_options)
    allowed = hex_options.union(unchecked_options, other_options, dir_options, keyring_options, file_or_none_options, pref_options, none_options)
    if group and group in locals().keys():
        return locals()[group]


def _get_all_gnupg_options():
    """Get all GnuPG options and flags.

    This is hardcoded within a local scope to reduce the chance of a tampered
    GnuPG binary reporting falsified option sets, i.e. because certain options
    (namedly the ``--no-options`` option, which prevents the usage of gpg.conf
    files) are necessary and statically specified in
    :meth:`gnupg._meta.GPGBase._make_args`, if the inputs into Python are
    already controlled, and we were to summon the GnuPG binary to ask it for
    its options, it would be possible to receive a falsified options set
    missing the ``--no-options`` option in response. This seems unlikely, and
    the method is stupid and ugly, but at least we'll never have to debug
    whether or not an option *actually* disappeared in a different GnuPG
    version, or some funny business is happening.

    These are the options as of GnuPG 1.4.12; the current stable branch of the
    2.1.x tree contains a few more -- if you need them you'll have to add them
    in here.

    :type gnupg_options: frozenset
    :ivar gnupg_options: All known GPG options and flags.
    :rtype: frozenset
    :returns: ``gnupg_options``
    """
    three_hundred_eighteen = ('\n--allow-freeform-uid              --multifile\n--allow-multiple-messages         --no\n--allow-multisig-verification     --no-allow-freeform-uid\n--allow-non-selfsigned-uid        --no-allow-multiple-messages\n--allow-secret-key-import         --no-allow-non-selfsigned-uid\n--always-trust                    --no-armor\n--armor                           --no-armour\n--armour                          --no-ask-cert-expire\n--ask-cert-expire                 --no-ask-cert-level\n--ask-cert-level                  --no-ask-sig-expire\n--ask-sig-expire                  --no-auto-check-trustdb\n--attribute-fd                    --no-auto-key-locate\n--attribute-file                  --no-auto-key-retrieve\n--auto-check-trustdb              --no-batch\n--auto-key-locate                 --no-comments\n--auto-key-retrieve               --no-default-keyring\n--batch                           --no-default-recipient\n--bzip2-compress-level            --no-disable-mdc\n--bzip2-decompress-lowmem         --no-emit-version\n--card-edit                       --no-encrypt-to\n--card-status                     --no-escape-from-lines\n--cert-digest-algo                --no-expensive-trust-checks\n--cert-notation                   --no-expert\n--cert-policy-url                 --no-force-mdc\n--change-pin                      --no-force-v3-sigs\n--charset                         --no-force-v4-certs\n--check-sig                       --no-for-your-eyes-only\n--check-sigs                      --no-greeting\n--check-trustdb                   --no-groups\n--cipher-algo                     --no-literal\n--clearsign                       --no-mangle-dos-filenames\n--command-fd                      --no-mdc-warning\n--command-file                    --no-options\n--comment                         --no-permission-warning\n--completes-needed                --no-pgp2\n--compress-algo                   --no-pgp6\n--compression-algo                --no-pgp7\n--compress-keys                   --no-pgp8\n--compress-level                  --no-random-seed-file\n--compress-sigs                   --no-require-backsigs\n--ctapi-driver                    --no-require-cross-certification\n--dearmor                         --no-require-secmem\n--dearmour                        --no-rfc2440-text\n--debug                           --no-secmem-warning\n--debug-all                       --no-show-notation\n--debug-ccid-driver               --no-show-photos\n--debug-level                     --no-show-policy-url\n--decrypt                         --no-sig-cache\n--decrypt-files                   --no-sig-create-check\n--default-cert-check-level        --no-sk-comments\n--default-cert-expire             --no-strict\n--default-cert-level              --notation-data\n--default-comment                 --not-dash-escaped\n--default-key                     --no-textmode\n--default-keyserver-url           --no-throw-keyid\n--default-preference-list         --no-throw-keyids\n--default-recipient               --no-tty\n--default-recipient-self          --no-use-agent\n--default-sig-expire              --no-use-embedded-filename\n--delete-keys                     --no-utf8-strings\n--delete-secret-and-public-keys   --no-verbose\n--delete-secret-keys              --no-version\n--desig-revoke                    --openpgp\n--detach-sign                     --options\n--digest-algo                     --output\n--disable-ccid                    --override-session-key\n--disable-cipher-algo             --passphrase\n--disable-dsa2                    --passphrase-fd\n--disable-mdc                     --passphrase-file\n--disable-pubkey-algo             --passphrase-repeat\n--display                         --pcsc-driver\n--display-charset                 --personal-cipher-preferences\n--dry-run                         --personal-cipher-prefs\n--dump-options                    --personal-compress-preferences\n--edit-key                        --personal-compress-prefs\n--emit-version                    --personal-digest-preferences\n--enable-dsa2                     --personal-digest-prefs\n--enable-progress-filter          --pgp2\n--enable-special-filenames        --pgp6\n--enarmor                         --pgp7\n--enarmour                        --pgp8\n--encrypt                         --photo-viewer\n--encrypt-files                   --pipemode\n--encrypt-to                      --preserve-permissions\n--escape-from-lines               --primary-keyring\n--exec-path                       --print-md\n--exit-on-status-write-error      --print-mds\n--expert                          --quick-random\n--export                          --quiet\n--export-options                  --reader-port\n--export-ownertrust               --rebuild-keydb-caches\n--export-secret-keys              --recipient\n--export-secret-subkeys           --recv-keys\n--fast-import                     --refresh-keys\n--fast-list-mode                  --remote-user\n--fetch-keys                      --require-backsigs\n--fingerprint                     --require-cross-certification\n--fixed-list-mode                 --require-secmem\n--fix-trustdb                     --rfc1991\n--force-mdc                       --rfc2440\n--force-ownertrust                --rfc2440-text\n--force-v3-sigs                   --rfc4880\n--force-v4-certs                  --run-as-shm-coprocess\n--for-your-eyes-only              --s2k-cipher-algo\n--gen-key                         --s2k-count\n--gen-prime                       --s2k-digest-algo\n--gen-random                      --s2k-mode\n--gen-revoke                      --search-keys\n--gnupg                           --secret-keyring\n--gpg-agent-info                  --send-keys\n--gpgconf-list                    --set-filename\n--gpgconf-test                    --set-filesize\n--group                           --set-notation\n--help                            --set-policy-url\n--hidden-encrypt-to               --show-keyring\n--hidden-recipient                --show-notation\n--homedir                         --show-photos\n--honor-http-proxy                --show-policy-url\n--ignore-crc-error                --show-session-key\n--ignore-mdc-error                --sig-keyserver-url\n--ignore-time-conflict            --sign\n--ignore-valid-from               --sign-key\n--import                          --sig-notation\n--import-options                  --sign-with\n--import-ownertrust               --sig-policy-url\n--interactive                     --simple-sk-checksum\n--keyid-format                    --sk-comments\n--keyring                         --skip-verify\n--keyserver                       --status-fd\n--keyserver-options               --status-file\n--lc-ctype                        --store\n--lc-messages                     --strict\n--limit-card-insert-tries         --symmetric\n--list-config                     --temp-directory\n--list-key                        --textmode\n--list-keys                       --throw-keyid\n--list-only                       --throw-keyids\n--list-options                    --trustdb-name\n--list-ownertrust                 --trusted-key\n--list-packets                    --trust-model\n--list-public-keys                --try-all-secrets\n--list-secret-keys                --ttyname\n--list-sig                        --ttytype\n--list-sigs                       --ungroup\n--list-trustdb                    --update-trustdb\n--load-extension                  --use-agent\n--local-user                      --use-embedded-filename\n--lock-multiple                   --user\n--lock-never                      --utf8-strings\n--lock-once                       --verbose\n--logger-fd                       --verify\n--logger-file                     --verify-files\n--lsign-key                       --verify-options\n--mangle-dos-filenames            --version\n--marginals-needed                --warranty\n--max-cert-depth                  --with-colons\n--max-output                      --with-fingerprint\n--merge-only                      --with-key-data\n--min-cert-level                  --yes\n').split()
    three_hundred_eighteen.append('--export-ownertrust')
    three_hundred_eighteen.append('--import-ownertrust')
    three_hundred_eighteen.append('--pinentry-mode')
    three_hundred_eighteen.append('--allow-loopback-pinentry')
    gnupg_options = frozenset(three_hundred_eighteen)
    return gnupg_options


def nodata(status_code):
    """Translate NODATA status codes from GnuPG to messages."""
    lookup = {'1': 'No armored data.', 
       '2': 'Expected a packet but did not find one.', 
       '3': 'Invalid packet found, this may indicate a non OpenPGP message.', 
       '4': 'Signature expected but not found.'}
    for key, value in lookup.items():
        if str(status_code) == key:
            return value


def progress(status_code):
    """Translate PROGRESS status codes from GnuPG to messages."""
    lookup = {'pk_dsa': 'DSA key generation', 
       'pk_elg': 'Elgamal key generation', 
       'primegen': 'Prime generation', 
       'need_entropy': 'Waiting for new entropy in the RNG', 
       'tick': 'Generic tick without any special meaning - still working.', 
       'starting_agent': 'A gpg-agent was started.', 
       'learncard': 'gpg-agent or gpgsm is learning the smartcard data.', 
       'card_busy': 'A smartcard is still working.'}
    for key, value in lookup.items():
        if str(status_code) == key:
            return value


class KeyExpirationInterface(object):
    """ Interface that guards against misuse of --edit-key combined with --command-fd"""

    def __init__(self, expiration_time, passphrase=None):
        self._passphrase = passphrase
        self._expiration_time = expiration_time
        self._clean_key_expiration_option()

    def _clean_key_expiration_option(self):
        """validates the expiration option supplied"""
        allowed_entry = re.findall('^(\\d+)(|w|m|y)$', self._expiration_time)
        if not allowed_entry:
            raise UsageError('Key expiration option: %s is not valid' % self._expiration_time)

    def _input_passphrase(self, _input):
        if self._passphrase:
            return '%s%s\n' % (_input, self._passphrase)
        return _input

    def _main_key_command(self):
        main_key_input = 'expire\n%s\n' % self._expiration_time
        return self._input_passphrase(main_key_input)

    def _sub_key_command(self, sub_key_number):
        sub_key_input = 'key %d\nexpire\n%s\n' % (sub_key_number, self._expiration_time)
        return self._input_passphrase(sub_key_input)

    def gpg_interactive_input(self, sub_keys_number):
        """ processes series of inputs normally supplied on --edit-key but passed through stdin
            this ensures that no other --edit-key command is actually passing through.
        """
        deselect_sub_key = 'key 0\n'
        _input = self._main_key_command()
        for sub_key_number in range(1, sub_keys_number + 1):
            _input += self._sub_key_command(sub_key_number) + deselect_sub_key

        return '%ssave\n' % _input


class KeyExpirationResult(object):
    """Handle status messages for key expiry
        It does not really have a job, but just to conform to the API
    """

    def __init__(self, gpg):
        self._gpg = gpg
        self.status = 'ok'

    def _handle_status(self, key, value):
        """Parse a status code from the attached GnuPG process.

        :raises: :exc:`~exceptions.ValueError` if the status message is unknown.
        """
        if key in ('USERID_HINT', 'NEED_PASSPHRASE', 'GET_HIDDEN', 'SIGEXPIRED', 'KEYEXPIRED',
                   'GOOD_PASSPHRASE', 'GOT_IT', 'GET_LINE'):
            pass
        elif key in ('BAD_PASSPHRASE', 'MISSING_PASSPHRASE'):
            self.status = key.replace('_', ' ').lower()
        else:
            self.status = 'failed'
            raise ValueError('Unknown status message: %r' % key)


class KeySigningResult(object):
    """Handle status messages for key singing
    """

    def __init__(self, gpg):
        self._gpg = gpg
        self.status = 'ok'

    def _handle_status(self, key, value):
        """Parse a status code from the attached GnuPG process.

        :raises: :exc:`~exceptions.ValueError` if the status message is unknown.
        """
        if key in ('USERID_HINT', 'NEED_PASSPHRASE', 'ALREADY_SIGNED', 'GOOD_PASSPHRASE',
                   'GOT_IT', 'GET_BOOL'):
            pass
        elif key in ('BAD_PASSPHRASE', 'MISSING_PASSPHRASE'):
            self.status = '%s: %s' % (key.replace('_', ' ').lower(), value)
        else:
            self.status = 'failed'
            raise ValueError('Key signing, unknown status message: %r ::%s' % (key, value))


class GenKey(object):
    """Handle status messages for key generation.

    Calling the ``__str__()`` method of this class will return the generated
    key's fingerprint, or a status string explaining the results.
    """

    def __init__(self, gpg):
        self._gpg = gpg
        self.type = None
        self.fingerprint = None
        self.status = ''
        self.subkey_created = False
        self.primary_created = False
        self.keyring = None
        self.secring = None
        return

    def __nonzero__(self):
        if self.fingerprint:
            return True
        return False

    __bool__ = __nonzero__

    def __str__(self):
        if self.fingerprint:
            return self.fingerprint
        else:
            if self.status is not None:
                return self.status
            else:
                return False

            return

    def _handle_status(self, key, value):
        """Parse a status code from the attached GnuPG process.

        :raises: :exc:`~exceptions.ValueError` if the status message is unknown.
        """
        if key in 'GOOD_PASSPHRASE':
            pass
        elif key == 'KEY_CONSIDERED':
            self.status = key.replace('_', ' ').lower()
        elif key == 'KEY_NOT_CREATED':
            self.status = 'key not created'
        elif key == 'KEY_CREATED':
            self.type, self.fingerprint = value.split()
            self.status = 'key created'
        elif key == 'NODATA':
            self.status = nodata(value)
        elif key == 'PROGRESS':
            self.status = progress(value.split(' ', 1)[0])
        elif key == 'PINENTRY_LAUNCHED':
            log.warn('GnuPG has just attempted to launch whichever pinentry program you have configured, in order to obtain the passphrase for this key.  If you did not use the `passphrase=` parameter, please try doing so.  Otherwise, see Issues #122 and #137:\nhttps://github.com/isislovecruft/python-gnupg/issues/122\nhttps://github.com/isislovecruft/python-gnupg/issues/137')
            self.status = 'key not created'
        elif key.startswith('TRUST_') or key.startswith('PKA_TRUST_') or key == 'NEWSIG':
            pass
        else:
            raise ValueError('Unknown status message: %r' % key)
        if self.type in ('B', 'P'):
            self.primary_created = True
        if self.type in ('B', 'S'):
            self.subkey_created = True


class DeleteResult(object):
    """Handle status messages for --delete-keys and --delete-secret-keys"""

    def __init__(self, gpg):
        self._gpg = gpg
        self.status = 'ok'

    def __str__(self):
        return self.status

    problem_reason = {'1': 'No such key', '2': 'Must delete secret key first', 
       '3': 'Ambigious specification'}

    def _handle_status(self, key, value):
        """Parse a status code from the attached GnuPG process.

        :raises: :exc:`~exceptions.ValueError` if the status message is unknown.
        """
        if key in ('DELETE_PROBLEM', 'KEY_CONSIDERED'):
            self.status = self.problem_reason.get(value, 'Unknown error: %r' % value)
        else:
            raise ValueError('Unknown status message: %r' % key)


class Sign(object):
    """Parse GnuPG status messages for signing operations.

    :param gpg: An instance of :class:`gnupg.GPG`.
    """
    sig_type = None
    sig_algo = None
    sig_hash_also = None
    fingerprint = None
    timestamp = None
    what = None
    status = None

    def __init__(self, gpg):
        self._gpg = gpg

    def __nonzero__(self):
        """Override the determination for truthfulness evaluation.

        :rtype: bool
        :returns: True if we have a valid signature, False otherwise.
        """
        return self.fingerprint is not None

    __bool__ = __nonzero__

    def __str__(self):
        return self.data.decode(self._gpg._encoding, self._gpg._decode_errors)

    def _handle_status(self, key, value):
        """Parse a status code from the attached GnuPG process.

        :raises: :exc:`~exceptions.ValueError` if the status message is unknown.
        """
        if key in ('USERID_HINT', 'NEED_PASSPHRASE', 'BAD_PASSPHRASE', 'GOOD_PASSPHRASE',
                   'MISSING_PASSPHRASE', 'PINENTRY_LAUNCHED', 'BEGIN_SIGNING', 'CARDCTRL',
                   'INV_SGNR', 'SIGEXPIRED', 'KEY_CONSIDERED'):
            self.status = key.replace('_', ' ').lower()
        elif key == 'SIG_CREATED':
            self.sig_type, self.sig_algo, self.sig_hash_algo, self.what, self.timestamp, self.fingerprint = value.split()
        elif key == 'KEYEXPIRED':
            self.status = 'skipped signing key, key expired'
            if value is not None and len(value) > 0:
                self.status += (' on {}').format(str(value))
        elif key == 'KEYREVOKED':
            self.status = 'skipped signing key, key revoked'
            if value is not None and len(value) > 0:
                self.status += (' on {}').format(str(value))
        elif key == 'NODATA':
            self.status = nodata(value)
        elif key == 'PROGRESS':
            self.status = progress(value.split(' ', 1)[0])
        else:
            raise ValueError('Unknown status message: %r' % key)
        return


class ListKeys(list):
    """Handle status messages for --list-keys.

    Handles pub and uid (relating the latter to the former).  Don't care about
    the following attributes/status messages (from doc/DETAILS):

    |  crt = X.509 certificate
    |  crs = X.509 certificate and private key available
    |  ssb = secret subkey (secondary key)
    |  uat = user attribute (same as user id except for field 10).
    |  pkd = public key data (special field format, see below)
    |  grp = reserved for gpgsm
    |  rvk = revocation key
    """

    def __init__(self, gpg):
        super(ListKeys, self).__init__()
        self._gpg = gpg
        self.curkey = None
        self.curuid = None
        self.fingerprints = []
        self.uids = []
        self.sigs = {}
        self.certs = {}
        self.revs = {}
        return

    def key(self, args):
        vars = ('\n            type trust length algo keyid date expires dummy ownertrust uid\n        ').split()
        self.curkey = {}
        for i in range(len(vars)):
            self.curkey[vars[i]] = args[i]

        self.curkey['uids'] = []
        self.curkey['sigs'] = {}
        self.curkey['rev'] = {}
        if self.curkey['uid']:
            self.curuid = self.curkey['uid']
            self.curkey['uids'].append(self.curuid)
            self.sigs[self.curuid] = set()
            self.certs[self.curuid] = set()
            self.revs[self.curuid] = set()
            self.curkey['sigs'][self.curuid] = []
        del self.curkey['uid']
        self.curkey['subkeys'] = []
        self.append(self.curkey)

    pub = sec = key

    def fpr(self, args):
        self.curkey['fingerprint'] = args[9]
        self.fingerprints.append(args[9])

    def uid(self, args):
        uid = args[9]
        uid = ESCAPE_PATTERN.sub(lambda m: chr(int(m.group(1), 16)), uid)
        self.curkey['uids'].append(uid)
        self.curuid = uid
        self.curkey['sigs'][uid] = []
        self.sigs[uid] = set()
        self.certs[uid] = set()
        self.uids.append(uid)

    def sig(self, args):
        vars = ('\n            type trust length algo keyid date expires dummy ownertrust uid\n        ').split()
        sig = {}
        for i in range(len(vars)):
            sig[vars[i]] = args[i]

        self.curkey['sigs'][self.curuid].append(sig)
        self.sigs[self.curuid].add(sig['keyid'])
        if sig['trust'] == '!':
            self.certs[self.curuid].add(sig['keyid'])

    def sub(self, args):
        subkey = [
         args[4], args[11]]
        self.curkey['subkeys'].append(subkey)

    def rev(self, args):
        self.curkey['rev'] = {'keyid': args[4], 'revtime': args[5], 
           'uid': self.curuid}

    def _handle_status(self, key, value):
        pass


class ImportResult(object):
    """Parse GnuPG status messages for key import operations."""

    def __init__(self, gpg):
        """Start parsing the results of a key import operation.

        :type gpg: :class:`gnupg.GPG`
        :param gpg: An instance of :class:`gnupg.GPG`.
        """
        self._gpg = gpg
        self._ok_reason = {'0': 'Not actually changed', '1': 'Entirely new key', 
           '2': 'New user IDs', 
           '4': 'New signatures', 
           '8': 'New subkeys', 
           '16': 'Contains private key', 
           '17': 'Contains private key'}
        self._problem_reason = {'0': 'No specific reason given', '1': 'Invalid Certificate', 
           '2': 'Issuer Certificate missing', 
           '3': 'Certificate Chain too long', 
           '4': 'Error storing certificate'}
        self._fields = ('count no_user_id imported imported_rsa unchanged\n        n_uids n_subk n_sigs n_revoc sec_read sec_imported sec_dups\n        not_imported').split()
        self.counts = OrderedDict(zip(self._fields, [ int(0) for x in range(len(self._fields)) ]))
        self.fingerprints = list()
        self.results = list()

    def __nonzero__(self):
        """Override the determination for truthfulness evaluation.

        :rtype: bool
        :returns: True if we have imported some keys, False otherwise.
        """
        if self.counts['not_imported'] > 0:
            return False
        if len(self.fingerprints) == 0:
            return False
        return True

    __bool__ = __nonzero__

    def _handle_status(self, key, value):
        """Parse a status code from the attached GnuPG process.

        :raises ValueError: if the status message is unknown.
        """
        if key == 'IMPORTED':
            pass
        elif key == 'PINENTRY_LAUNCHED':
            log.warn('GnuPG has just attempted to launch whichever pinentry program you have configured, in order to obtain the passphrase for this key.  If you did not use the `passphrase=` parameter, please try doing so.  Otherwise, see Issues #122 and #137:\nhttps://github.com/isislovecruft/python-gnupg/issues/122\nhttps://github.com/isislovecruft/python-gnupg/issues/137')
        elif key == 'KEY_CONSIDERED':
            self.results.append({'status': key.replace('_', ' ').lower()})
        elif key == 'NODATA':
            self.results.append({'fingerprint': None, 'status': 'No valid data found'})
        elif key == 'IMPORT_OK':
            reason, fingerprint = value.split()
            reasons = []
            for code, text in self._ok_reason.items():
                if int(reason) == int(code):
                    reasons.append(text)

            reasontext = ('\n').join(reasons) + '\n'
            self.results.append({'fingerprint': fingerprint, 'status': reasontext})
            self.fingerprints.append(fingerprint)
        elif key == 'IMPORT_PROBLEM':
            try:
                reason, fingerprint = value.split()
            except:
                reason = value
                fingerprint = '<unknown>'

            self.results.append({'fingerprint': fingerprint, 'status': self._problem_reason[reason]})
        elif key == 'IMPORT_RES':
            import_res = value.split()
            for x in self.counts.keys():
                self.counts[x] = int(import_res.pop(0))

        elif key == 'KEYEXPIRED':
            res = {'fingerprint': None, 'status': 'Key expired'}
            self.results.append(res)
        elif key == 'SIGEXPIRED':
            res = {'fingerprint': None, 'status': 'Signature expired'}
            self.results.append(res)
        else:
            raise ValueError('Unknown status message: %r' % key)
        return

    def summary(self):
        l = []
        l.append('%d imported' % self.counts['imported'])
        if self.counts['not_imported']:
            l.append('%d not imported' % self.counts['not_imported'])
        return (', ').join(l)


class ExportResult(object):
    """Parse GnuPG status messages for key export operations."""

    def __init__(self, gpg):
        """Start parsing the results of a key export operation.

        :type gpg: :class:`gnupg.GPG`
        :param gpg: An instance of :class:`gnupg.GPG`.
        """
        self._gpg = gpg
        self._fields = ('count secret_count exported').split()
        self.counts = OrderedDict(zip(self._fields, [ int(0) for x in range(len(self._fields)) ]))
        self.fingerprints = list()

    def __nonzero__(self):
        """Override the determination for truthfulness evaluation.

        :rtype: bool
        :returns: True if we have exported some keys, False otherwise.
        """
        if self.counts['not_imported'] > 0:
            return False
        if len(self.fingerprints) == 0:
            return False
        return True

    __bool__ = __nonzero__

    def _handle_status(self, key, value):
        """Parse a status code from the attached GnuPG process.

        :raises ValueError: if the status message is unknown.
        """
        informational_keys = [
         'KEY_CONSIDERED']
        if key in 'EXPORTED':
            self.fingerprints.append(value)
        elif key == 'EXPORT_RES':
            export_res = value.split()
            for x in self.counts.keys():
                self.counts[x] += int(export_res.pop(0))

        elif key not in informational_keys:
            raise ValueError('Unknown status message: %r' % key)

    def summary(self):
        return '%d exported' % self.counts['exported']


class Verify(object):
    """Parser for status messages from GnuPG for certifications and signature
    verifications.

    People often mix these up, or think that they are the same thing. While it
    is true that certifications and signatures *are* the same cryptographic
    operation -- and also true that both are the same as the decryption
    operation -- a distinction is made for important reasons.

    A certification:
        * is made on a key,
        * can help to validate or invalidate the key owner's identity,
        * can assign trust levels to the key (or to uids and/or subkeys that
          the key contains),
        * and can be used in absense of in-person fingerprint checking to try
          to build a path (through keys whose fingerprints have been checked)
          to the key, so that the identity of the key's owner can be more
          reliable without having to actually physically meet in person.

    A signature:
        * is created for a file or other piece of data,
        * can help to prove that the data hasn't been altered,
        * and can help to prove that the data was sent by the person(s) in
          possession of the private key that created the signature, and for
          parsing portions of status messages from decryption operations.

    There are probably other things unique to each that have been
    scatterbrainedly omitted due to the programmer sitting still and staring
    at GnuPG debugging logs for too long without snacks, but that is the gist
    of it.
    """
    TRUST_UNDEFINED = 0
    TRUST_NEVER = 1
    TRUST_MARGINAL = 2
    TRUST_FULLY = 3
    TRUST_ULTIMATE = 4
    TRUST_LEVELS = {'TRUST_UNDEFINED': TRUST_UNDEFINED, 'TRUST_NEVER': TRUST_NEVER, 
       'TRUST_MARGINAL': TRUST_MARGINAL, 
       'TRUST_FULLY': TRUST_FULLY, 
       'TRUST_ULTIMATE': TRUST_ULTIMATE}

    def __init__(self, gpg):
        """Create a parser for verification and certification commands.

        :param gpg: An instance of :class:`gnupg.GPG`.
        """
        self._gpg = gpg
        self.valid = False
        self.status = None
        self.fingerprint = None
        self.pubkey_fingerprint = None
        self.key_id = None
        self.signature_id = None
        self.creation_date = None
        self.timestamp = None
        self.sig_timestamp = None
        self.username = None
        self.expire_timestamp = None
        self.trust_level = None
        self.trust_text = None
        self.subpackets = {}
        self.notations = {}
        self._last_notation_name = None
        return

    def __nonzero__(self):
        """Override the determination for truthfulness evaluation.

        :rtype: bool
        :returns: True if we have a valid signature, False otherwise.
        """
        return self.valid

    __bool__ = __nonzero__

    def _handle_status(self, key, value):
        """Parse a status code from the attached GnuPG process.

        :raises: :exc:`~exceptions.ValueError` if the status message is unknown.
        """
        if key in self.TRUST_LEVELS:
            self.trust_text = key
            self.trust_level = self.TRUST_LEVELS[key]
        elif key in ('RSA_OR_IDEA', 'NODATA', 'IMPORT_RES', 'PLAINTEXT', 'PLAINTEXT_LENGTH',
                     'POLICY_URL', 'DECRYPTION_INFO', 'DECRYPTION_KEY', 'DECRYPTION_OKAY',
                     'INV_SGNR', 'PROGRESS', 'PINENTRY_LAUNCHED', 'SUCCESS', 'UNEXPECTED',
                     'ENCRYPTION_COMPLIANCE_MODE', 'VERIFICATION_COMPLIANCE_MODE'):
            pass
        elif key == 'KEY_CONSIDERED':
            self.status = ('\n').join([self.status, 'key considered'])
        elif key == 'NEWSIG':
            self.status = None
            self.valid = False
            self.key_id, self.username = (None, None)
        elif key == 'BADSIG':
            self.valid = False
            self.status = 'signature bad'
            self.key_id, self.username = value.split(None, 1)
        elif key == 'GOODSIG':
            self.valid = True
            self.status = 'signature good'
            self.key_id, self.username = value.split(None, 1)
        elif key == 'VALIDSIG':
            self.valid = True
            self.fingerprint, self.creation_date, self.sig_timestamp, self.expire_timestamp = value.split()[:4]
            self.pubkey_fingerprint = value.split()[(-1)]
            self.status = 'signature valid'
        elif key == 'SIG_ID':
            self.signature_id, self.creation_date, self.timestamp = value.split()
        elif key == 'ERRSIG':
            self.valid = False
            self.key_id, algo, hash_algo, cls, self.timestamp = value.split()[:5]
            self.status = 'signature error'
        elif key == 'DECRYPTION_FAILED':
            self.valid = False
            self.key_id = value
            self.status = 'decryption failed'
        elif key in ('WARNING', 'ERROR', 'FAILURE'):
            if key in ('ERROR', 'FAILURE'):
                self.valid = False
            self.status = value
            log.warn('%s status emitted from gpg process: %s' % (key, value))
        elif key == 'NO_PUBKEY':
            self.valid = False
            self.key_id = value
            self.status = 'no public key'
        elif key in ('KEYEXPIRED', 'SIGEXPIRED'):
            pass
        elif key in ('EXPKEYSIG', 'REVKEYSIG'):
            self.valid = False
            self.key_id = value.split()[0]
            self.status = ('%s %s' % (key[:3], key[3:])).lower()
        elif key in 'KEYREVOKED':
            self.status = ('\n').join([self.status, 'key revoked'])
        elif key in 'SIG_SUBPACKET':
            fields = value.split()
            try:
                subpacket_number = fields[0]
                self.subpackets[subpacket_number] = {'flags': None, 'length': None, 
                   'data': None}
            except IndexError:
                pass
            else:
                try:
                    self.subpackets[subpacket_number]['flags'] = fields[1]
                    self.subpackets[subpacket_number]['length'] = fields[2]
                    self.subpackets[subpacket_number]['data'] = fields[3]
                except IndexError:
                    pass

        elif key.startswith('NOTATION_'):
            if key.endswith('NAME'):
                self.notations[value] = str()
                self._last_notation_name = value
            elif key.endswith('DATA'):
                if self._last_notation_name is not None:
                    self.notations[self._last_notation_name] += value
        else:
            raise ValueError('Unknown status message: %r %r' % (key, value))
        return


class Crypt(Verify):
    """Parser for internal status messages from GnuPG for ``--encrypt``,
    ``--decrypt``, and ``--decrypt-files``.
    """

    def __init__(self, gpg):
        Verify.__init__(self, gpg)
        self._gpg = gpg
        self.data = ''
        self.ok = False
        self.status = None
        self.data_format = None
        self.data_timestamp = None
        self.data_filename = None
        return

    def __nonzero__(self):
        if self.ok:
            return True
        return False

    __bool__ = __nonzero__

    def __str__(self):
        """The str() method for a :class:`Crypt` object will automatically return the
        decoded data string, which stores the encryped or decrypted data.

        In other words, these two statements are equivalent:

        >>> assert decrypted.data == str(decrypted)

        """
        return self.data.decode(self._gpg._encoding, self._gpg._decode_errors)

    def _handle_status(self, key, value):
        """Parse a status code from the attached GnuPG process.

        :raises: :exc:`~exceptions.ValueError` if the status message is unknown.
        """
        if key in ('ENC_TO', 'USERID_HINT', 'GOODMDC', 'END_DECRYPTION', 'BEGIN_SIGNING',
                   'NO_SECKEY', 'ERROR', 'NODATA', 'CARDCTRL'):
            pass
        elif key in ('NEED_PASSPHRASE', 'BAD_PASSPHRASE', 'GOOD_PASSPHRASE', 'MISSING_PASSPHRASE',
                     'DECRYPTION_FAILED', 'KEY_NOT_CREATED', 'KEY_CONSIDERED'):
            self.status = key.replace('_', ' ').lower()
        elif key == 'NEED_TRUSTDB':
            self._gpg._create_trustdb()
        elif key == 'NEED_PASSPHRASE_SYM':
            self.status = 'need symmetric passphrase'
        elif key == 'BEGIN_DECRYPTION':
            self.status = 'decryption incomplete'
        elif key == 'BEGIN_ENCRYPTION':
            self.status = 'encryption incomplete'
        elif key == 'DECRYPTION_OKAY':
            self.status = 'decryption ok'
            self.ok = True
        elif key == 'END_ENCRYPTION':
            self.status = 'encryption ok'
            self.ok = True
        elif key == 'INV_RECP':
            self.status = 'invalid recipient'
        elif key == 'KEYEXPIRED':
            self.status = 'key expired'
        elif key == 'KEYREVOKED':
            self.status = 'key revoked'
        elif key == 'SIG_CREATED':
            self.status = 'sig created'
        elif key == 'SIGEXPIRED':
            self.status = 'sig expired'
        elif key == 'PLAINTEXT':
            fmt, dts = value.split(' ', 1)
            if dts.find(' ') > 0:
                self.data_timestamp, self.data_filename = dts.split(' ', 1)
            else:
                self.data_timestamp = dts
            self.data_format = chr(int(str(fmt), 16))
        else:
            super(Crypt, self)._handle_status(key, value)


class ListPackets(object):
    """Handle status messages for --list-packets."""

    def __init__(self, gpg):
        self._gpg = gpg
        self.status = None
        self.need_passphrase = None
        self.need_passphrase_sym = None
        self.userid_hint = None
        self.key = None
        self.encrypted_to = []
        return

    def _handle_status(self, key, value):
        """Parse a status code from the attached GnuPG process.

        :raises: :exc:`~exceptions.ValueError` if the status message is unknown.
        """
        if key in ('NO_SECKEY', 'BEGIN_DECRYPTION', 'DECRYPTION_FAILED', 'END_DECRYPTION',
                   'GOOD_PASSPHRASE', 'BAD_PASSPHRASE', 'KEY_CONSIDERED'):
            pass
        elif key == 'NODATA':
            self.status = nodata(value)
        elif key == 'ENC_TO':
            key, _, _ = value.split()
            if not self.key:
                self.key = key
            self.encrypted_to.append(key)
        elif key in ('NEED_PASSPHRASE', 'MISSING_PASSPHRASE'):
            self.need_passphrase = True
        elif key == 'NEED_PASSPHRASE_SYM':
            self.need_passphrase_sym = True
        elif key == 'USERID_HINT':
            self.userid_hint = value.strip().split()
        else:
            raise ValueError('Unknown status message: %r' % key)