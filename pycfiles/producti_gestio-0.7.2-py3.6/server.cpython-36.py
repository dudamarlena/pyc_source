# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/server/server.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 18285 bytes
"""
producti_gestio.server.server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This section contains the :class:`producti_gestio.server.server.Server` class, the main class
of the entire library.

It could create the web-server, set the configuration by the
init function or using set_* functions.

You can create handlers (using :func:`producti_gestio.server.server.Server.on_request` or not)
and start using it simply using :func:`producti_gestio.server.server.Server.run` or
:func:`producti_gestio.server.server.Server.start` for who's gonna use Threads.

The :class:`producti_gestio.Server` allows a custom configuration that you
can pass when you create a new instance as ``kwargs``:

    * *allow_get* (``bool``): If you want to allow ``GET`` requests. **Default is False**
    * *allow_post* (``bool``): If you want to allow ``POST`` requests. **Default is True**
    * *function* (``callable``): Your ``handler_function``, it won't be considered if you're using Handlers.
    * *debug* (``bool``): If you want to get **debugging infos**
    * *ip** (``str``): Your ``ip``. **Default is 127.0.0.1**
    * *port* (``int``): Your ``server post``. **Default is 8000**

Here an example:

.. code-block:: python

    from producti_gestio import Server

    my_server = Server(allow_get=True, allow_post=False) # Create the Server instance

    def my_function(**kwargs):
        return {
            'response_code': 200,
            'response': {
                'ok': True,
                'message': 'Hello world!'
            }
        }

    my_server.set_function(my_function) # Set the handler function
    my_server.start() # Run the server using threads

    while True:
        pass

Or using :class:`producti_gestio.handlers.handler` and :class:`producti_gestio.filters.filter`:

.. code-block:: python

    from producti_gestio import Server, Filter

    my_server = Server(allow_get=True, allow_post=False) # Create the Server instance

    @my_server.on_request(Filter.get) # Define the decorator for the function (it uses Filters)
    def my_function(**kwargs): # Define the handler function
        return {
            'response_code': 200, # The response code
            'response': { # A dict of the response (it will be encoded in JSON)
                'ok': True,
                'message': 'Hello world!'
            }
        }

    my_server.start() # Run the server using threads

    while True:
        pass
"""
from http.server import HTTPServer
from producti_gestio.core import RequestHandler
from producti_gestio.exceptions import NotAFunction, NotABoolean, NotAString, NotAnInteger, NotDefinedFunction
from producti_gestio.handlers import Handler
from typing import NewType
configuration: object = NewType('Configuration', dict)

class Server:
    __doc__ = 'The main class.\n    It is used to create, edit\n    configuration and launch the\n    web server.\n    '
    thread_activated: bool
    try:
        import _thread
        thread_activated: bool = True
    except ImportError:
        _thread = None
        thread_activated: bool = False

    def __init__(self, **conf: configuration):
        """
        It defines the configuration by
        merging the default configuration with
        the user-chosen configuration.

        Args:
            conf (configuration): The chosen configuration. See :mod:`producti_gestio.server.server`.
        """
        default_configuration = {'allow_get':False, 
         'allow_post':True, 
         'function':lambda **kwargs: {'response_code':403, 
          'response':{'ok': False}}, 
         'debug':False, 
         'ip':'127.0.0.1', 
         'port':8000}
        self.configuration = default_configuration
        self.configuration.update(conf)
        self.running = False
        self.server = None
        self.use_handler = False
        self.handlers = []

    def __repr__(self) -> str:
        """
        It returns a representation
        of the object.

        Returns:
            str: A representation of the object
        """
        return 'ProductiGestio(**' + repr(self.configuration) + ')'

    def add_handler(self, handler: object) -> bool:
        """It adds an handler to the
        server object.

        Here an example:

        .. code-block:: python

            from producti_gestio import Server
            from producti_gestio.handlers.handler import Handler

            my_server = Server(allow_get=True) # Create the Server instance.
            my_handler = Handler(lambda parameters: bool(parameters['path'] == '/test')) # Create the handler

            my_server.add_handler(my_handler) # Add the handler to the Server object
            my_server.start() # Run the server using threads

        Args:
          handler(Handler): The Handler
          handler: object:

        Returns:
          bool: True if all went right, False on fails

        """
        self.use_handler = True
        self.handlers.append(handler)

    def remove_handler(self, handler: object) -> bool:
        """It removes an handler
        from the
        server object.

        Here an example:

        .. code-block:: python

            from producti_gestio import Server
            from producti_gestio.handlers.handler import Handler

            my_server = Server(allow_get=True) # Create the Server instance.
            my_handler = Handler(lambda parameters: bool(parameters['path'] == '/test')) # Create the handler
            other_handler = Handler(lambda parameters: bool(parameters['path'] == '/second_test')) # Create the other handler

            my_server.add_handler(my_handler) # Add the handler to the Server object
            my_server.start() # Start the server using threads

            my_server.add_handler(other_handler) # Add the other handler to the Server object
            my_server.remove_handler(my_handler) # Remove 'my handler' from the Server object

        Args:
          handler(Handler): The Handler
          handler: object:

        Returns:
          bool: True if all went right, False on fails
        """
        if len(self.handlers) == 0:
            self.use_handler = False
        self.handlers.remove(handler)

    def stop(self):
        """It stops the server, you
        can re-put it on in by
        re-calling the run function.
        """
        self.running = False

    def shutdown(self):
        """It shutdowns the server."""
        self.running = False
        self.server.socket.close()
        self.server.shutdown()

    def set_function(self, handler_function: callable) -> bool:
        """It sets the function by the handler_function parameter.

        Here an example:
        
        .. code-block:: python
        
            from producti_gestio import Server
            
            my_server = Server() # Create the server instance
            
            def my_function(**kwargs): # It creates the function
                return {
                    'response_code': 200, # The Response Code
                    'response': {
                        'ok': True
                    }
                }
                
            my_server.set_function(my_function) # Set the handler function
            my_server.start() # Start the server using Threads
            
        Args:
          handler_function(callable): The user-defined function you would like to set.
          handler_function: callable:

        Raises:
          NotAFunction: It throws a NotAFunction exception if the given parameter is not a function.

        """
        if callable(handler_function):
            self.configuration['function'] = handler_function
            return True
        raise NotAFunction()

    def set_allow_get(self, allow_get: bool) -> bool:
        """It sets if the GET method
        is allowed by the allow_get parameter.
        
        **Remember:** The *GET* method is **not** allowed on by default!
                
        Here an example:
        
        .. code-block:: python
        
            from producti_gestio import Server
            
            my_server = Server() # Create the server instance
            
            @my_server.on_request
            def my_function(**kwargs):
                return {
                    'response_code': 200, # The Response Code
                    'response': {
                        'ok': True
                    }
                }
                
            my_server.set_allow_get(True) # Allow GET requests
            my_server.start() # Start the server using Threads

        Args:
          allow_get(bool): A boolean of the choice.
          allow_get: bool:

        Raises:
          NotABoolean: It throws a NotABoolean exception if the given parameter is not a boolean.

        """
        if isinstance(allow_get, bool):
            self.configuration['allow_get'] = allow_get
            return True
        raise NotABoolean()

    def set_allow_post(self, allow_post: bool) -> bool:
        """It sets if the POST method
        is allowed by the allow_post parameter.
        
        **Remember:** The *POST* method is allowed by default!
                
        Here an example:
        
        .. code-block:: python
        
            from producti_gestio import Server
            
            my_server = Server() # Create the server instance
            
            @my_server.on_request
            def my_function(**kwargs):
                return {
                    'response_code': 200, # The Response Code
                    'response': {
                        'ok': True
                    }
                }
                
            my_server.set_allow_post(True) # Allow POST requests
            my_server.start() # Start the server using Threads

        Args:
          allow_post(bool): A boolean of the choice.
          allow_post: bool:

        Raises:
          NotABoolean: It throws a NotABoolean exception if the given parameter is not a boolean.

        """
        if isinstance(allow_post, bool):
            self.configuration['allow_post'] = allow_post
            return True
        raise NotABoolean()

    def set_debug_mode(self, debug: bool) -> bool:
        """It sets if the Debug mode
        is on.
        
        Here an example:
        
        .. code-block:: python
        
            from producti_gestio import Server
            
            my_server = Server() # Create the server instance
            
            @my_server.on_request
            def my_function(**kwargs):
                return {
                    'response_code': 200, # The Response Code
                    'response': {
                        'ok': True
                    }
                }
                
            my_server.set_debug_mode(True) # Enable the debug mode
            my_server.start() # Start the server using Threads

        Args:
          debug(bool): A boolean of the choice.
          debug: bool:

        Raises:
          NotABoolean: It throws a NotABoolean exception if the given parameter is not a boolean.

        """
        if isinstance(debug, bool):
            self.configuration['debug'] = debug
            return True
        raise NotABoolean()

    def set_ip(self, ip: str) -> bool:
        """It sets the IP by the IP parameter.
        
        Here an example:
        
        .. code-block:: python
        
            from producti_gestio import Server
            
            my_server = Server() # Create the server instance
            
            @my_server.on_request
            def my_function(**kwargs):
                return {
                    'response_code': 200, # The Response Code
                    'response': {
                        'ok': True
                    }
                }
                
            my_server.set_ip('127.0.0.1') # Set the IP
            my_server.start() # Start the server using Threads

        Args:
          ip(str): The IP you chose
          ip: str:

        Raises:
          NotAString: It throws a NotAString exception if the given parameter is not a string.

        """
        if isinstance(ip, str):
            self.configuration['ip'] = ip
            return True
        raise NotAString()

    def set_port(self, port: int) -> bool:
        """It sets the Port by the Port parameter.
        
        Here an example:
        
        .. code-block:: python
        
            from producti_gestio import Server
            
            my_server = Server() # Create the server instance
            
            @my_server.on_request
            def my_function(**kwargs):
                return {
                    'response_code': 200, # The Response Code
                    'response': {
                        'ok': True
                    }
                }
                
            my_server.set_port(8000) # Set the Port
            my_server.start() # Start the server using Threads

        Args:
          port(int): The Port you chose.
          port: int:

        Raises:
          NotAnInteger: It throws a NotAnInteger exception if the given parameter is not an integer.

        """
        if isinstance(port, int):
            self.configuration['port'] = port
            return True
        raise NotAnInteger()

    def on_request(self, filters: object or None=None) -> callable:
        """It adds the function
        to the handler.

        It could be used as a decorator, here an example:

        .. code-block:: python

            from producti_gestio import Server, Filters

            my_server = Server(allow_get=True) # Create the Server instance

            @my_server.on_request(Filters.get) # Create and add an handler using Filters
            der my_function(**kwargs):
                return {
                    'response_code': 200, # The response code
                    'response' : {
                        'ok': True
                    }
                }

            my_server.start() # Start the server using Threads

        Args:
          filters(Filter): The filters you'd like to use
          filters: object or None:  (Default value = None)

        Returns:
          callable: A decorator function

        """

        def decorator(func):
            self.add_handler(Handler(func, filters))
            return func

        return decorator

    def start(self) -> bool:
        """It starts the server.
        If ``thread_activated`` is ``True``, it
        starts the server using ``_thread``, else it
        just calls :func:`producti_gestio.server.server.Server.run`.

        Returns:
          bool: True if all went right, False on fails

        """
        try:
            if not self.thread_activated:
                raise Exception()
            self._thread.start_new_thread(self.run, ())
            return True
        except Exception as e:
            print(str(e))
            try:
                self.server.run()
                return True
            except Exception as error:
                print(str(error))
                return False

    def run(self, handler_class=RequestHandler):
        """It launches the server and
        add the configuration to
        the Handler class.
        
        **Remember:** It doesn't use ``_thread``, see :func:`producti_gestio.server.server.Server.start` for that.

        Args:
          handler_class(classobj|type, optional): The Handler class you would like to use. Default is :class:`producti_gestio.core.request_handler.RequestHandler`.

        Raises:
          NotDefinedFunction: It throws a NotDefinedFunction exception if the handler function is not defined.

        """
        if not callable(self.configuration['function']):
            if not self.use_handler:
                raise NotDefinedFunction()
        else:
            server_address = (
             self.configuration['ip'],
             self.configuration['port'])
            self.server = HTTPServer(server_address, handler_class)
            if self.use_handler:
                self.configuration['function'] = None
                self.server.RequestHandlerClass.configuration = self.configuration
                self.server.RequestHandlerClass.handlers = self.handlers
                self.server.RequestHandlerClass.use_handler = True
            else:
                self.server.RequestHandlerClass.configuration = self.configuration
            self.server.RequestHandlerClass.use_handler = False
        self.running = True
        while self.running:
            self.server.handle_request()