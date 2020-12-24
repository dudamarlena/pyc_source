# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: sisl/info.py
# Compiled at: 2020-02-10 09:23:58
released = True
git_revision = '13a327bd8e27d689f119bafdf38519bab7f6e0f6'
git_revision_short = git_revision[:7]
git_count = 72
major = 0
minor = 9
micro = 8
version = ('.').join(map(str, [major, minor, micro]))
release = version
if git_count > 2 and not released:
    version += '+' + str(git_count)
bibtex = ('@misc{{zerothi_sisl,\n    author = {{Papior, Nick}},\n    title  = {{sisl: v{0}}},\n    year   = {{2020}},\n    doi    = {{10.5281/zenodo.597181}},\n    url    = {{https://doi.org/10.5281/zenodo.597181}},\n}}').format(version)

def cite():
    return bibtex