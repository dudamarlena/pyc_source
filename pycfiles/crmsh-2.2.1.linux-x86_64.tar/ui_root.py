# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/ui_root.py
# Compiled at: 2016-05-10 02:02:08
from . import command
from . import cmd_status
from . import ui_cib
from . import ui_cibstatus
from . import ui_cluster
from . import ui_configure
from . import ui_corosync
from . import ui_history
from . import ui_maintenance
from . import ui_node
from . import ui_options
from . import ui_ra
from . import ui_report
from . import ui_resource
from . import ui_script
from . import ui_site

class Root(command.UI):
    """
    Root of the UI hierarchy.
    """
    name = 'root'

    @command.level(ui_cib.CibShadow)
    @command.help('manage shadow CIBs\nA shadow CIB is a regular cluster configuration which is kept in\na file. The CRM and the CRM tools may manage a shadow CIB in the\nsame way as the live CIB (i.e. the current cluster configuration).\nA shadow CIB may be applied to the cluster in one step.\n')
    def do_cib(self):
        pass

    @command.level(ui_cibstatus.CibStatusUI)
    @command.help('CIB status management and editing\nEnter edit and manage the CIB status section level.\n')
    def do_cibstatus(self):
        pass

    @command.level(ui_cluster.Cluster)
    @command.help('Cluster setup and management\nCommands at this level enable low-level cluster configuration\nmanagement with HA awareness.\n')
    def do_cluster(self):
        pass

    @command.level(ui_configure.CibConfig)
    @command.help('CRM cluster configuration\nThe configuration level.\n\nNote that you can change the working CIB at the cib level. It is\nadvisable to configure shadow CIBs and then commit them to the\ncluster.\n')
    def do_configure(self):
        pass

    @command.level(ui_corosync.Corosync)
    @command.help('Corosync configuration management\nCorosync is the underlying messaging layer for most HA clusters.\nThis level provides commands for editing and managing the corosync\nconfiguration.\n')
    def do_corosync(self):
        pass

    @command.level(ui_history.History)
    @command.help("CRM cluster history\nThe history level.\n\nExamine Pacemaker's history: node and resource events, logs.\n")
    def do_history(self):
        pass

    @command.level(ui_maintenance.Maintenance)
    @command.help('maintenance\nCommands that should only be executed while in\nmaintenance mode.\n')
    def do_maintenance(self):
        pass

    @command.level(ui_node.NodeMgmt)
    @command.help('nodes management\nA few node related tasks such as node standby are implemented\nhere.\n')
    def do_node(self):
        pass

    @command.level(ui_options.CliOptions)
    @command.help('user preferences\nSeveral user preferences are available. Note that it is possible\nto save the preferences to a startup file.\n')
    def do_options(self):
        pass

    @command.level(ui_ra.RA)
    @command.help('resource agents information center\nThis level contains commands which show various information about\nthe installed resource agents. It is available both at the top\nlevel and at the `configure` level.\n')
    def do_ra(self):
        pass

    @command.help('Utility to collect logs and other information\n`report` is a utility to collect all information (logs,\nconfiguration files, system information, etc) relevant to\ncrmsh over the given period of time.\n')
    def do_report(self, context, *args):
        rc = ui_report.create_report(context, args)
        return rc == 0

    @command.level(ui_resource.RscMgmt)
    @command.help('resources management\nEverything related to resources management is available at this\nlevel. Most commands are implemented using the crm_resource(8)\nprogram.\n')
    def do_resource(self):
        pass

    @command.level(ui_script.Script)
    @command.help('Cluster scripts\nCluster scripts can perform cluster-wide configuration,\nvalidation and management. See the `list` command for\nan overview of available scripts.\n')
    def do_script(self):
        pass

    @command.level(ui_site.Site)
    @command.help('Geo-cluster support\nThe site level.\n\nGeo-cluster related management.\n')
    def do_site(self):
        pass

    @command.help('show cluster status\nShow cluster status. The status is displayed by `crm_mon`. Supply\nadditional arguments for more information or different format.\nSee `crm_mon(8)` for more details.\n\nUsage:\n...............\nstatus [<option> ...]\n\noption :: bynode | inactive | ops | timing | failcounts\n...............\n')
    def do_status(self, context, *args):
        return cmd_status.cmd_status(args)

    @command.help('Verify cluster state\nPerforms basic checks for the cluster configuration and\ncurrent status, reporting potential issues.\n\nUsage:\n.................\nverify [scores]\n.................\n')
    def do_verify(self, context, *args):
        return cmd_status.cmd_verify(args)


Root.init_ui()