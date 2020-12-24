# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ifacetools\fbtest\use.py
# Compiled at: 2019-08-12 20:51:57
# Size of source mod 2**32: 667 bytes
from django.forms.models import model_to_dict
import factory
from fbtest.userfc import UserFactory
from fbtest.school import School
seq = []
uf = UserFactory()
print(uf.__dict__)
seq.append(uf.__dict__)
seq.append(UserFactory().__dict__)
print(seq)
list = []
fss = factory.build_batch(UserFactory, 4)
for fs in fss:
    list.append(fs.__dict__)

print(list)
uff = UserFactory(shipped=True)
print(uff.__dict__)