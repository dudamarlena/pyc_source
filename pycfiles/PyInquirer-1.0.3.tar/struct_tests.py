# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\struct_tests.py
# Compiled at: 2013-10-27 20:36:12
from pyinq.tags import *

@TestClass
class Class1(object):

    @BeforeClass
    def setupClass():
        print 'setup Class1'

    @Before
    def setup():
        print 'setup test in Class1'

    @Test
    def test1():
        print 'test1 in Class1'

    @Test
    def test2():
        print 'test2 in Class1'

    @After
    def tearDown():
        print 'tear down test in Class1'

    @AfterClass
    def tearDownClass():
        print 'tear down Class1'


@TestClass
class Class2(object):

    @BeforeClass
    def setupClass():
        print 'setup Class2'

    @Before
    def setup():
        print 'setup test in Class2'

    @Test
    def test1():
        print 'test1 in Class2'

    @After
    def tearDown():
        print 'tear down test in Class2'

    @AfterClass
    def tearDownClass():
        print 'tear down Class2'


@BeforeModule
def setupModule():
    print 'setup module'


@AfterModule
def tearDownModule():
    print 'tear down module'


@BeforeClass
def setupMain():
    print 'setup main'