# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mop/__about__.py
# Compiled at: 2020-04-07 11:12:59
# Size of source mod 2**32: 378 bytes
import dataclasses
project_name = 'Mop'
version = '0.1.1'
release_name = 'Avalanche Master Song'
author = 'Travis Shirk'
author_email = 'travis@pobox.com'
years = '2020'

@dataclasses.dataclass
class Version:
    major: int
    minor: int
    maint: int
    release: str
    release_name: str


version_info = Version(0, 1, 1, 'final', 'Avalanche Master Song')