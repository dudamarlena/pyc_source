# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_basic.py
# Compiled at: 2015-04-13 16:10:47
test_xml = '<?xml version="1.0"?>\n<!DOCTYPE PyObject SYSTEM "PyObjects.dtd">\n\n<PyObject class="Automobile">\n   <attr name="doors" type="numeric" value="4" />\n   <attr name="make" type="string" value="Honda" />\n   <attr name="tow_hitch" type="None" />\n   <attr name="prev_owners" type="tuple">\n      <item type="string" value="Jane Smith" />\n      <item type="tuple">\n         <item type="string" value="John Doe" />\n         <item type="string" value="Betty Doe" />\n      </item>\n      <item type="string" value="Charles Ng" />\n   </attr>\n   <attr name="repairs" type="list">\n      <item type="string" value="June 1, 1999:\tFixed radiator" />\n      <item type="PyObject" class="Swindle">\n         <attr name="date" type="string" value="July 1, 1999" />\n         <attr name="swindler" type="string" value="Ed\'s Auto" />\n         <attr name="purport" type="string" value="Fix A/C" />\n      </item>\n   </attr>\n   <attr name="options" type="dict">\n      <entry>\n         <key type="string" value="Cup Holders" />\n         <val type="numeric" value="4" />\n      </entry>\n      <entry>\n         <key type="string" value="Custom Wheels" />\n         <val type="string" value="Chrome Spoked" />\n      </entry>\n   </attr>\n   <attr name="engine" type="PyObject" class="Engine">\n      <attr name="cylinders" type="numeric" value="4" />\n      <attr name="manufacturer" type="string" value="Ford" />\n   </attr>\n</PyObject>'
if __name__ == '__main__':
    from gnosis.xml.pickle import XML_Pickler
    import gnosis.xml.pickle as xml_pickle
    from gnosis.xml.pickle.util import add_class_to_store
    import funcs
    funcs.set_parser()

    class MyClass:
        pass


    o = XML_Pickler()
    o.num = 37
    o.str = b"Hello World \n Special Chars: \t \x00 < > & ' \x87"
    o.lst = [1, 3.5, 2, complex(4.0, 7.0)]
    o.lst2 = o.lst
    o2 = MyClass()
    o2.tup = ('x', 'y', 'z')
    o2.tup2 = o2.tup
    o2.num = complex(2.0, 2.0)
    o2.dct = {'this': 'that', 'spam': 'eggs', 3.14: 'about PI'}
    o2.dct2 = o2.dct
    o.obj = o2
    s = o.dumps()
    t = o.loads(s)
    if id(o) == id(t) or id(o.obj) == id(t.obj):
        raise 'ERROR(0)'
    for attr in ['num', 'str', 'lst', 'lst2']:
        if getattr(o, attr) != getattr(t, attr):
            raise 'ERROR(1)'

    for attr in ['tup', 'tup2', 'num', 'dct', 'dct2']:
        if getattr(o.obj, attr) != getattr(t.obj, attr):
            raise 'ERROR(2)'

    u = o.loads(test_xml)
    if u.engine.__dict__ != {'cylinders': 4, 'manufacturer': 'Ford'} or u.repairs[0] != 'June 1, 1999: Fixed radiator' or u.repairs[1].__dict__ != {'date': 'July 1, 1999', 'swindler': "Ed's Auto", 'purport': 'Fix A/C'} or u.make != 'Honda' or u.prev_owners != ('Jane Smith', ('John Doe', 'Betty Doe'), 'Charles Ng') or u.doors != 4 or u.tow_hitch != None or u.options != {'Cup Holders': 4, 'Custom Wheels': 'Chrome Spoked'}:
        raise 'ERROR(4)'
    print '** OK **'