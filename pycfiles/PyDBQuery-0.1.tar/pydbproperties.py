# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pydbproperties.py
# Compiled at: 2015-01-14 13:55:41
from __future__ import print_function
import re, sys
__doc__ = '\nauthor: José Roberto Meza Cabrera\nmail: robertpro01@gmail.com\n\nWith this script, you can use store properties into a\nMySQL table, you can change the name of the table, and\nlist the properties into a output stream or file\nstream, etc.\n'
try:
    import myquerybuilder
except:
    print('MySql Simple Query Builder module not found')
    print('pip install MysqlSimpleQueryBuilder')
    sys.exit(1)

NULL = (
 '', None, (), [], {})

class pydbproperties:
    """
    A Python implements of pyjavaproperties for database
    """

    def __init__(self):
        self._props = {}
        self.bspacere = re.compile('\\\\(?!\\s$)')
        self.othercharre = re.compile('(?<!\\\\)(\\s*\\=)|(?<!\\\\)(\\s*\\:)')
        self._keymap = {}
        self._origprops = {}
        self._keyorder = []
        self._conn = None
        self._table_name = 'pydbproperties'
        self._auto_load = False
        self._auto_store = False
        return

    def set_auto_load(self, boolean):
        """ Set True for working directly with the database """
        self._auto_load = boolean

    def set_auto_store(self, boolean):
        """ Set True for working directly with the database """
        self._auto_store = boolean

    def get_db_connector(self):
        return self._conn

    def _load(self):
        if self._auto_load and self._conn is not None:
            self.load()
        return

    def _store(self):
        if self._auto_store and self._conn is not None:
            self.store()
        return

    def get_property(self, key):
        """ Return a property for the given key """
        self._load()
        return self._props.get(key, '')

    def set_property(self, key, value):
        """ Set the property for the given key """
        if type(key) is str and type(value) is str:
            if len(key) != 0:
                self.process_pair(key, value)
                self._store()
            else:
                raise ValueError("key can't be null!")
        else:
            raise TypeError('both key and value should be strings!')

    def process_pair(self, key, value):
        """ Process a (key, value) pair """
        oldkey = key
        oldvalue = value
        keyparts = self.bspacere.split(key)
        strippable = False
        lastpart = keyparts[(-1)]
        if lastpart.find('\\ ') != -1:
            keyparts[-1] = lastpart.replace('\\', '')
        else:
            if lastpart and lastpart[(-1)] == ' ':
                strippable = True
            key = ('').join(keyparts)
            if strippable:
                key = key.strip()
                oldkey = oldkey.strip()
            curlies = re.compile('{.+?}')
            found = curlies.findall(value)
            for f in found:
                srcKey = f[1:-1]
                if srcKey in self._props:
                    value = value.replace(f, self._props[srcKey], 1)

        self._props[key] = value.strip()
        if key in self._keymap:
            oldkey = self._keymap.get(key)
            self._origprops[oldkey] = oldvalue.strip()
        else:
            self._origprops[oldkey] = oldvalue.strip()
            self._keymap[key] = oldkey
        if key not in self._keyorder:
            self._keyorder.append(key)

    def escape(self, value):
        newvalue = value.replace(':', '\\:')
        newvalue = newvalue.replace('=', '\\=')
        return newvalue

    def unescape(self, value):
        newvalue = value.replace('\\:', ':')
        newvalue = newvalue.replace('\\=', '=')
        return newvalue

    def list(self, out=sys.stdout):
        """ Prints a listing of the properties to the
        stream 'out' which defaults to the standard output """
        self._load()
        if out == sys.stdout or type(out) is file:
            out.write('-- listing properties --\n')
            for key, value in self._props.items():
                out.write(('').join((key, '=', value, '\n')))

        else:
            raise TypeError('Argument should be a file or sys.stdout object!')

    def get_property_dict(self):
        """
        Returns property dict
        """
        self._load()
        return self._props

    def store(self):
        """
        Stores the dict to a database
        """
        try:
            self.create_table()
            for prop in self._keyorder:
                if prop in self._origprops:
                    val = self._origprops[prop]
                    self._conn.ping()
                    if prop == self._conn.one(('key', ), self.get_table_name(), {'key': prop}):
                        self._conn.update(self.get_table_name(), {'value': val}, {'key': prop})
                    else:
                        self._conn.insert(self.get_table_name(), {'key': prop, 'value': val})

        except:
            raise

    def load(self):
        """
        Load properties from database
        """
        try:
            self.create_table()
        except:
            pass

        if self._conn is None:
            raise ValueError('Connection not initialized')
        attr = ('key', 'value')
        if self._table_name in NULL:
            raise ValueError("Table name can't be null")
        self._conn.ping()
        properties_dict = self._conn.select(attr, self._table_name)
        properties_list = [ b.get('key') + '=' + b.get('value') + '\n' for b in properties_dict
                          ]
        self.__parse(properties_list)
        return

    def __parse(self, lines):
        """ Parse a list of lines and create
        an internal property dictionary """
        lineno = 0
        i = iter(lines)
        for line in i:
            lineno += 1
            line = line.strip()
            if not line:
                continue
            if line[0] in ('#', '!'):
                continue
            sepidx = -1
            m = self.othercharre.search(line)
            if m:
                first, last = m.span()
                start, end = 0, first
                wspacere = re.compile('(?<![\\\\\\=\\:])(\\s)')
            else:
                if self.othercharre2.search(line):
                    wspacere = re.compile('(?<![\\\\])(\\s)')
                start, end = 0, len(line)
            m2 = wspacere.search(line, start, end)
            if m2:
                first, last = m2.span()
                sepidx = first
            else:
                if m:
                    first, last = m.span()
                    sepidx = last - 1
                while line[(-1)] == '\\':
                    nextline = i.next()
                    nextline = nextline.strip()
                    lineno += 1
                    line = line[:-1] + nextline

            if sepidx != -1:
                key, value = line[:sepidx], line[sepidx + 1:]
            else:
                key, value = line, ''
            self._keyorder.append(key)
            self.process_pair(key, value)

    def set_table_name(self, table_name):
        """
        Sets table name
        """
        if table_name not in NULL:
            self._table_name = table_name
            return
        raise ValueError("Table name can't be null")

    def get_table_name(self):
        """
        Returns table name
        """
        return self._table_name

    def get_property_names(self):
        """ Return an iterator over all the keys of the property
        dictionary, i.e the names of the properties """
        self._load()
        return self._props.keys()

    def remove_property(self, property):
        """
        Remove a property
        if property is None: remove all properties
        """
        if self._auto_store and self._conn is not None:
            self.remove_property_db(property)
        if property is None:
            self._props = {}
            self._keyorder = []
            self._keymap = {}
        else:
            try:
                self._props.pop(property)
                self._keyorder.remove(property)
                self._keymap.pop(property)
            except:
                pass

        return

    def remove_property_db(self, prop):
        """
        Remove a property directly from a database
        if property is None: remove all properties directly from a database
        """
        if prop is None:
            value = None
        else:
            value = {'key': prop}
        self._conn.ping()
        self._conn.delete(self.get_table_name(), value)
        return

    def __getitem__(self, name):
        """ To support direct dictionary like access """
        return self.get_property(name)

    def __setitem__(self, name, value):
        """ To support direct dictionary like access """
        self.set_property(name, value)

    def conn(self, **kwargs):
        """
        Instance a connection with the database
        """
        try:
            self._conn = myquerybuilder.QueryBuilder(**kwargs)
        except:
            print('An error has occurred\n')
            raise

    def create_table(self):
        """
        Create a table, if you don't use set_table_name() method, the
        name of the table will be default( pydbproperties )
        """

        def validate_table():
            """
            This method is auxiliar to create_table() method, it will
            return True if table definition is correct
            """
            try:
                aux = self._conn.query('describe ' + self._table_name).fetchall()
                key = aux[0]
                value = aux[1]
                if len(aux) != 2 or key['Field'] != 'key' or value['Field'] != 'value' or not key['Type'].lower().startswith('varchar') or not value['Type'].lower().startswith('longtext') or not key['Null'].upper() == 'NO' or not value['Null'].upper() == 'YES':
                    return False
                return True
            except:
                return False

        query = ('\n        create table {0} ( `key` varchar(30) not null,\n        `value` longtext null, primary key (`key`));\n        ').format(self.get_table_name())
        try:
            self._conn.ping()
            self._conn.query(query)
        except:
            pass

        return validate_table()