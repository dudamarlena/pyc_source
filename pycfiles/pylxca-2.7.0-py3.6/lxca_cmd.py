# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylxca/pylxca_cmd/lxca_cmd.py
# Compiled at: 2020-03-12 01:38:00
# Size of source mod 2**32: 29901 bytes
"""
@since: 15 Sep 2015
@author: Prashant Bhosale <pbhosale@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo 
@summary: This module provides command class implementation for PyLXCA 
"""
import sys, getopt, logging, traceback
from getpass import getpass
import json, argparse, pylxca.pylxca_api
from pylxca.pylxca_api.lxca_rest import HTTPError
from pylxca.pylxca_api.lxca_connection import ConnectionError
from pylxca.pylxca_cmd.lxca_icommands import InteractiveCommand
logger = logging.getLogger(__name__)

class connect(InteractiveCommand):
    __doc__ = '\n    Connects to the LXCA Interface\n\n    USAGE:\n        connect -h | --help\n        connect -l <URL> -u <USER> [--noverify]\n    \n    OPTIONS:\n        -h        This option displays command usage information\n        -l, --url    URL of LXCA\n        -u, --user    Username to authenticate\n        --noverify    Do not verify the server certificate for https URLs\n\n    '

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
    __doc__ = '\n    Diconnects from LXCA Interface \n\n    USAGE:\n        disconnect -h | --help\n        disconnect\n    '

    def handle_no_input(self, con_obj=None):
        api = pylxca.pylxca_api.lxca_api()
        if api.disconnect() == True:
            self.sprint('Connection with LXCA closed successfully ')
        else:
            self.sprint('Failed to close connection with LXCA ')


class log(InteractiveCommand):
    __doc__ = '\n    Retrieve and configure logging of LXCA Python tool\n    \n    USAGE:\n        log -h | --help\n        log [-l <level>]\n\n    OPTIONS:\n        -l, --lvl    Logging level\n      \n    '

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
    __doc__ = '\n    Configure output stream or verbose level of command shell \n    \n    USAGE:\n        ostream -h | --help\n        ostream [-l <level>]\n    \n    OPTIONS:\n        -l, --lvl    verbose level\n\n    '

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
    __doc__ = '\n    Get Chassis List and Chassis Information\n    \n    USAGE:\n        chassis -h\n        chassis [-u <chassis UUID>] [-v <view filter name>]\n    \n    OPTIONS:\n        -h        This option displays command usage information\n        -u, --uuid    chassis uuid\n        -s, --status    chassis manage status (managed/unmanaged)\n        -v, --view    view filter name\n\n    '


class nodes(InteractiveCommand):
    __doc__ = '\n    Retrieve nodes List and nodes Information\n    \n    USAGE:\n        nodes -h\n        nodes [-u <node UUID>] [-s <managed/unmanaged>] [-c <chassis UUID>] [-v <view filter name>]\n    \n    OPTIONS:\n        -h        This option displays command usage information\n        -u, --uuid    node uuid\n        -s, --status    nodes manage status (managed/unmanaged)\n        -c, --chassis    chassis uuid\n        -v, --view    view filter name\n        -x, --metrics   flag to fetch metrics\n\n    '


class switches(InteractiveCommand):
    __doc__ = '\n    Retrieve switches List and switches Information\n    \n    USAGE:\n        switches -h\n        switches [-u <switch UUID>] [-c <chassis UUID>] [-v <view filter name>]\n        switches  [-u <switch_UUID>] [--ports <port_name>] [--action <action>]\n    \n    OPTIONS:\n        -h            This option displays command usage information\n        -u, --uuid    switch uuid\n        -c, --chassis    chassis uuid\n        --ports        portnames if port is empty lists ports\n        --action       enable/disable ports\n        -v, --view    view filter name\n\n    '

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
    __doc__ = '\n    Retrieve fan List and fans Information\n    \n    USAGE:\n        fans -h\n        fans [-u <fan UUID>] [-c <chassis UUID>] [-v <view filter name>]\n    \n    OPTIONS:\n        -h        This option displays command usage information\n        -u, --uuid    fan uuid\n        -c, --chassis    chassis uuid\n        -v, --view    view filter name\n\n    '


class powersupplies(InteractiveCommand):
    __doc__ = '\n    Retrieve Power Supply Information\n    \n    USAGE:\n        powersupplies -h\n        powersupplies [-u <power supply UUID>] [-c <chassis UUID>] [-v <view filter name>]\n    \n    OPTIONS:\n        -h            This option displays command usage information\n        -u, --uuid    power supply uuid\n        -c, --chassis    chassis uuid\n        -v, --view    view filter name\n\n    '


class fanmuxes(InteractiveCommand):
    __doc__ = '\n    Retrieve fan Mux Information\n\n    USAGE:\n        fanmuxes -h\n        fanmuxes [-u <fan mux UUID>] [-c <chassis UUID>] [-v <view filter name>]\n    \n    OPTIONS:\n        -h        This option displays command usage information\n        -u, --uuid    fan mux uuid\n        -c, --chassis    chassis uuid\n        -v, --view    view filter name\n\n    '


class cmms(InteractiveCommand):
    __doc__ = '\n    Get CMM  Information\n    \n    USAGE:\n        cmms -h\n        cmms [-u <cmm UUID>] [-c <chassis UUID>] [-v <view filter name>]\n    \n    OPTIONS:\n        -h        This option displays command usage information\n        -u, --uuid    cmm uuid\n        -c, --chassis    chassis uuid\n        -v, --view    view filter name\n\n    '


class scalablesystem(InteractiveCommand):
    __doc__ = '\n    Retrieve Scalable Complex System  Information\n    \n    USAGE:\n        scalablesystem -h\n        scalablesystem [-i <scalablesystem id>] [-t <scalablesystem type>] [-s <status>] [-v <view filter name>]\n    \n    OPTIONS:\n        -h        This option displays command usage information\n        -i, --id    scalable complex id\n        -t, --type    type (flex/rackserver)\n        -s, --status    scalable system manage status (managed/unmanaged)\n        -v, --view    view filter name\n\n'


class jobs(InteractiveCommand):
    __doc__ = '\n    Retrieve and Manage information about jobs.\n\n    USAGE:\n        jobs -h | --help\n        jobs [-i <job id>][-u <uuid of endpoint>][-s <jobs state>]\n        jobs [-c <cancels the job with specified id>]\n        jobs [-d <delete the job with specified id>]\n    \n    OPTIONS:\n        -i, --id=    job id\n        -u, --uuid=    uuid of endpoint for which jobs should be retrieved\n        -s, --state=    job state to retrieve jobs in specified state.\n                The state can be one of the following\n                Pending\n                Running\n                Complete\n                Cancelled\n                Running_With_Errors\n                Cancelled_With_Errors\n                Stopped_With_Error\n                Interrupted\n        -c, --cancel=    cancel job of specified id\n        -d, --delete=    delete job of specified id\n\n    '

    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint('Jobs command Failed.')
        else:
            if out_obj == False:
                self.sprint('Jobs command Failed.')
            elif out_obj == True:
                self.sprint('Jobs command succeeded')


class discover(InteractiveCommand):
    __doc__ = '\n    Retrieve a list of devices discovered by SLP discovery.\n    \n    USAGE:\n        discover [-i <IP Address of endpoint>][-j <job ID>]\n    \n    OPTIONS:\n        -i, --ip       One or more IP addresses for each endpoint to be discovered.\n        -j, --job      Job ID of discover request\n    \n\n    '

    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint('Failed to start Discovery job for selected endpoint ')
        else:
            self.sprint('Discovery job started, jobId = ' + out_obj)


class manage(InteractiveCommand):
    __doc__ = '\n    Manage the endpoint.\n    \n    USAGE:\n        manage  -h | --help\n        manage  -i <IP Address of endpoint> -u <user ID to access the endpoint>\n                -p <current password to access the endpoint> [-r <recovery password for the endpoint>]\n                [-f <Force Manage (True/False)>]\n        manage  -i <IP Address of endpoint> -s <stored credential ID> [-r <recovery password for the endpoint>]\n                [-f <Force Manage (True/False)>]\n\n        manage  -j <job ID> [-v <view filter name>]\n\n    OPTIONS:\n        -i, --ip        One or more IP addresses for each endpoint to be managed.\n        -u, --user      user ID to access the endpoint\n        -p, --pw        The current password to access the endpoint.\n        -r, --rpw       The recovery password to be used for the endpoint.\n        -j, --job       Job ID of existing manage request\n        -f, --force     Force Manage Boolean flag\n        -s  --storedcredential_id  stored credential id\n        -v, --view      view filter name\n    '

    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint('Failed to start manage job for selected endpoint ')
        else:
            self.sprint('Manage job started, jobId = ' + out_obj)


class unmanage(InteractiveCommand):
    __doc__ = "\n    Unmanage the endpoint\n\n    USAGE:\n        unmanage -h | --help\n        unmanage -i <endpoint information> [--force]\n        unmanage -j <job ID> [-v <view filter name>]\n    \n    OPTIONS:\n        -e, --ep    one or more endpoints to be unmanaged.\n                This is comma separated list of multiple endpoints, each endpoint should\n                contain endpoint information separated by semicolon.\n                endpoint's IP Address(multiple addresses should be separated by #), UUID of the endpoint and\n                Type of endpoint to be unmanaged ,This can be one of the following values:\n                    Chassis\n                    ThinkServer\n                    Storage\n                    Rackswitch\n                    Rack-Tower\n        -f, --force     Indicates whether to force the unmanagement of an endpoint (True/False)\n        -j, --job       Job ID of unmanage request\n        -v, --view      View filter name\n\n    "

    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint('Failed to start unmanage job for selected endpoint ')
        else:
            self.sprint('Unmanage job started, jobId = ' + out_obj)


class lxcalog(InteractiveCommand):
    __doc__ = '\n    Retrieve and Manage information about LXCA Event log.\n\n    USAGE:\n        lxcalog [-f < events that apply to the specified filters >]\n\n    '


class ffdc(InteractiveCommand):
    __doc__ = '\n    Retrieve and Manage information about ffdc\n\n    USAGE:\n        ffdc -u <UUID of the target endpoint>\n    \n    OPTIONS:\n        -u, --uuid    <UUID of the target endpoint>\n    '

    def handle_output(self, out_obj):
        if out_obj == None:
            self.sprint('Failed to start ffdc job for selected endpoint ')
        else:
            self.sprint('FFDC job started, jobId = ' + out_obj)


class users(InteractiveCommand):
    __doc__ = '\n    Retrieve and Manage information about users.\n    \n    USAGE:\n        users [-i <unique ID of the user to be retrieved>][-v <view filter name>]\n\n    OPTIONS:\n        -i, --id    unique ID of the user to be retrieved\n        -v, --view    View filter name\n\n    '


class updatepolicy(InteractiveCommand):
    __doc__ = '\n    Retrieve and Manage information about jobs.\n    \n    USAGE:\n        updatepolicy [-v <view filter name>]\n        updatepolicy -p <Compliance policy to be assigned to device> -u <UUID of Device> -t <Device Type>\n        updatepolicy -j <Job Id of assign policy operation>\n        updatepolicy -i <Information type of compliance policy to be retreived>\n    \n    OPTIONS:\n        -p, --policy    Name of the compliance-policy to be assigned to device\n        -u, --UUID      UUID of the device to which you want to assign the compliance policy\n        -t, --type      Type = The device type. This can be one of the following values.\n                            CMM - Chassis Management Module\n                            IOSwitch - Flex switch\n                            RACKSWITCH - RackSwitch switch\n                            STORAGE - Lenovo Storage system\n                            SERVER - Compute node or rack server\n\n        -j, --job       Job ID of assign compliance policy operation\n\n        -i, --info      Specifies the type of information to return. This can be one of the following values:\n                            FIRMWARE- Returns information about firmware that is applicable to each managed endpoint\n                            RESULTS- Returns persisted compare result for servers to which a compliance policy is assigned\n\n        -v, --view      View filter name\n\n    '


class updaterepo(InteractiveCommand):
    __doc__ = '\n    Retrieve and Manage information about jobs.\n\n    USAGE:\n        updaterepo -k <Key to return the specified type of update> [-v <view filter name>]\n        updaterepo -a <action to take> [-v <view filter name>]\n    OPTIONS:\n        -k, --key       Returns the specified type of update. This can be one of the following values.\n                        supportedMts - Returns a list of supported machine types\n                        size - Returns the repository size\n                        lastRefreshed - Returns the timestamp of the last repository refresh\n                        importDir - Returns the import directory for the repository.\n                        publicKeys - Returns the supported signed keys\n                        updates - Returns information about all firmware updates\n                        updatesByMt - Returns information about firmware updates for the specified machine type\n                        updatesByMtByComp - Returns the update component names for the specified machine type\n        -a  --action    The action to take. This can be one of the following values.\n                        read - Reloads the repository files. The clears the update information in cache and reads the update file again from the repository.\n                        refresh - Retrieves information about the latest available firmware updates from the Lenovo Support website,\n                            and stores the information to the firmware-updates repository.\n                        acquire - Downloads the specified firmware updates from Lenovo Support website, and stores the updates to the firmware-updates repository.\n                        delete - Deletes the specified firmware updates from the firmware-updates repository.\n                        export.not supported\n\n        -m  --mt        comma separated machine types\n        -s  --scope     scope of operation [ all/latest] for refresh and [ payloads ] for acquire\n        -f  --fixids    comma separated fixids\n        -t  --type      filetype [ all/payloads ]\n\n        -v, --view    View filter name\n\n    '


class updatecomp(InteractiveCommand):
    __doc__ = '\n    Update the firmware of specified component.\n        \n    USAGE:\n        updatecomp [-q <The data to return>] [-v <view filter name>]\n        updatecomp  [-m <activate mode>] [-a <action to take>] [-c <information of cmms>] [-w <information of switches>] [-s <information of servers>] [-t <information of storages>]\n        updatecomp  -a power [-c <cmms UUID and desired state>] [-w <switches UUID and desired state>]  [-s <servers UUID and desired state>]\n    \n    OPTIONS:\n        -q, --query     The data to return. This can be one of the following values.\n                            components - Returns a list of endpoints and components that can be updated.\n                            status - Returns the status and progress of firmware updates. This is the default value\n        -m, --mode      Indicates when to activate the update. This can be one of the following values.\n                            immediate - Uses Immediate Activation mode when applying firmware updates to the selected endpoints.\n                            delayed - Uses Delayed Activation mode when applying firmware updates to the selected endpoints.\n                            prioritized - Firmware updates on the baseboard management controller are activated immediately\n\n        -a, --action    The action to take. This can be one of the following values.\n                            apply - Applies the associated firmware to the submitted components.\n                            power - Perform power action on selected endpoint.\n                            cancelApply - Cancels the firmware update request to the selected components.\n        -c, --cmm       cmms information\n        -w, --switch    switch information\n        -s, --server    servers information\n        -t, --storage   storages information\n    \n            For action = apply/cancelApply, Device information should contain following data separated by comma\n                UUID - UUID of the device\n                Fixid - Firmware-update ID of the target package to be applied to the component. If not provided assigned policy would be used.\n                Component - Component name\n\n            For action = power, Device information should contain following data separated by comma\n                UUID - UUID of the device\n                powerState - One of the power state values. Possible values per device type are\n                    Server: powerOn, powerOff, powerCycleSoft, powerCycleSoftGraceful, powerOffHardGraceful\n                    Switch: powerOn, powerOff, powerCycleSoft\n                    CMM: reset\n                    Storage:powerOff,powerCycleSoft\n\n        -v, --view      View filter name\n\n    '


class configtargets(InteractiveCommand):
    __doc__ = '\n    Retrieve and Manage information of configuration targes.\n    \n    USAGE:\n        configtargets [-i <ID of specific profile or pattern>] [-v <view filter name>]\n    \n    OPTIONS:\n        -i, --id    The unique ID that was assigned when the server pattern was created\n        -v, --view    View filter name\n    \n    \n    '


class configpatterns(InteractiveCommand):
    __doc__ = '\n    Retrieve and Manage information about config patterns.\n    \n    USAGE:\n        configpatterns [-i <ID of specific pattern>] [-r <when to activate the configurations>] [-e <Comma separated list of one or more UUIDs for the target servers>] [-t <type of the target server>] [-s True] [-v <view filter name>]\n    \n    OPTIONS:\n        -i, --id    The unique ID that was assigned when the server pattern was created\n        -n, --name  Name of pattern\n        -e, --endpoint    Comma separated list of one or more UUIDs for the target servers,If a target is an empty bay,\n                specify the location ID; otherwise, specify the server UUID\n        -r, --restart    When to activate the configurations. This can be one of the following values:\n                defer - Activate IMM settings but do not restart the server.\n                immediate - Activate all settings and restart the server immediately.\n                pending - Manually activate the server profile and restart the server.\n        -t, --type    Type of the server, It can be one of the following\n                Flex  - for empty bay having endpoint other than UUID\n                Node\n                Rack\n                Tower\n        -s, --status  return config status\n        -v, --view    View filter name\n\n    '


class configprofiles(InteractiveCommand):
    __doc__ = '\n    Retrieve and Manage information of config profiles.\n\n    USAGE:\n        configprofiles [-i <ID of specific profile>] [-v <view filter name>]\n        configprofiles -i <ID of specific profile> -n <New profile name>\n        configprofiles -i <ID of specific profile> -e <UUID or location ID>  -r <restart option> [-v <view filter name>]\n        configprofiles -i <ID of specific profile>  -d <boolean>   [-v <view filter name>]\n        configprofiles -i <ID of specific profile>  -u <boolean> -p <boolean> --resetimm <boolean> -f <boolean> [-v <view filter name>]\n\n    OPTIONS:\n        -i, --id    The unique ID that was assigned when the server pattern was created\n               id          The unique ID that was assigned when the server profile was created\n        -n, --name        profile name\n        -e,  --endpoint    endpoint  UUID of the server or location id for flex system\n        -r,  --restart     restart server to activate profile ( immediate / defer )\n        -d,  --delete      True for delete id\n        -u   --unassign    unassign specified id\n        -p   --powerdown   powerdown server [true/false]\n             --resetimm    reset IMM [true/false]\n        -f   --force       force profile deactivation [true/false]\n        -v, --view    View filter name\n\n    '


class manifests(InteractiveCommand):
    __doc__ = '\n    Send solution manifest to and retreive manifests from Lenovo XClarity Administrator.\n    '


class tasks(InteractiveCommand):
    __doc__ = '\n    Retrieve tasks List and tasks Information\n\n    USAGE:\n        tasks -h\n        tasks [-u <JOB UUID>]  [-v <view filter name>]\n\n    OPTIONS:\n    -h            This option displays command usage information\n        -u, --uuid    Job uuids\n        -v, --view    view filter name\n\n    '


class resourcegroups(InteractiveCommand):
    __doc__ = '\n    create Group of Resources\n    '


class osimages(InteractiveCommand):
    __doc__ = '\n    OSImages/Deployment on LXCA\n    '


class managementserver(InteractiveCommand):
    __doc__ = '\n    managementserver update on LXCA\n    '


class rules(InteractiveCommand):
    __doc__ = '\n    complaince rules get and update on LXCA\n    '


class compositeResults(InteractiveCommand):
    __doc__ = '\n    complaince compositeresult get and update on LXCA\n    '


class storedcredentials(InteractiveCommand):
    __doc__ = '\n        storedcredentials get and update on LXCA\n\n    USAGE:\n        storedcredentials -h\n        storedcredentials [-u <admin>] [-p <password>] [-d <description>] [-v <view filter name>]\n        storedcredentials [-u <Stored Credential Id>] [-u <admin>] [-p <password>] [-d <description>] [-v <view filter name>]\n\n    OPTIONS:\n        -h        This option displays command usage information\n        -i  --id      stored credential id\n        -u, --user_name     user name\n        -p, --password    password\n        -d, --description detail about user\n            --delete_id    credential id to be deleted\n        -v, --view    view filter name\n\n    '