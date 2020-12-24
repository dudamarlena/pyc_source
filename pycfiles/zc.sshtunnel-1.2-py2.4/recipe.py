# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zc/sshtunnel/recipe.py
# Compiled at: 2007-03-28 20:00:10
"""`zc.buildout` recipe to create and manage an SSH tunnel using an rc script.

"""
__docformat__ = 'reStructuredText'
import os

class Recipe(object):
    __module__ = __name__

    def __init__(self, buildout, name, options):
        self.name = name
        self.options = options
        self.via = options['via']
        self.specification = options['specification']
        parts = self.specification.split(':')
        wait_port = int(parts[(-3)])
        self.wait_port = str(wait_port)
        python = options.get('python', 'buildout')
        self.executable = buildout[python]['executable']
        self.script = os.path.join(buildout['buildout']['bin-directory'], name)
        self.pidfile = os.path.join(buildout['buildout']['parts-directory'], name + '.pid')
        options['executable'] = self.executable
        options['pidfile'] = self.pidfile
        options['run-script'] = self.script

    def install(self):
        d = {'name': self.name, 'pid_file': self.pidfile, 'python': self.executable, 'specification': self.specification, 'via': self.via, 'wait_port': self.wait_port}
        text = tunnel_script_template % d
        f = open(self.script, 'w')
        f.write(text)
        f.close()
        os.chmod(self.script, int('0770', 8))
        return [self.script]

    def update(self):
        pass


tunnel_script_template = '#!%(python)s\n\nimport os, sys, signal, socket, time, errno\n\npid_file = "%(pid_file)s"\nspecification = "%(specification)s"\nvia = "%(via)s"\nwait_port = %(wait_port)s\nname = "%(name)s"\n\ndef wait(port):\n    addr = \'localhost\', port\n    for i in range(120):\n        time.sleep(0.25)\n        try:\n            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n            s.connect(addr)\n            s.close()\n            break\n        except socket.error, e:\n            if e[0] not in (errno.ECONNREFUSED, errno.ECONNRESET):\n                raise\n            s.close()\n    else:\n        raise\n\ndef main(args=None):\n    if args is None:\n        args = sys.argv[1:]\n\n    [verb] = args\n\n    if verb == \'start\':\n        if os.path.exists(pid_file):\n            print "Pid file %%s already exists" %% pid_file\n            return\n\n        pid = os.fork()\n        if pid == 0:\n            # redirect output to /dev/null.  This will\n            # cause nohup to be unannoying\n            os.dup2(os.open(\'/dev/null\', os.O_WRONLY), 1)\n            os.dup2(os.open(\'/dev/null\', os.O_WRONLY), 2)\n            pid = os.spawnlp(os.P_NOWAIT, \'nohup\', \'nohup\',\n                             \'ssh\', \'-TnaxqNL\'+specification,  via)\n            open(pid_file, \'w\').write("%%s\\n" %% pid)\n        else:\n            wait(wait_port)\n            print name, \'started\'\n    elif verb == \'status\':\n        if os.path.exists(pid_file):\n            pid = int(open(pid_file).read().strip())\n            try:\n                os.kill(pid, 0)\n            except OSError, v:\n                if v.errno == errno.ESRCH:\n                    print name, \'not running\'\n                    # Unlink the pid_file if we can, to avoid having\n                    # process numbers cycle around and accidentally\n                    # recognizing some other process mistakenly.\n                    try:\n                        os.unlink(pid_file)\n                    except OSError:\n                        pass\n                else:\n                    print v\n            else:\n                print name, \'running\'\n        else:\n            print "Pid file %%s doesn\'t exist" %% pid_file\n    elif verb == \'stop\':\n        if os.path.exists(pid_file):\n            pid = int(open(pid_file).read().strip())\n            try:\n                os.kill(pid, signal.SIGINT)\n            except OSError, v:\n                print v\n            os.remove(pid_file)\n            print name, \'stopped\'\n        else:\n            print "Pid file %%s doesn\'t exist" %% pid_file\n    elif verb == \'restart\':\n        main([\'stop\'])\n        main([\'start\'])\n        return\n    else:\n        raise ValueError("Unknown verb", verb)\n\nif __name__ == \'__main__\':\n    main()\n'