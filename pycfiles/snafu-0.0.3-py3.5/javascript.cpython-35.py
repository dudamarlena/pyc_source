# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/javascript.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 1473 bytes
import subprocess, time, os.path

def execute(func, funcargs, envvars, sourceinfos):
    sourcemodule = sourceinfos.source[:-3]
    if '.' in func:
        func = func.split('.')[1]
    sourcemodulemod = sourcemodule + '.js.export'
    if not os.path.isfile(sourcemodulemod):
        code = open(sourcemodule + '.js').read()
        if 'exports' not in code:
            f = open(sourcemodulemod, 'w')
            f.write(code)
            f.write('\n')
            f.write('function mainwrapper(input){console.log(main(input));}\n')
            f.write('exports.main = mainwrapper;\n')
            sourcemodule = sourcemodulemod
    else:
        sourcemodule = sourcemodulemod
    if '{' not in funcargs[0]:
        funcargs[0] = '"{"body": {"message": "%s"}}"' % funcargs[0]
    if sourcemodulemod != sourcemodule:
        cmd = 'nodejs -e \'require("./%s").%s(%s, {"status": function(x){return {"send": function(x){console.log("RET:" + x)}}}})\'' % (sourcemodule, func, funcargs[0])
    else:
        cmd = 'nodejs -e \'require("./%s").%s(%s)\'' % (sourcemodule, func, funcargs[0])
    stime = time.time()
    p = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    out = p.stdout.decode('utf-8')
    dtime = time.time() - stime
    success = False
    res = []
    for line in out.split('\n'):
        if sourcemodulemod != sourcemodule:
            if line.startswith('RET:'):
                success = True
                res = line[4:]
                break
        else:
            success = True
            res = line
            break

    return (
     dtime, success, res)