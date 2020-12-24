# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyjld\system\command\ui.py
# Compiled at: 2009-04-06 10:21:28
__doc__ = ' \npyjld.system.command.ui\n'
__author__ = 'Jean-Lou Dupont'
__fileid = '$Id: ui.py 44 2009-04-06 14:21:24Z jeanlou.dupont $'
__all__ = [
 'BaseCmdUI', 'BaseCmdUIConfigError', 'ExOptionParser']
import sys
from string import Template
from optparse import OptionParser, Option

class BaseCmdUIConfigError(Exception):
    """
    Base exception class for this module
    """

    def __init__(self, msg, params=None):
        Exception.__init__(self, msg)
        self.msg = msg
        self.params = params


class ExOptionParser(OptionParser):
    """
    Enhances the standard library's OptionParser class
    
    Adds the method :meth:`ex_add_options`
    """

    def __init__(self, *pargs, **kwargs):
        OptionParser.__init__(self, *pargs, **kwargs)

    def ex_add_options(self, options_list):
        """
        Adds options through a keyword dictionary only.
        This constrasts to :meth:`add_options` which goes 
        through hoops to support both positional &
        keyword based argument list.
        
        This method translates the `options_list` for
        the base class.
        
        :param options_list: a list of dictionaries containing the options
        
        Each dictionary entry (i.e. each list item) will be translated
        to comply with the standard base class OptionParser. Furthermore,
        only options which are supported by the base class are passed
        to the OptionParser: this behavior allows for extending the 
        ``options_list`` entries (i.e. each dictionary item) with custom
        keys without breaking OptionParser.
        
            [ { option } ... ]
    
        In each `option`, the keys which are translated are:
            * short
            * long
            
        Thus, a full option list can be passed to :meth:`ex_add_options` 
        without worrying about the special cases *short* and *long* 
        positional arguments.

        """
        translated_options = []
        for option_dict in options_list:
            short = option_dict.get('short', None)
            long = option_dict.get('long', None)
            popt = [short, long]
            popt = filter(None, popt)
            filtered_keys = filter(lambda X: X in Option.ATTRS, option_dict)
            filtered_dict = dict([ (key, option_dict[key]) for key in option_dict if key in filtered_keys
                                 ])
            translated_options.append((popt, filtered_dict))

        for (popt, fdict) in translated_options:
            if not popt:
                raise RuntimeError('missing `short` and/or `long` keys')
            self.add_option(*popt, **fdict)

        return


class BaseCmdUI(object):
    """ 
    Base class for Command Line UI
    
    :param msgs: messages object
    :param template_factory: the factory for creating templates out of ``message_id``
    
    **Messages object**
    
    This object can be controlled with through ``template_factory``; the latter
    must implement a ``safe_substitute`` method for rendering the ``message_id``
    with the given ``parameters`` to a message string.

    """
    _platform_win32 = sys.platform[:3] == 'win'

    def __init__(self, msgs, ref_options, logger=None, template_factory=None):
        self.logger = logger
        self.msgs = msgs
        self.options = None
        self.args = None
        self.command = None
        self.ref_options = ref_options
        if not ref_options:
            raise RuntimeError('ref_options is invalid')
        if template_factory is None:
            self.template_factory = Template
        else:
            self.template_factory = template_factory
        return

    def popArg(self):
        """ 
        Pops one argument from the list
        """
        return self.args.pop(0)

    def handleError(self, exc):
        """ 
        Displays, if required, an appropriate user message
        corresponding to an error condition.
            
        :param exc: Exception being raised
        
        :rtype: boolean True if the exception was handled
                successfully i.e. a message was found and
                rendered correctly.
        """
        try:
            already_handled = exc.already_handled
        except:
            already_handled = False

        if already_handled:
            return True
        try:
            msg_key = exc.msg
        except:
            try:
                msg_key = exc.msg_id
            except:
                msg_key = None

        try:
            params = exc.params
        except:
            params = None

        msg_found = False
        if msg_key:
            try:
                msg_base = self.msgs.get(msg_key, None)
                msg_tpl = self.template_factory(msg_base)
                msg = msg_tpl.safe_substitute(params)
                msg_found = True
            except:
                msg = str(exc)

        else:
            msg = str(exc)
        try:
            self.logger.error(msg)
        except:
            print msg

        return msg_found

    def _resolveHelp(self, entry):
        if self._platform_win32:
            if 'help_win' in entry:
                return entry.get('help_win', None)
        if not self._platform_win32:
            if 'help_nix' in entry:
                return entry.get('help_nix', None)
        if 'help' in entry:
            return entry.get('help', None)
        return

    def handleArguments(self, cmd=None, usage_msg=None, args=None, help_params=None):
        """ 
        Processes command line options
        
        :param usage_msg: usage message string 
        :param config_options: the options configuration dictionary
        :param args: the arguments from the command-line
        :param help_params: dictionary of parameters used to render the ``help`` messages
 
        """
        try:
            usage_msg_tpl = self.template_factory(usage_msg)
            params = {'commands': cmd.commands_help}
            msg = usage_msg_tpl.safe_substitute(params)
        except:
            msg = usage_msg

        parser = ExOptionParser(usage=msg)
        parser.ex_add_options(self.ref_options)
        (self.options, self.args) = parser.parse_args(args)
        try:
            self.command = self.args[0]
        except:
            self.command = None

        return

    def updateRegistry(self, reg):
        """
        Updates the registry from the command-line args
        
        Goes through the ``args``, verifies if the ``reg``
        option is to be found in the ``ref_options`` dictionary
        and updates accordingly the registry.
        
        :param reg: the dictionary registry
        :param ref_options: the reference options list
        :param options: the processed command-line arguments
        
        The registry is a dictionary.
        """
        if reg is None:
            return
        for o in self.ref_options:
            do_update = o.get('reg', False)
            if do_update:
                key = o.get('dest', None)
                if key is None:
                    raise RuntimeError('Missing "dest" key in ref_options')
                val = getattr(self.options, key, None)
                if val is not None:
                    reg[key] = val

        return reg

    def copyOptions(self, target):
        """ 
        Copies all `var` entries from the ``source`` dictionary
        following the ``ref_options`` dictionary into the
        ``target`` dictionary.

        :param source: source dictionary
        :param target: target object
        :param ref_options: the reference options list
        """
        for o in self.ref_options:
            key = o.get('dest', None)
            if key is None:
                raise RuntimeError("Missing 'dest' key in ref_options")
            val = getattr(self.options, key, None)
            setattr(target, key, val)

        return

    def integrateRegistry(self, cmd, reg):
        """
        Integrate values from the registry where ``None``
        values are found in the ``cmd`` object
         
        :param cmd: the ``cmd`` object
        :rtype: keys list for all replacement performed 
        
        """
        keys = []
        for (key, value) in cmd.iterconfig():
            if value is None:
                reg_value = reg.get(key, None)
                setattr(cmd, key, reg_value)
                keys.append(key)

        return keys

    def prepareCmd(self, cmd, reg):
        """
        Prepare the command ``cmd`` object
        
        1. Options from the command-line have precedence over any other.
        2. Options with ''None'' value are updated with matching registry value
        3. The registry is updated where necessary
         
        """
        if self.options is None:
            raise RuntimeError('prepareCmd should only be called after handleArguments')
        self.updateRegistry(reg)
        self.copyOptions(cmd)
        self.integrateRegistry(cmd, reg)
        return

    def dispatchCommand(self, cmd):
        """
        """
        if self.command is None:
            return
        cmd.validateCommand(self.command)
        self.popArg()
        return getattr(cmd, 'cmd_%s' % self.command)(self.args)