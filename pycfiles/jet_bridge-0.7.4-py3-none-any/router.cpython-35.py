# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge/jet_bridge/router.py
# Compiled at: 2019-11-10 09:36:35
# Size of source mod 2**32: 2418 bytes


class Router(object):
    routes = [
     {'path': '', 
      'method_mapping': {'get': 'list', 
                         'post': 'create'}, 
      
      'detail': False},
     {'path': '(?P<pk>[^/]+)/', 
      'method_mapping': {'get': 'retrieve', 
                         'put': 'update', 
                         'patch': 'partial_update', 
                         'delete': 'destroy'}, 
      
      'detail': True}]
    urls = []

    def add_handler(self, view, url, actions):

        class ActionHandler(view):
            pass

        for method, method_action in actions.items():

            def create_action_method(action):

                def action_method(inner_self, *args, **kwargs):
                    inner_self.view.action = action
                    inner_self.before_dispatch()
                    response = inner_self.view.dispatch(action, *args, **kwargs)
                    inner_self.write_response(response)

                return action_method

            func = create_action_method(method_action)
            setattr(ActionHandler, method, func)

        self.urls.append((url, ActionHandler))

    def add_route_actions(self, view, route, prefix):
        viewset = view.view
        actions = route['method_mapping']
        actions = dict(filter(lambda x: hasattr(viewset, x[1]), actions.items()))
        if len(actions) == 0:
            return
        url = '{}{}'.format(prefix, route['path'])
        self.add_handler(view, url, actions)

    def add_route_extra_actions(self, view, route, prefix):
        viewset = view.view
        for attr in dir(viewset):
            method = getattr(viewset, attr)
            bind_to_methods = getattr(method, 'bind_to_methods', None)
            if bind_to_methods is None:
                pass
            else:
                detail = getattr(method, 'detail', None)
                if detail != route['detail']:
                    pass
                else:
                    extra_actions = dict(map(lambda x: (x, attr), bind_to_methods))
                    url = '{}{}{}/'.format(prefix, route['path'], attr)
                    self.add_handler(view, url, extra_actions)

    def register(self, prefix, view):
        for route in self.routes:
            self.add_route_extra_actions(view, route, prefix)

        for route in self.routes:
            self.add_route_actions(view, route, prefix)