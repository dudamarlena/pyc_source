# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ifacetools\fbtest\userfc.py
# Compiled at: 2019-08-12 20:51:57
# Size of source mod 2**32: 929 bytes
import factory, factory.fuzzy
from fbtest.user import User
from fbtest.school import School
from fbtest.numpv import NumProvider
factory.Faker.add_provider(NumProvider)

class SchoolFactory(factory.Factory):

    class Meta:
        model = School

    schoolName = factory.sequence(lambda n: 'school%04d' % n)


class UserFactory(factory.Factory):

    class Meta:
        model = User

    name = factory.Faker('name', locale='zh_CN')
    num = factory.Faker('num')
    age = factory.fuzzy.FuzzyInteger(42)
    city = factory.Faker('address', locale='zh_CN')
    phone = factory.fuzzy.FuzzyText('138', 7, '1', '1234567890')
    school = factory.SubFactory(SchoolFactory)

    class Params:
        shipped = factory.Trait(name=None)