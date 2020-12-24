# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/strings.py
# Compiled at: 2015-11-05 10:40:17
"""Commonly used string constants.

.. todo:: The instructions for the OpenPGP keys in
    :data:`BRIDGEDB_OPENPGP_KEY` are not translated… should we translate them?
    Should we tell users where to obtain GPG4Win/GPGTools/gnupg?  Should those
    instruction be that verbose?  Or should we get rid of the instructions
    altogether, and assume that any encouragement towards using GPG will just
    make users more frustrated, and (possibly) (mis-)direct that frustration
    at Tor or BridgeDB?
"""
from __future__ import unicode_literals
from collections import OrderedDict

def _(text):
    """This is necessary because strings are translated when they're imported.
    Otherwise this would make it impossible to switch languages more than
    once.

    :returns: The **text**.
    """
    return text


EMAIL_MISC_TEXT = {0: _(b'[This is an automated message; please do not reply.]'), 
   1: _(b'Here are your bridges:'), 
   2: _(b'You have exceeded the rate limit. Please slow down! The minimum time between\nemails is %s hours. All further emails during this time period will be ignored.'), 
   3: _(b'COMMANDs: (combine COMMANDs to specify multiple options simultaneously)'), 
   4: _(b'Welcome to BridgeDB!'), 
   5: _(b'Currently supported transport TYPEs:'), 
   6: _(b'Hey, %s!'), 
   7: _(b'Hello, friend!'), 
   8: _(b'Public Keys'), 
   9: _(b'This email was generated with rainbows, unicorns, and sparkles\nfor %s on %s at %s.')}
WELCOME = {0: _(b'BridgeDB can provide bridges with several %stypes of Pluggable Transports%s,\nwhich can help obfuscate your connections to the Tor Network, making it more\ndifficult for anyone watching your internet traffic to determine that you are\nusing Tor.\n\n'), 
   1: _(b"Some bridges with IPv6 addresses are also available, though some Pluggable\nTransports aren't IPv6 compatible.\n\n"), 
   2: _(b"Additionally, BridgeDB has plenty of plain-ol'-vanilla bridges %s without any\nPluggable Transports %s which maybe doesn't sound as cool, but they can still\nhelp to circumvent internet censorship in many cases.\n\n")}
FAQ = {0: _(b'What are bridges?'), 
   1: _(b'%s Bridges %s are Tor relays that help you circumvent censorship.')}
OTHER_DISTRIBUTORS = {0: _(b'I need an alternative way of getting bridges!'), 
   1: _(b'Another way to get bridges is to send an email to %s. Please note that you must\nsend the email using an address from one of the following email providers:\n%s, %s or %s.')}
HELP = {0: _(b"My bridges don't work! I need help!"), 
   1: _(b"If your Tor doesn't work, you should email %s."), 
   2: _(b'Try including as much info about your case as you can, including the list of\nbridges and Pluggable Transports you tried to use, your Tor Browser version,\nand any messages which Tor gave out, etc.')}
BRIDGES = {0: _(b'Here are your bridge lines:'), 
   1: _(b'Get Bridges!')}
OPTIONS = {0: _(b'Please select options for bridge type:'), 
   1: _(b'Do you need IPv6 addresses?'), 
   2: _(b'Do you need a %s?')}
CAPTCHA = {0: _(b'Your browser is not displaying images properly.'), 
   1: _(b'Enter the characters from the image above...')}
HOWTO_TBB = {0: _(b'How to start using your bridges'), 
   1: _(b'To enter bridges into Tor Browser, first go to the %s Tor Browser download\npage %s and then follow the instructions there for downloading and starting\nTor Browser.'), 
   2: _(b"When the 'Tor Network Settings' dialogue pops up, click 'Configure' and follow\nthe wizard until it asks:"), 
   3: _(b'Does your Internet Service Provider (ISP) block or otherwise censor connections\nto the Tor network?'), 
   4: _(b"Select 'Yes' and then click 'Next'. To configure your new bridges, copy and\npaste the bridge lines into the text input box. Finally, click 'Connect', and\nyou should be good to go! If you experience trouble, try clicking the 'Help'\nbutton in the 'Tor Network Settings' wizard for further assistance.")}
EMAIL_COMMANDS = {b'get help': _(b'Displays this message.'), 
   b'get bridges': _(b'Request vanilla bridges.'), 
   b'get ipv6': _(b'Request IPv6 bridges.'), 
   b'get transport [TYPE]': _(b'Request a Pluggable Transport by TYPE.'), 
   b'get key': _(b"Get a copy of BridgeDB's public GnuPG key.")}
SUPPORTED_TRANSPORTS = {}
DEFAULT_TRANSPORT = b''

def _getSupportedTransports():
    """Get the list of currently supported transports.

    :rtype: list
    :returns: A list of strings, one for each supported Pluggable Transport
        methodname, sorted in alphabetical order.
    """
    global SUPPORTED_TRANSPORTS
    supported = [ name.lower() for name, w00t in SUPPORTED_TRANSPORTS.items() if w00t ]
    supported.sort()
    return supported


def _setDefaultTransport(transport):
    global DEFAULT_TRANSPORT
    DEFAULT_TRANSPORT = transport


def _getDefaultTransport():
    return DEFAULT_TRANSPORT


def _setSupportedTransports(transports):
    """Set the list of currently supported transports.

    .. note: You shouldn't need to touch this. This is used by the config file
        parser. You should change the SUPPORTED_TRANSPORTS dictionary in
        :file:`bridgedb.conf`.

    :param dict transports: A mapping of Pluggable Transport methodnames
        (strings) to booleans.  If the boolean is ``True``, then the Pluggable
        Transport is one which we will (more easily) distribute to clients.
        If ``False``, then we (sort of) don't distribute it.
    """
    global SUPPORTED_TRANSPORTS
    SUPPORTED_TRANSPORTS = transports


def _getSupportedAndDefaultTransports():
    """Get a dictionary of currently supported transports, along with a boolean
    marking which transport is the default.

    It is returned as a :class:`collections.OrderedDict`, because if it is a
    regular dict, then the dropdown menu would populated in random order each
    time the page is rendered.  It is sorted in alphabetical order.

    :rtype: :class:`collections.OrderedDict`
    :returns: An :class:`~collections.OrderedDict` of the Pluggable Transport
        methodnames from :data:`SUPPORTED_TRANSPORTS` whose value in
        ``SUPPORTED_TRANSPORTS`` is ``True``.  If :data:`DEFAULT_TRANSPORT` is
        set, then the PT methodname in the ``DEFAULT_TRANSPORT`` setting is
        added to the :class:`~collections.OrderedDict`, with the value
        ``True``. Every other transport in the returned ``OrderedDict`` has
        its value set to ``False``, so that only the one which should be the
        default PT is ``True``.
    """
    supported = _getSupportedTransports()
    transports = OrderedDict(zip(supported, [ False for _ in range(len(supported)) ]))
    if DEFAULT_TRANSPORT:
        transports[DEFAULT_TRANSPORT] = True
    return transports


EMAIL_SPRINTF = {b'WELCOME0': (
               b'', b'[0]'), 
   b'WELCOME2': (
               b'-', b'-'), 
   b'HOWTO_TBB1': (
                 b'', b'[0]'), 
   b'HELP0': b'help@rt.torproject.org'}
EMAIL_REFERENCE_LINKS = {b'WELCOME0': b'[0]: https://www.torproject.org/docs/pluggable-transports.html', 
   b'HOWTO_TBB1': b'[0]: https://www.torproject.org/projects/torbrowser.html'}
BRIDGEDB_OPENPGP_KEY = b"# This keypair contains BridgeDB's online signing and encryption subkeys. This\n# keypair rotates because it is kept online. However, the current online\n# keypair will *ALWAYS* be certified by the offline keypair (at the bottom of\n# this file).\n#\n# If you receive an email from BridgeDB, it should be signed with the\n# 21B554E95938F4D0 subkey from the following keypair:\n\n# pub   4096R/8DC43A2848821E32 2013-09-11 [expires: 2015-09-11]\n#       Key fingerprint = DF81 1109 E17C 8BF1 34B5  EEB6 8DC4 3A28 4882 1E32\n# uid                          BridgeDB <bridges@bridges.torproject.org>\n# sub   4096R/21B554E95938F4D0 2013-09-11 [expires: 2015-09-11]\n#       Key fingerprint = 9FE3 9D1A 7438 9223 3B3F  66F2 21B5 54E9 5938 F4D0\n# sub   4096R/E7793047C5B54232 2013-09-11 [expires: 2015-09-11]\n#       Key fingerprint = CFFB 8469 9048 37E7 8CAE  322C E779 3047 C5B5 4232\n\n-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nmQINBFIv8YABEADRqvfLB4xWj3Fz+HEmUUt/qbJnZhqIjo5WBHaBJOmrzx1c9fLN\naYG36Hgo6A7NygI1oQmFnDinSrZAtrPaT63d1Jg49yZwr/OhMaxHYJElMFHGJ876\nkLZHmQTysquYKDHhv+fH51t7UVaZ9NkP5cI+V3pqck0DW5DwMsVJXNaU317kk9me\nmPJUDMb5FM4d2Vtk1N+54bHJgpgmnukNtpJmRyHRbZBqNMln5nWF7vdZ4u5PGPWj\nbA0rPZhayeE3FQ0MHiGL12kHAy30pfg54QfPJDQBCywjABetRE+xaM9TcS+R31Pf\n2VbLeb+Km7QpHMwOXI5xZLss9BAWm9EBbmXxuqaRBHyi830jjCrK9UYuzzOqKoUV\nMk1BRelZTFnGPWeVTE+Ps+pwJ0Dwx4ghppJBCoArmEbkNliblxR/2wYOOFi/ZVA4\nZc2ok9T3rBLVg07b7ezFUScGiTnc7ac7hp6r8Qsh09ZbhRr9erK/n194aEvkXTfr\nqepwrAE7YeF4YuR206UOFFWDhxWDLbRu0gIWgrevEQu/cvQPrO9uH5fL6Gw/+mNP\nQ/NIteejhkDyvyTUKyBu7x+Gls71zT2u/X13eOAJ8IxBkSVRKQ8tRD+oqJkWplOf\n+BpaGU+g6u4kT2AzFDxTOupfrYcPvORTAV/V3suys2YQE4x422GASXDivQARAQAB\ntClCcmlkZ2VEQiA8YnJpZGdlc0BicmlkZ2VzLnRvcnByb2plY3Qub3JnPokDJQQT\nAQoBD0gUgAAAAAAXACh2ZXJpZmllZEB0b3Jwcm9qZWN0Lm9yZ0RGODExMTA5RTE3\nQzhCRjEzNEI1RUVCNjhEQzQzQTI4NDg4MjFFMzJPFIAAAAAAHgAoYnJpZGdlc0Bi\ncmlkZ2VzLnRvcnByb2plY3Qub3JnREY4MTExMDlFMTdDOEJGMTM0QjVFRUI2OERD\nNDNBMjg0ODgyMUUzMioaaHR0cHM6Ly9icmlkZ2VzLnRvcnByb2plY3Qub3JnL3Bv\nbGljeS50eHQCGwEDCw0JBBUKCQgEFgIBAAIeAQIXgCcYaHR0cHM6Ly9icmlkZ2Vz\nLnRvcnByb2plY3Qub3JnL2tleS5hc2MFAlSKBKIFCQPDTiIACgkQjcQ6KEiCHjIs\njg//bJ12eRnBMfIGzOGh+T4wz7/YyKLfARAMnqDnSxhTxuE+M5hWm3QbxP03R6eY\nx+PKwQaDJSmm7HhRhltb7QXUe8dqjnocFwwagpoLZ/81mBLxByqg5TKHGGIGy+DX\nomIzCq5ijx1IUkHlgh708a5alG7bjRTqedT4Wxxyl6psGzDhGQdS8bqx/f32nQaE\nh41l+A/EY1g2HVqky63ZHAP3S2v+mWCrk5DnkElc0229MXqaBuEr4nbYMXRkahMb\nE2gnCmdSoeD21AY6bNyz7IcJGpyKCx9+hVgPjpm3J23JEYyPL+s48jn6QcI/Q2gD\nyAtgU65y6IrdYn8SwkABI1FIq9WAwG7DaInxvkqkYqyBQLaZJEMyX8NTBvFoT5JS\njnkxG0xu61Vxq0BLYBIOJE0VFHAJ40/jOvSxQJkQhu9G4BK7htnADbtstmMDMM3q\nxuuO5pcj2rl7YthNunyZ1yhPHXijUUyKrwR9piENpptztFBVN6+ijqU/TmWMOtbH\nX7p9F+3tXCHHqwO5U/JMtsb/9M39MR8BrdcLc7m6dCpeuSUuR2LLroh+MoMJGviI\niesxHF95kFqkJAecW1Z3eKL9vrlbfO3waeuCi18k1TePnZuG5lmf2KjKDW5vHK4O\nWFqvvfK2kxkCUjvGdLeTOAVOV+X+PQ23jvBJO2bS7YbOb9C5Ag0EUi/ygQEQALZ/\np7xRINHY7MMf3/bo/I0WRxWHd1AE9tRToyEg1S2u1YrWWL5M9D8saRsp9cpnpGEu\nhW3vu7G4nasY27qOz4bSKu1YMAVIC58v1tEnBqdo1zErNjhs38PrmJKbbs9tDfYY\nOi2x0GlhMbIrNStcZpnCdLa6U6NLMbggDL1GxjMPYBMi4TtLgcIeRDUSjsZscZkg\nKxs5QkSVc3SrYyraayIc8WtIpDLcxPt6/g90rbatZzBfO+93Rz7qUXHmgzuM0hy1\nFvn619o3I5DsWrfOz9t/QuznoOBw4PfzDPNT7VlzZN4xHAcr5+7B+DH9IsvlCt5N\nkQFuYpFZCpXNaD2XOtmIqjTCeLNfcgTEj0qoUIEKyKbBIgfP+7S2tLXy8JKUTy5g\n9kxXQeHueLykQ4Mt18JH0nMHbHbQl0K3LGT4ucRDOmjNtlQCltVLkIk3GimyqKs/\nvdZ9c+dm4Akx1qsJcwvveX+imJe2e9RUodcxWXxWrYnuPa5b5nfR1i+GfV0on/Pt\nAQ8gc9CkJpMiq5TQDOFhFP6yQcq77sXuUkEl5qamptedz28E0I693ulnfwcsE80p\nxkpIG6n33DZJSEyqgtWjE1P2pnsVfO5ILs3mKLe7bO1v3qMXcCkMCGH/kwzvtowq\nYvY4gaZMDZtQFY8U7lI9FdRUvVdeHAB24y291nhzABEBAAGJBYMEGAEKANNIFIAA\nAAAAFwAodmVyaWZpZWRAdG9ycHJvamVjdC5vcmdERjgxMTEwOUUxN0M4QkYxMzRC\nNUVFQjY4REM0M0EyODQ4ODIxRTMyTxSAAAAAAB4AKGJyaWRnZXNAYnJpZGdlcy50\nb3Jwcm9qZWN0Lm9yZ0RGODExMTA5RTE3QzhCRjEzNEI1RUVCNjhEQzQzQTI4NDg4\nMjFFMzIqGmh0dHBzOi8vYnJpZGdlcy50b3Jwcm9qZWN0Lm9yZy9wb2xpY3kudHh0\nAhsCBQJUigTTBQkDw01SAqTB2CAEGQEKAIEFAlIv8oFPFIAAAAAAHgAoYnJpZGdl\nc0BicmlkZ2VzLnRvcnByb2plY3Qub3JnOUZFMzlEMUE3NDM4OTIyMzNCM0Y2NkYy\nMjFCNTU0RTk1OTM4RjREMCoaaHR0cHM6Ly9icmlkZ2VzLnRvcnByb2plY3Qub3Jn\nL3BvbGljeS50eHQACgkQIbVU6Vk49NDbPw/5ATe/T8+eaToC3v0TYNRH5nveQvzA\nWdnshD3lnvfsgDhbilwifKpc5LHKXU3rvb42HH2cu0ckuksdDTvICZD9cJjRq/F+\nMzm0pNCAJg0pQnHaaWFQjw+CHYEoizai3S+iYxhNHeSdA6Ty7xm4+bHNf0Aqblbd\n6dKwq9EvjwAI6zZsAHtsmHRUMdrFwGdKae6CSchUT2JQFBPEWMhvzdpDGACWVaSP\nsxYKuYg9LgpswGcof+tprRjKRl8MtSh0ufjbVBlTeSKpL5Y+fcTRD3PI8w7Ocr3z\njr6XpYG4SUNHsWwxyu/DTXg76Lk1/+BdaH25hDOAasLUOU7yRL8zD/c7M0FkGXdj\nr5I2DEEqwzJ9cPHWjpgb8N9fZLoPFP9JOmKGHINqxNe7TfwiTdD6uDKs/u/QK1U+\no3iYBXBTREdopPUdBTM9wYRUhyGXTEKLhUP3MGpXYlgeYPrSdp76VyN3BzLTbMv+\n+7rxyKxL9cWYU0pnXHgPC5nyHX5nqXmhMnkxAD3Bnm8n9XDfgiyTDExqksEh2VXt\nyhVfLezylEP2fwtd8/mABBCsTjzZW6FRfRRAjUZWZGFpFg8no1x5JS9uiswRP5g1\nqHijNFWpGyTtJWl5VNd0d9+LtVUX1jRpDUpsjZcxqs3fsvw2p+H/zQ1wFvDrsoav\nhqOTq+AEnJc7ZG8JEI3EOihIgh4ych8P/3GTyWb29+43YVibbSPPvEv4gFqziC+9\n1p92FJ0V4XdaT7TW3qaZVp5edUNwB/jjF0SxBybwaMX2ZIGXOjnjF6/Zby4ynuTX\nvZkS1mKRA0KWupB3e9PSMY3ZtssnqpGna/+3qlpxtunW7HcW4nCF/f59WHhlVjaO\nMXjtuWj59yB56Dd1sNjwhcNCyp4/NpzGnRW97ZV3Pp4oqIOqcGzCQXkVPcnaqcOh\nCs9vIDJlMtn/IWBzUGimuRllDSSVSWkYkyJcG2NUHUwgXYpLwQz7sScvmCPchf4K\nqarpX0FpkUDfqaVVuQ7A2XbPUAVFzIk930G1WzgOuOdg9vhWSEjou+SKrAoMz90w\n3xHwEvmPDTTVJQft9ytoRbwZkIPfzzhII3mr4agbORAfzDaj5g/f6CVRdg6D3ME1\nEtg9ZrfLgRY993g/arfIME6OOsiNcy5+PunN96Rw0o1xoD+97NmZuQrs/p4Mfn5o\n8EwXHutREhahin+3/SV3hz9ReeLYmClq+OVhjPzPdtwZsFoyQyUJoFVHPTuSdChZ\nFPaqN68FjlNMugmxnvski3ZDVT7pw3B6otjjaL3rr6q0PC2yhEb2ntb3IFUizHjn\n80SmfE1Bqwit7ZHu8r/Gt/0iecGk5h84VzSgiGZGF/7m1i5UMVlNSeWnsInGa5Su\n7HSzfMq+YmkzuQINBFIv8p4BEADTOLR5e5NKKRPpjCb4B/8YYkWh+orb70EogIZ6\nj5v8d/djLyhjqZ9BIkh41/hYKMwnsa4KkDkTaX0eNu3BFB2zGgZ1GSd7525ESxiq\nsuXIlAg2pex7bysaFfua0nUx64tmaQm2XArdkj/wI0pbg+idWym3WQQmZLyTTbzl\n8rpTEtTt+S2m6z3EeAhEHuNFH16hEDUywlef3EotX3njuFiLqaNvnzUYDxhUvKd2\n2K1es1ggispgP+eb1bkMApxecf2rqmSUEcvsuTWip4oGZPBLGDQeNKHkCUVbj4wT\nyWDIRtto3wi+4CFPEVzw+htj1cQfTstPqUdG7NSOmLQggedoUdv7AJm4MJJiyEax\nl+IAf6Afwrrm3eOSv0PgoUxOrUb9vhIoL8ih8gtiqvQ9qYaRQfQA/w3Z0Su2Yfoc\nfQS8Uw99qG+oTgieG6F6ud8+hMZAYVZFqbU+ztzMyDE6h4Hflkt6VNJ0Hk0VoF38\nTTs77pHXXBbLD6SzR6tbNuR9r/lbmC8Qf2A1ZAThR0iuGhNRFtUPo28GxakxGdLZ\n9kHIxjl7EN/gsmYTwuEhr+yfNtLwtSH0ojeqbDmgufvgh+SITCtyNDAUspjrZYEt\nF0NHRpSom2NFVELMqMRydU/ncph1rGZgVp6/zVj6xIlhKmqj5P1y/9B0c4Tu1CzJ\npkJ5wwARAQABiQLpBBgBCgDTSBSAAAAAABcAKHZlcmlmaWVkQHRvcnByb2plY3Qu\nb3JnREY4MTExMDlFMTdDOEJGMTM0QjVFRUI2OERDNDNBMjg0ODgyMUUzMk8UgAAA\nAAAeAChicmlkZ2VzQGJyaWRnZXMudG9ycHJvamVjdC5vcmdERjgxMTEwOUUxN0M4\nQkYxMzRCNUVFQjY4REM0M0EyODQ4ODIxRTMyKhpodHRwczovL2JyaWRnZXMudG9y\ncHJvamVjdC5vcmcvcG9saWN5LnR4dAIbDAUCVIoE4QUJA8NNQwAKCRCNxDooSIIe\nMo7JEADDBtQpYxPhbj3MT0xpk96EDlon/5yHVf+cnk1pNisc+HkJsVe1nh7gAWOz\nwJKdeqOVpgxiJTxIQdl6mipKwwFi0DreP7h56s1WQkuSSWJzqssAwWHfVAsX13fV\nzWd0XyxN/OF9ZKQjX4qwpJ/na631PSwZLvHYhMaZnb9pjNwC5/PEKRmFqLbQT6Px\n12miZT6ToPDCczHxJ4BxbEGVU+PtRsHwmTRT3JhxFNDfeVd+uwsQIMidJbUoqVW7\nfe2zNd0TaWyz4Rw087oZE2OXdctjvtsu8fzXx6d/tkazI6cUOqoaMTR41KEu5X0T\nBpWSAMADBYjNs9QRWXX7ZlsJRUSCX1EKbMhgoL6KIGceIkjH61M/LF6HqDgSgSWt\nh+LIYGa+LrB/6819o32QSOSHHJ5+NJrbCSaLgKE/LKnf92V2QbZE8IGY6EOSjHqn\nn1+j+CLRKY/kUyvk+1TumTghjg/aDs/8Jv8PvgSWLQ0q1rxHYbX7q9ZJhYC/4LdR\nya/Cho6w2l0N3tV/IMAwvFNHsaiIiiwfoOQbkBUvkyzBwjKt96Ai4I0QKt/63uH0\ndrQhlJEgIyGkOrorBByVqZAQdnoLENYIu6tDUj0bTbGObKqua4iPlSK3/g40zCm4\n9OgcN7A8kFuNpgp2EHqj1/jrwd7mZYKsWTuGiR/7fwXf+4xbvg==\n=raCx\n-----END PGP PUBLIC KEY BLOCK-----\n\n# The following keypair is BridgeDB's offline certification-only keypair. It\n# is used to sign new online signing/encryption keypairs.\n#\n# If you import this key and mark it as trusted, emails from BridgeDB (if\n# signed correctly with the online keypair above) should always be trusted. To\n# do this, open a shell and do:\n#\n#     $ curl -O https://bridges.torproject.org/keys\n#     $ gpg --import keys\n#     $ gpg --check-sigs 7B78437015E63DF47BB1270ACBD97AA24E8E472E\n#     $ gpg --edit-key 7B78437015E63DF47BB1270ACBD97AA24E8E472E\n#\n# Then type 'trust' to set the trust level. Choose a number that you like.\n# Next type 'quit'. Finally, to create a local signature which will will not\n# be uploaded to keyservers:\n#\n#     $ gpg --lsign-key 7B78437015E63DF47BB1270ACBD97AA24E8E472E\n#\n\n# pub   16384R/CBD97AA24E8E472E 2013-10-12\n#      Key fingerprint = 7B78 4370 15E6 3DF4 7BB1  270A CBD9 7AA2 4E8E 472E\n# uid            BridgeDB (Offline ID Key) <bridges@bridges.torproject.org>\n-----BEGIN PGP PUBLIC KEY BLOCK-----\n\n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\nILUXBkpIDfVSoZD7qWlntai53BDQr5pfMJhv15di4XAhtqv43vAmA57ifd+QJS2U\nAfYc4CdX0lk2BZ4jRD8jCZ4Uxw15E3RqhnXsWDRxtD4fwsb2ZFi0DDuPlwBdGgh5\nRm2Bz9JjSV6gDEuXr/JtAzjSz1Jdh8wPkSofiHGTfxysVhlGlg+YPRziRlzML8A2\n0xY+9mPxEEin5ZQ9wmrDyiiOBvPTbG3O9+Sp5VZDuD4ivW/DHumPWGVSRdjcAQDe\nHMXUVGjhBDnj06XNrgJPhODdJeYq0EnGTt15ofZQSswD7TTTRPDOn0Cz/QARAQAB\ntDpCcmlkZ2VEQiAoT2ZmbGluZSBJRCBLZXkpIDxicmlkZ2VzQGJyaWRnZXMudG9y\ncHJvamVjdC5vcmc+iQkfBBMBCgEJBQJSWQfkSBSAAAAAABcAKHZlcmlmaWVkQHRv\ncnByb2plY3Qub3JnN0I3ODQzNzAxNUU2M0RGNDdCQjEyNzBBQ0JEOTdBQTI0RThF\nNDcyRU8UgAAAAAAeAChicmlkZ2VzQGJyaWRnZXMudG9ycHJvamVjdC5vcmc3Qjc4\nNDM3MDE1RTYzREY0N0JCMTI3MEFDQkQ5N0FBMjRFOEU0NzJFKhpodHRwczovL2Jy\naWRnZXMudG9ycHJvamVjdC5vcmcvcG9saWN5LnR4dAIbAQMLDQkEFQoJCAQWAgEA\nAh4BAheAJxhodHRwczovL2JyaWRnZXMudG9ycHJvamVjdC5vcmcva2V5LmFzYwAK\nCRDL2XqiTo5HLoqEP/48rFpJCVStn8xo+KkHSVvsqpxDRlb/nNheI+ov2UxILdwl\nNIU6kLsvKECKPe1AHKdS/MzANbkTF35Y4QgZsNpVXaCVL7adGBSzOdPFupDJJVOu\nwa+uFRc/FuNJyH/TIn56/+R5J5C54OxIYNxvW3WF4eHKLJYk/JZOMMfy4iWm7Sql\n0nDC5O435nK4F4Jb4GLPlUIzioIy2OWqGoFHXymbGhL1tWaqasYmED4n3AMqlYw6\nxnNhdWOc/KZelPl9nanybyh0IIdZqUKZleRt4BxSgIT8FqC2sZuZ8z7O9s987Naz\nQ32SKaP4i2M9lai/Y2QYfKo+wlG+egmxtujz7etQMGlpgBZzFLdJ8/w4U11ku1ai\nom74RIn8zl/LHjMQHnCKGoVlscTI1ZPt+p+p8hO2/9vOwTR8y8O/3DQSOfTSipwc\n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\nYnJpZGdlc0BicmlkZ2VzLnRvcnByb2plY3Qub3JnREY4MTExMDlFMTdDOEJGMTM0\nQjVFRUI2OERDNDNBMjg0ODgyMUUzMioaaHR0cHM6Ly9icmlkZ2VzLnRvcnByb2pl\nY3Qub3JnL3BvbGljeS50eHQACgkQjcQ6KEiCHjIaqBAA0BuEs7horx6iCq4cjAhv\nYPLrxuC4fKEfVyhAjCJMJSFFCPAlGgU+BjyPNDD57wzKAmUkdJG+Ss25mwWXa53w\n5R2kDqDnHocOdZGtxZ7zx/uUd2eWLNBfVuK7nHOk1d1Hs0OZBnckc+MCqnLtuYe5\n68pa9+jW6cNIjAnzMIListmoXWgYYWJvMKeBMG4DGtYJ8w7CJQjOHc5yar12DrX3\nwnQ7hXtFuuqQblpEUnLnZGvHf2NKMZfBBMcP96h9OmLGNa+vmNYsMyPKU7n5hPgX\nnTgmQ4xrv1G7JukjppZRA8SFoxupcaQeTixyWERGBhBiAbwZsbQz8L/TVZKierzg\nsdNngHcFzE8MyjuJDvTos7qXPmgSRXFqJLRn0ZxpR5V1V8BVZUqCGuSZT89TizsD\nz5vyv8c9r7HKD4pRjw32P2dgcEqyGRkqERAgSuFpObP+juty+kxYyfnadBNCyjgP\ns7u0GmsTt4CZi7BbowNRL6bynrwrmQI9LJI1bPhgqfdDUbqG3HXwHz80oRFfKou8\nJTYKxK4Iumfw2l/uAACma5ZyrwIDBX/H5XEQqch4sORzQnuhlTmZRf6ldVIIWjdJ\nef+DpOt12s+cS2F4D5g8G6t9CprCLYyrXiHwM/U8N5ywL9IeYKSWJxa7si3l9A6o\nZxOds8F/UJYDSIB97MQFzBo=\n=JdC7\n-----END PGP PUBLIC KEY BLOCK-----\n"