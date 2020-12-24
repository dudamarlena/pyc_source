# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/userschema/zcml.py
# Compiled at: 2007-05-17 18:29:20
from zope.interface import Interface
from zope.interface.interface import InterfaceClass
from zope.schema import Text
from zope.configuration.fields import GlobalInterface
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import Path
from zope.configuration.fields import PythonIdentifier
from zope.configuration.fields import Tokens

class ISynthesizedSchema(Interface):
    """ Base interface for directives which synthesize schemas.
    """
    __module__ = __name__
    name = PythonIdentifier(title='Schema name', description='Name of the synthesized interface.', required=True)
    module = GlobalObject(title='Target module', description='Module into which the synthesized interface will be added.', required=True)
    bases = Tokens(title='Base Interfaces', description='Defaults to (Interface,).', required=False, value_type=GlobalInterface())


class ICSVSchemaDirective(ISynthesizedSchema):
    """ Synthesize a schema from a CSV file.

    Example:

     <configure xmlns="http://namespaces.zope.org/zope"
                xmlns:userschema="http://namespaces.zope.org/userschema">

      <userschema:csv
        file="schema.csv"
        name="IUserDefinedSchema"
        module="somepackage.somemodule"
        />

     </configure>
    """
    __module__ = __name__
    file = Path(title='CSV File', description='Path to the CSV file.  If relative, start from configuring package.', required=True)


def createCSVSchema(file, module, name, bases):
    """ Synthesize a Zope3 schema interface from 'file'.
 
    o Seat the new schema into 'module' under 'name'.
    """
    from userschema.schema import fromCSV
    schema = fromCSV(open(file), name, module.__name__, bases)
    placeholder = getattr(module, name, None)
    if placeholder is not None:
        placeholder.__dict__.update(schema.__dict__)
    else:
        setattr(module, name, schema)
    return


def CSVSchemaDirective(_context, file, module, name, bases=()):
    dummy = InterfaceClass(name=name, __module__=module.__name__)
    setattr(module, name, dummy)
    _context.action(discriminator=(file, module, name), callable=createCSVSchema, args=(file, module, name, bases))


class IHTMLFormSchemaDirective(ISynthesizedSchema):
    """ Synthesize a schema from an HTML form.

    Example:

     <configure xmlns="http://namespaces.zope.org/zope"
                xmlns:userschema="http://namespaces.zope.org/userschema">

      <userschema:htmlform
        file="page_with_form.html"
        form="form_name"
        name="IUserDefinedSchema"
        module="somepackage.somemodule"
        encoding="UTF-8"
        />

     </configure>
    """
    __module__ = __name__
    file = Path(title='HTML File', description='Path to the HTML file.  If relative, start from configuring package.', required=True)
    form = PythonIdentifier(title='Form name', description='Name of the form element.  If blank, use the first form in the page.', required=False)
    encoding = Text(title='Encoding', description='Encoding of the form file.', default='UTF-8', required=False)


def createHTMLFormSchema(file, module, name, form, bases, encoding):
    """ Synthesize a Zope3 schema interface from 'file'.
 
    o Seat the new schema into 'module' under 'name'.
    """
    from userschema.schema import fromHTMLForm
    schema = fromHTMLForm(open(file), name, form, module.__name__, bases, encoding)
    placeholder = getattr(module, name, None)
    if placeholder is not None:
        placeholder.__dict__.update(schema.__dict__)
    else:
        setattr(module, name, schema)
    return


def HTMLFormSchemaDirective(_context, file, module, name, form=None, bases=(), encoding='UTF-8'):
    dummy = InterfaceClass(name=name, __module__=module.__name__)
    setattr(module, name, dummy)
    _context.action(discriminator=(file, module, name), callable=createHTMLFormSchema, args=(file, module, name, form, bases, encoding))


class IXMLSchemaDirective(ISynthesizedSchema):
    """ Synthesize a schema from an XML document.

    Example:

     <configure xmlns="http://namespaces.zope.org/zope"
                xmlns:userschema="http://namespaces.zope.org/userschema">

      <userschema:xml
        file="schema.xml"
        element_name="some_schema"
        name="IUserDefinedSchema"
        module="somepackage.somemodule"
        />

     </configure>
    """
    __module__ = __name__
    file = Path(title='XML File', description='Path to the XML file.  If relative, start from configuring package.', required=True)
    element_name = PythonIdentifier(title='Element name', description='Name of the schema element.  If blank, use the first <schema> elemtn in the document.', required=False)


def createXMLSchema(file, module, name, element_name, bases):
    """ Synthesize a Zope3 schema interface from 'file'.
 
    o Seat the new schema into 'module' under 'name'.
    """
    from userschema.etree import fromXML
    schema = fromXML(open(file).read(), name, element_name, module.__name__, bases)
    placeholder = getattr(module, name, None)
    if placeholder is not None:
        placeholder.__dict__.update(schema.__dict__)
    else:
        setattr(module, name, schema)
    return


def XMLSchemaDirective(_context, file, module, name, element_name=None, bases=()):
    dummy = InterfaceClass(name=name, __module__=module.__name__)
    setattr(module, name, dummy)
    _context.action(discriminator=(file, module, name), callable=createXMLSchema, args=(file, module, name, element_name, bases))