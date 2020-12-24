# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylxca/pylxca_cmd/lxca_cmd.py
# Compiled at: 2020-03-12 01:38:00
# Size of source mod 2**32: 29901 bytes
__doc__ = '\n@since: 15 Sep 2015\n@author: Prashant Bhosale <pbhosale@lenovo.com>\n@license: Lenovo License\n@copyright: Copyright 2016, Lenovo\n@organization: Lenovo \n@summary: This module provides command class implementation for PyLXCA \n'
import sys, getopt, logging, traceback
from getpass import getpass
import json, argparse, pylxca.pylxca_api
from pylxca.pylxca_api.lxca_rest import HTTPError
from pylxca.pylxca_api.lxca_connection import ConnectionError
from pylxca.pylxca_cmd.lxca_icommands import InteractiveCommand
logger = logging.getLogger(__name__)

class connect(InteractiveCommand):
    """connect"""

    def handle_command(self, opts, args):
        """
        try:
            parser = self.get_argparse_options()
            namespace = parser.parse_args(args)
        except argparse.ArgumentError as e:
            self.invalid_input_err()
            return
        except SystemExit as e:
            # -h and --help land here
            return

        for opt, arg in opts:
            if '-h' in opt:
                self.sprint (self.__doc__)
                return                

        if not opts:
            self.handle_no_input()
            return
        
        opt_dict = self.parse_args(opts, argv)
        """
        try:
            opt_dict = self.parse_args(args)
            if opt_dict.get('pw', None) == None:
                opt_dict['pw'] = getpass('Enter Password: ')
        except SystemExit as e:
            return

        out_obj = None
        try:
            out_obj = self.handle_input(opt_dict)
            self.handle_output(out_obj)
        except HTTPError as re:
            self.sprint('Exception %s occurred while executing command.' % re)
        except ConnectionError as re:
            self.sprint('Exception %s occurred while executing command.' % re)
        except RuntimeError:
            self.sprint('Session Error to LXCA, Try connect')
        except Exception as err:
            self.sprint('Exception occurred: %s' % err)

        return out_obj

    def handle_no_input(self, con_obj=None):
        self.invalid_input_err()

    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint('Failed to connect given LXCA ')
        else:
            self.sprint('Connection to LXCA successful')


class disconnect(InteractiveCommand):
    """disconnect"""

    def handle_no_input(self, con_obj=None):
        api = pylxca.pylxca_api.lxca_api()
        if api.disconnect() == True:
            self.sprint('Connection with LXCA closed successfully ')
        else:
            self.sprint('Failed to close connection with LXCA ')


class log(InteractiveCommand):
    """log"""

    def handle_no_input(self, con_obj=None):
        api = pylxca.pylxca_api.lxca_api()
        self.sprint('Current Log Level is set to ' + str(api.get_log_level()))
        message = '\nPossible Log Levels, Please use following values to set desired log level. \n\n\tDEBUG:        Detailed information, typically of interest only when diagnosing problems.\n\tINFO:        Confirmation that things are working as expected.\n\tWARNING:    An indication that something unexpected happened, or indicative of some problem in the near future. \n\tERROR:        Due to a more serious problem, the software has not been able to perform some function.\n\tCRITICAL:    A serious error, indicating that the program itself may be unable to continue running.\n'
        self.sprint(message)

    def handle_output(self, out_obj):
        api = pylxca.pylxca_api.lxca_api()
        if out_obj == True:
            self.sprint('Current Log Level is set to ' + api.get_log_level())
        else:
            self.sprint('Fail to set Log Level')
        message = '\nPossible Log Levels, Please use following values to set desired log level. \n\n\tDEBUG:        Detailed information, typically of interest only when diagnosing problems.\n\tINFO:        Confirmation that things are working as expected.\n\tWARNING:    An indication that something unexpected happened, or indicative of some problem in the near future. \n\tERROR:        Due to a more serious problem, the software has not been able to perform some function.\n\tCRITICAL:    A serious error, indicating that the program itself may be unable to continue running.\n'
        self.sprint(message)


class ostream(InteractiveCommand):
    """ostream"""

    def handle_no_input(self, con_obj=None):
        self.sprint('Current ostream level is set to %s' % self.shell.ostream.get_lvl())
        message = '\nPossible ostream levels, Please use following values to set desired stdout level. \n\n\t0:Quite.\n\t1:Console.\n\t2:File. \n\t3:Console and File.\n'
        self.sprint(message)

    def handle_input(self, dict_handler, con_obj=None):
        lvl = None
        if dict_handler:
            lvl = next((item for item in [dict_handler.get('l'), dict_handler.get('lvl')] if item is not None), None)
            return self.shell.ostream.set_lvl(int(lvl))
        else:
            return False

    def handle_output(self, out_obj):
        if out_obj == True:
            self.sprint('Current ostream level is set to %s' % self.shell.ostream.get_lvl())
        else:
            self.sprint('Fail to set ostream Level')
            message = '\nPossible ostream levels, Please use following values to set desired ostream level. \n\n\t0:Quite.\n\t1:Console.\n\t2:File. \n\t3:Console and File.\n'
            self.sprint(message)


class chassis(InteractiveCommand):
    """chassis"""
    pass


class nodes(InteractiveCommand):
    """nodes"""
    pass


class switches(InteractiveCommand):
    """switches"""

    def handle_command(self, opts, args):
        no_args = len(args)
        change = False
        try:
            i = args.index('--ports')
            if i < no_args - 1:
                next_args = args[(i + 1)]
                if next_args.startswith('-'):
                    change = True
                else:
                    change = False
            else:
                change = True
        except ValueError:
            change = False

        if change:
            args = [w.replace('--ports', '--ports=') if w == '--ports' else w for w in args]
        return InteractiveCommand.handle_command(self, opts, args)


class fans(InteractiveCommand):
    """fans"""
    pass


class powersupplies(InteractiveCommand):
    """powersupplies"""
    pass


class fanmuxes(InteractiveCommand):
    """fanmuxes"""
    pass


class cmms(InteractiveCommand):
    """cmms"""
    pass


class scalablesystem(InteractiveCommand):
    """scalablesystem"""
    pass


class jobs(InteractiveCommand):
    """jobs"""

    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint('Jobs command Failed.')
        else:
            if out_obj == False:
                self.sprint('Jobs command Failed.')
            elif out_obj == True:
                self.sprint('Jobs command succeeded')


class discover(InteractiveCommand):
    """discover"""

    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint('Failed to start Discovery job for selected endpoint ')
        else:
            self.sprint('Discovery job started, jobId = ' + out_obj)


class manage(InteractiveCommand):
    """manage"""

    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint('Failed to start manage job for selected endpoint ')
        else:
            self.sprint('Manage job started, jobId = ' + out_obj)


class unmanage(InteractiveCommand):
    """unmanage"""

    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint('Failed to start unmanage job for selected endpoint ')
        else:
            self.sprint('Unmanage job started, jobId = ' + out_obj)


class lxcalog(InteractiveCommand):
    """lxcalog"""
    pass


class ffdc(InteractiveCommand):
    """ffdc"""

    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint('Failed to start ffdc job for selected endpoint ')
        else:
            self.sprint('FFDC job started, jobId = ' + out_obj)


class users(InteractiveCommand):
    """users"""
    pass


class updatepolicy(InteractiveCommand):
    """updatepolicy"""
    pass


class updaterepo(InteractiveCommand):
    """updaterepo"""
    pass


class updatecomp(InteractiveCommand):
    """updatecomp"""
    pass


class configtargets(InteractiveCommand):
    """configtargets"""
    pass


class configpatterns(InteractiveCommand):
    """configpatterns"""
    pass


class configprofiles(InteractiveCommand):
    """configprofiles"""
    pass


class manifests(InteractiveCommand):
    """manifests"""
    pass


class tasks(InteractiveCommand):
    """tasks"""
    pass


class resourcegroups(InteractiveCommand):
    """resourcegroups"""
    pass


class osimages(InteractiveCommand):
    """osimages"""
    pass


class managementserver(InteractiveCommand):
    """managementserver"""
    pass


class rules(InteractiveCommand):
    """rules"""
    pass


class compositeResults(InteractiveCommand):
    """compositeResults"""
    pass


class storedcredentials(InteractiveCommand):
    """storedcredentials"""
    pass