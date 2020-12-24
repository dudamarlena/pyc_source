# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sparrow/interfaces.py
# Compiled at: 2009-07-20 09:57:48
from zope.interface import Interface, Attribute

class ITripleStore(Interface):

    def connect(uri):
        """
        Connect to database, retrieve an ITripleStore instance
        """
        pass

    def disconnect():
        """
        Disconnect the database
        """
        pass

    def contexts():
        """
        Return a list of context names
        """
        pass

    def clear(context_name):
        """
        Remove all triples from a context
        """
        pass

    def register_prefix(prefix, namespace):
        """
        Register a namespace with a specific prefix
        These will be used in serializing rdfxml
        if backend supports this
        """
        pass

    def count(context_name=None):
        """
        Return the number of triples in the database or
        None if the backend does not support this
        Optionally a context_name can be specified
        """
        pass

    def add_rdfxml(uri_string_or_file, context_name, base_uri):
        """
        Add triples data in rdfxml format to a specific context
        
        data can be either a URI string starting with 'http://' or 'file://',
        it can also be a string containing the data, or a file like
        object with a read, seek, and close method.      
        """
        pass

    def add_ntriples(uri_string_or_file, context_name):
        """
        Add triples data in ntriples format to a specific context
        
        data can be either a URI string starting with 'http://' or 'file://',
        it can also be a string containing the data, or a file like
        object with a read, seek, and close method.      
        """
        pass

    def add_turtle(uri_string_or_file, context_name):
        """
        Add triples data in turtle format to a specific context
        
        data can be either a URI string starting with 'http://' or 'file://',
        it can also be a string containing the data, or a file like
        object with a read, seek, and close method.      
        """
        pass

    def add_json(uri_string_or_file, context_name):
        """
        Add triples data in json format to a specific context
        
        data can be either a URI string starting with 'http://' or 'file://',
        it can also be a string containing the data, or a file like
        object with a read, seek, and close method.      
        """
        pass

    def add_dict(dictionary, context_name):
        """
        Add triples data as a python dictionary to a specific context
        """
        pass

    def remove_rdfxml(uri_string_or_file, context_name, base_uri):
        """
        Remove triples data in rdfxml format from a specific context
        
        data can be either a URI string starting with 'http://' or 'file://',
        it can also be a string containing the data, or a file like
        object with a read, seek, and close method.      
        """
        pass

    def remove_ntriples(uri_string_or_file, context_name):
        """
        Remove triples data in ntriples format from a specific context
        
        data can be either a URI string starting with 'http://' or 'file://',
        it can also be a string containing the data, or a file like
        object with a read, seek, and close method.      
        """
        pass

    def remove_turtle(uri_string_or_file, context_name):
        """
        Remove triples data in turtle format from a specific context
        
        data can be either a URI string starting with 'http://' or 'file://',
        it can also be a string containing the data, or a file like
        object with a read, seek, and close method.      
        """
        pass

    def remove_json(uri_string_or_file, context_name):
        """
        Remove triples data in json format from a specific context
        
        data can be either a URI string starting with 'http://' or 'file://',
        it can also be a string containing the data, or a file like
        object with a read, seek, and close method.      
        """
        pass

    def remove_dict(dictionary, context_name):
        """
        Remove triples data as a python dictionary from a specific context
        """
        pass

    def get_rdfxml(context_name, pretty=False):
        """
        Returns a file object (something with a read and close method)
        containing the triple data from a specific context in rdfxml format
        """
        pass

    def get_ntriples(context_name):
        """
        Returns a file object (something with a read and close method)
        containing the triple data from a specific context in ntriples format
        """
        pass

    def get_turtle(context_name):
        """
        Returns a file object (something with a read and close method)
        containing the triple data from a specific context in turtle format
        """
        pass

    def get_json(context_name):
        """
        Returns a file object (something with a read and close method)
        containing the triple data from a specific context in json format
        """
        pass

    def get_dict(context_name):
        """
        Returns a python dictionary containing the triple data
        from a specific context
        """
        pass


class ISPARQLEndpoint(Interface):

    def select(sparql_query):
        """
        Run a sparql SELECT query, returns a list
        of dictionaries in sparql result format (json-like)
        """
        pass

    def ask(sparql_query):
        """
        Run a sparql ASK query, returns a boolean
        """
        pass

    def construct(sparql_query, format):
        """
        Run a sparql CONSTRUCT query, returns a
        filestream with triples in the specifed format
        or None if no result was found
        """
        pass