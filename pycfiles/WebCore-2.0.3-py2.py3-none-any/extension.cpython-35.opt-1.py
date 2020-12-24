# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/core/extension.py
# Compiled at: 2016-09-25 02:28:40
# Size of source mod 2**32: 5479 bytes
"""WebCore extension management.

This extension registry handles loading and access to extensions as well as the collection of standard WebCore
Extension API callbacks. Reference the `SIGNALS` constant for a list of the individual callbacks that can be
utilized and their meanings, and the `extension.py` example for more detailed descriptions.

At a basic level an extension is a class. That's it; attributes and methods are used to inform the manager
of extension metadata and register callbacks for certain events. The most basic extension is one that does
nothing:

        class Extension: pass

To register your extension, add a reference to it to your project's `entry_points` in your project's `setup.py`
under the `web.extension` namespace:

        setup(
                ...,
                entry_points = {'web.extension': [
                                'example = myapp:Extension',
                        ]},
        )

Your extension may define several additional properties:

* `provides` -- declare a set of tags describing the features offered by the plugin
* `needs` -- delcare a set of tags that must be present for this extension to function
* `uses` -- declare a set of tags that must be evaluated prior to this extension, but aren't hard requirements
* `first` -- declare that this extension is a dependency of all other non-first extensions if truthy
* `last` -- declare that this extension depends on all other non-last extensions if truthy
* `signals` -- a set of additional signal names declared used (thus cacheable) by the extension manager

Tags used as `provides` values should also be registered as `web.extension` entry points. Additional `signals` may be
prefixed with a minus symbol (-) to request reverse ordering, simulating the exit path of WSGI middleware.

"""
from __future__ import unicode_literals
from marrow.package.host import ExtensionManager
from .compat import items
from .context import Context
log = __import__('logging').getLogger(__name__)

class WebExtensions(ExtensionManager):
    __doc__ = 'Principal WebCore extension manager.'
    SIGNALS = {
     'start',
     'stop',
     'graceful',
     'prepare',
     'dispatch',
     'before',
     'mutate',
     '-after',
     '-transform',
     '-done',
     '-middleware'}
    __isabstractmethod__ = False

    def __init__(self, ctx):
        """Extension registry constructor.
                
                The extension registry is not meant to be instantiated by third-party software. Instead, access the registry
                as an attribute of the current Application or Request context: `context.extension`
                
                Currently, this uses some application-internal shenanigans to construct the initial extension set.
                """
        self.feature = set()
        all = self.all = self.order(ctx.app.config['extensions'])
        signals = {}
        inverse = set()

        def add_signal(name):
            if name[0] == '-':
                name = name[1:]
                inverse.add(name)
            signals[name] = []

        for signal in self.SIGNALS:
            add_signal(signal)

        for ext in all:
            self.feature.update(getattr(ext, 'provides', []))
            for signal in getattr(ext, 'signals', []):
                add_signal(signal)

        for ext in all:
            for signal in signals:
                handler = getattr(ext, signal, None)
                if handler:
                    signals[signal].append(handler)

            if hasattr(ext, '__call__'):
                signals['middleware'].append(ext)

        for signal in inverse:
            signals[signal].reverse()

        self.signal = Context(**{k:tuple(v) for k, v in items(signals)})
        self.signal['pre'] = tuple(signals['prepare'] + signals['before'])
        super(WebExtensions, self).__init__('web.extension')