# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lambadalib/lambada.py
# Compiled at: 2017-12-20 14:11:12
# Size of source mod 2**32: 18963 bytes
import inspect, ast, tempfile, zipfile, subprocess, time, os
from lambadalib import codegen
from lambadalib import functionproxy

def printlambada(*s):
    red = '\x1b[1;31m'
    reset = '\x1b[0;0m'
    s += (reset,)
    print(red, '»» Lambada:', *s)


def lambadamonad(s):
    green = '\x1b[1;32m'
    reset = '\x1b[0;0m'
    print(green, '»» Lambada Monad:', s, reset)


class CloudFunctionConfiguration:

    def __init__(self):
        self.enabled = False
        self.memory = None
        self.duration = None
        self.region = None

    def __str__(self):
        return 'CFC({}|{}|{})'.format(self.memory, self.duration, self.region)

    def __format__(self, s):
        return self.__str__()


class FuncListener(ast.NodeVisitor):

    def __init__(self, functionname, functions, annotations):
        ast.NodeVisitor.__init__(self)
        self.functionname = functionname
        self.functions = functions
        self.annotations = annotations
        self.currentfunction = None
        self.tainted = []
        self.filtered = []
        self.args = {}
        self.bodies = {}
        self.deps = {}
        self.features = {}
        self.classes = {}
        self.cfcs = {}

    def checkdep(self, dep):
        if dep in self.functions and dep not in self.deps.get(self.currentfunction, []):
            printlambada('AST: dependency {:s} -> {:s}'.format(self.currentfunction, dep))
            self.deps.setdefault(self.currentfunction, []).append(dep)

    def visit_ClassDef(self, node):
        self.classes[node.name] = node

    def visit_Call(self, node):
        if 'id' in dir(node.func):
            self.checkdep(node.func.id)
        for arg in node.args:
            if isinstance(arg, ast.Call):
                if 'id' not in dir(arg.func):
                    pass
                else:
                    self.checkdep(arg.func.id)
                    if arg.func.id == 'map':
                        for maparg in arg.args:
                            if isinstance(maparg, ast.Name):
                                self.checkdep(maparg.id)

    def visit_Return(self, node):
        d = ast.Dict([ast.Str('ret'), ast.Str('log')], [node.value, ast.Name('__lambdalog', ast.Load())])
        node.value = d

    def visit_FunctionDef(self, node):
        self.currentfunction = node.name
        if self.annotations:
            if node.name == 'cloudfunction':
                self.generic_visit(node)
            cfc = CloudFunctionConfiguration()
            for name in node.decorator_list:
                if 'id' in dir(name):
                    if name.id == 'cloudfunction':
                        cfc.enabled = True
                    else:
                        if name.func.id == 'cloudfunction':
                            cfc.enabled = True
                            for keyword in name.keywords:
                                if keyword.arg == 'memory':
                                    cfc.memory = keyword.value.n
                                else:
                                    if keyword.arg == 'region':
                                        cfc.region = keyword.value.s
                                    elif keyword.arg == 'duration':
                                        cfc.duration = keyword.value.n

            if cfc.enabled:
                printlambada('AST: annotation {:s} @ {:s}'.format(cfc, node.name))
                self.cfcs[node.name] = cfc
        else:
            printlambada('AST: no annotation @ {:s}'.format(node.name))
            self.generic_visit(node)
            self.filtered.append(node.name)
        if self.functionname == None or node.name == self.functionname:
            for arg in node.args.args:
                pass

            for linekind in node.body:
                if isinstance(linekind, ast.Expr):
                    if not 'func' not in dir(linekind.value):
                        if 'id' not in dir(linekind.value.func):
                            pass
                        else:
                            if linekind.value.func.id in ('input', ):
                                self.tainted.append(node.name)
                            elif linekind.value.func.id in ('print', ):
                                self.features.setdefault(node.name, []).append('print')

        if node.name not in self.tainted:
            for arg in node.args.args:
                self.args.setdefault(node.name, []).append(arg.arg)

            newbody = []
            for linekind in node.body:
                if isinstance(linekind, ast.Return):
                    a = ast.Assign([ast.Name('ret', ast.Store())], linekind.value)
                    d = ast.Dict([ast.Str('ret'), ast.Str('log')], [ast.Name('ret', ast.Load()), ast.Name('__lambdalog', ast.Load())])
                    b = ast.Assign([ast.Name('ret', ast.Store())], d)
                    r = ast.Return(ast.Name('ret', ast.Load()))
                    g = ast.Global(['__lambdalog'])
                    z = ast.Assign([ast.Name('__lambdalog', ast.Store())], ast.Str(''))
                    newbody = [
                     g] + newbody + [a, b, z, r]
                else:
                    newbody.append(linekind)

            self.bodies[node.name] = newbody
        self.generic_visit(node)


def analyse(functionname, functions, module, annotations):
    if not module:
        modulename = inspect.stack()[(-1)][1]
        printlambada('targeting', modulename, '...')
    else:
        modulename = module
    modulestring = open(modulename).read()
    tree = ast.parse(modulestring, modulename)
    fl = FuncListener(functionname, functions, annotations)
    fl.visit(tree)
    for function in functions:
        for dep in fl.deps.get(function, []):
            if dep in fl.tainted:
                printlambada('AST: dependency {:s} -> {:s} leads to tainting'.format(function, dep))
                fl.tainted.append(function)

    for function in functions:
        for dep in fl.deps.get(function, []):
            if dep in fl.filtered:
                taint = True
                if taint:
                    fl.tainted.append(dep)

    return (
     fl.tainted, fl.args, fl.bodies, fl.deps, fl.features, fl.classes, fl.cfcs)


def awstool(endpoint):
    if endpoint:
        return 'aws --endpoint-url {:s}'.format(endpoint)
    else:
        return 'aws'


template = '\ndef FUNCNAME_remote(event, context):\n\tUNPACKPARAMETERS\n\tFUNCTIONIMPLEMENTATION\n\ndef FUNCNAME_stub(jsoninput):\n\tevent = json.loads(jsoninput)\n\tret = FUNCNAME_remote(event, None)\n\treturn json.dumps(ret)\n\ndef FUNCNAME(PARAMETERSHEAD):\n\tlocal = LOCAL\n\tjsoninput = json.dumps(PACKEDPARAMETERS)\n\tif local:\n\t\tjsonoutput = FUNCNAME_stub(jsoninput)\n\telse:\n\t\tfunctionname = "FUNCNAME_lambda"\n\t\truncode = [AWSTOOL, "lambda", "invoke", "--function-name", functionname, "--payload", jsoninput, "_lambada.log"]\n\t\tproc = subprocess.Popen(runcode, stdout=subprocess.PIPE)\n\t\tstdoutresults = proc.communicate()[0].decode("utf-8")\n\t\tjsonoutput = open("_lambada.log").read()\n\t\tproc = subprocess.Popen(["rm", "_lambada.log"])\n\t\tif "errorMessage" in jsonoutput:\n\t\t\traise Exception("Lambda Remote Issue: {:s}; runcode: {:s}".format(jsonoutput, " ".join(runcode)))\n\toutput = json.loads(jsonoutput)\n\tif "log" in output:\n\t\tif local:\n\t\t\tif output["log"]:\n\t\t\t\tprint(output["log"])\n\t\telse:\n\t\t\tlambada.lambadamonad(output["log"])\n\treturn output["ret"]\n'
proxytemplate = '\ndef FUNCNAME(PARAMETERSHEAD):\n\tmsg = PACKEDPARAMETERS\n\tfullresponse = lambda_client.invoke(FunctionName="FUNCNAME_lambda", Payload=json.dumps(msg))\n\t#response = json.loads(fullresponse["Payload"].read())\n\tresponse = json.loads(fullresponse["Payload"].read().decode("utf-8"))\n\treturn response["ret"]\n'
proxytemplate_monadic = '\ndef FUNCNAME(PARAMETERSHEAD):\n\tglobal __lambdalog\n\tmsg = PACKEDPARAMETERS\n\tfullresponse = lambda_client.invoke(FunctionName="FUNCNAME_lambda", Payload=json.dumps(msg))\n\t#response = json.loads(fullresponse["Payload"].read())\n\tresponse = json.loads(fullresponse["Payload"].read().decode("utf-8"))\n\tif "log" in response:\n\t\t__lambdalog += response["log"]\n\treturn response["ret"]\n'
netproxy_template = '\nimport json\nimport importlib\ndef Netproxy(d, classname, name, args):\n\tif "." in classname:\n\t\tmodname, classname = classname.split(".")\n\t\tmod = importlib.import_module(modname)\n\t\timportlib.reload(mod)\n\t\tC = getattr(mod, classname)\n\telse:\n\t\tC = globals()[classname]\n\t_o = C()\n\t_o.__dict__ = json.loads(d)\n\tret = getattr(_o, name)(*args)\n\td = json.dumps(_o.__dict__)\n\treturn d, ret\n\ndef netproxy_handler(event, context):\n\tn = Netproxy(event["d"], event["classname"], event["name"], event["args"])\n\treturn n\n'

def getlambdafunctions(endpoint):
    runcode = '{:s} lambda list-functions | grep FunctionName | cut -d \'"\' -f 4'.format(awstool(endpoint))
    proc = subprocess.Popen(runcode, stdout=subprocess.PIPE, shell=True)
    stdoutresults = proc.communicate()[0].decode('utf-8')
    lambdafunctions = stdoutresults.strip().split('\n')
    return lambdafunctions


def moveinternal(moveglobals, function, arguments, body, local, lambdafunctions, imports, dependencies, tainted, features, role, debug, endpoint, globalvars, cfc):

    def pack(x):
        return '"{:s}": {:s}'.format(x, x)

    def unpack(x):
        return '{:s} = event["{:s}"]'.format(x, x)

    parameters = arguments.get(function, [])
    unpackparameters = ';'.join(map(unpack, parameters))
    packedparameters = '{' + ','.join(map(pack, parameters)) + '}'
    t = template
    t = t.replace('AWSTOOL', ','.join(['"' + x + '"' for x in awstool(endpoint).split(' ')]))
    t = t.replace('FUNCNAME', function)
    t = t.replace('PARAMETERSHEAD', ','.join(parameters))
    t = t.replace('PACKEDPARAMETERS', packedparameters)
    t = t.replace('UNPACKPARAMETERS', unpackparameters)
    gencode = '\n'.join(map(lambda node: '\n'.join(['\t' + x for x in codegen.to_source(node, indent_with='\t').split('\n')]), body))
    t = t.replace('FUNCTIONIMPLEMENTATION', gencode[1:])
    t = t.replace('LOCAL', ('False', 'True')[local])
    for module in ('json', 'subprocess'):
        if module not in moveglobals:
            exec('import {:s}'.format(module), moveglobals)

    if debug and not local:
        print(t)
    exec(t, moveglobals)
    if local:
        return t
    lambdafunction = '{:s}_lambda'.format(function)
    if lambdafunction in lambdafunctions:
        printlambada('deployer: already deployed {:s}'.format(lambdafunction))
    else:
        printlambada('deployer: new deployment of {:s}'.format(lambdafunction))
        tmpdir = tempfile.TemporaryDirectory()
        filename = '{:s}/{:s}.py'.format(tmpdir.name, lambdafunction)
        f = open(filename, 'w')
        if 'print' in features.get(function, []):
            f.write('from __future__ import print_function\n')
            f.write("__lambdalog = ''\n")
            f.write('def print(*args, **kwargs):\n')
            f.write('\tglobal __lambdalog\n')
            f.write("\t__lambdalog += ''.join([str(arg) for arg in args]) + '\\n'\n")
        else:
            monadic = False
            for dep in dependencies.get(function, []):
                if 'print' in features.get(dep, []):
                    monadic = True

            if monadic:
                f.write("__lambdalog = ''\n")
        f.write("__lambdalog = ''\n")
        for importmodule in imports:
            f.write('import {:s}\n'.format(importmodule))

        for globalvar in globalvars:
            f.write('{:s} = {:s}\n'.format(globalvar[0], globalvar[1]))

        if len(dependencies.get(function, [])) > 0:
            f.write('import json\n')
            f.write('from boto3 import client as boto3_client\n')
            if endpoint:
                f.write("lambda_client = boto3_client('lambda', endpoint_url='{:s}')\n".format(endpoint))
            else:
                f.write("lambda_client = boto3_client('lambda')\n")
            f.write('\n')
            for dep in dependencies.get(function, []):
                f.write('# dep {:s}\n'.format(dep))
                t = proxytemplate
                if monadic:
                    t = proxytemplate_monadic
                depparameters = arguments.get(dep, [])
                packeddepparameters = '{' + ','.join(map(pack, depparameters)) + '}'
                t = t.replace('FUNCNAME', dep)
                t = t.replace('PARAMETERSHEAD', ','.join(depparameters))
                t = t.replace('PACKEDPARAMETERS', packeddepparameters)
                f.write('{:s}\n'.format(t))
                f.write('\n')

            f.write('def {:s}(event, context):\n'.format(lambdafunction))
            f.write('\t{:s}\n'.format(unpackparameters))
            f.write('{:s}\n'.format(gencode))
            f.flush()
            zf = tempfile.NamedTemporaryFile(prefix='lambada_', suffix='_{:s}.zip'.format(function))
            zipper = zipfile.ZipFile(zf, mode='w')
            zipper.write(f.name, arcname='{:s}.py'.format(lambdafunction))
            zipper.close()
            zipname = zf.name
            printlambada('deployer: zip {:s} -> {:s}'.format(lambdafunction, zipname))
            runcode = "{:s} lambda create-function --function-name '{:s}' --description 'Lambada remote function' --runtime 'python3.6' --role '{:s}' --handler '{:s}.{:s}' --zip-file 'fileb://{:s}'".format(awstool(endpoint), lambdafunction, role, lambdafunction, lambdafunction, zipname)
            if cfc:
                if cfc.memory:
                    runcode += ' --memory-size {}'.format(cfc.memory)
                if cfc.duration:
                    runcode += ' --timeout {}'.format(cfc.duration)
                proc = subprocess.Popen(runcode, stdout=subprocess.PIPE, shell=True)
                proc.wait()
                reverse = False
                for revdepfunction in dependencies:
                    if revdepfunction in tainted:
                        pass
                    else:
                        for revdep in dependencies[revdepfunction]:
                            if revdep == function:
                                reverse = True

    if reverse:
        printlambada('deployer: reverse dependencies require role authorisation')
        runcode = "{:s} lambda add-permission --function-name '{:s}' --statement-id {:s}_reverse --action lambda:InvokeFunction --principal {:s}".format(awstool(endpoint), lambdafunction, lambdafunction, role)
        proc = subprocess.Popen(runcode, stdout=subprocess.PIPE, shell=True)
        proc.wait()


def move(moveglobals, local=False, lambdarolearn=None, module=None, debug=False, endpoint=None, annotations=False):
    if not lambdarolearn and not local:
        printlambada('role not set, trying to read environment variable LAMBDAROLEARN')
        lambdarolearn = os.getenv('LAMBDAROLEARN')
        if not lambdarolearn:
            printlambada('environment variable not set, trying to assemble...')
            runcode = "{} sts get-caller-identity --output text --query 'Account'".format(awstool(endpoint))
            proc = subprocess.Popen(runcode, stdout=subprocess.PIPE, shell=True)
            stdoutresults = proc.communicate()[0].decode('utf-8').strip()
            if len(stdoutresults) == 12:
                lambdarolearn = 'arn:aws:iam::{:s}:role/lambda_basic_execution'.format(stdoutresults)
                printlambada('... assembled', lambdarolearn)
            if not lambdarolearn:
                raise Exception('Role not set - check lambdarolearn=... or LAMBDAROLEARN=...')
            if not local:
                lambdafunctions = getlambdafunctions(endpoint)
        else:
            lambdafunctions = None
        imports = []
        functions = []
        globalvars = []
        classes = []
        for moveglobal in list(moveglobals):
            if type(moveglobals[moveglobal]) == type(ast):
                if moveglobal != moveglobals[moveglobal].__name__:
                    moveglobal = '{:s} as {:s}'.format(moveglobals[moveglobal].__name__, moveglobal)
                if moveglobal not in ('lambada', '__builtins__'):
                    imports.append(moveglobal)
            else:
                if type(moveglobals[moveglobal]) == type(move):
                    functions.append(moveglobal)
                else:
                    if type(moveglobals[moveglobal]) == type(str):
                        classes.append(moveglobals[moveglobal])
                    elif not moveglobal.startswith('__'):
                        mgvalue = moveglobals[moveglobal]
                        if type(mgvalue) == str:
                            mgvalue = "'" + mgvalue + "'"
                        else:
                            mgvalue = str(mgvalue)
                        globalvars.append((moveglobal, mgvalue))

        tainted, args, bodies, dependencies, features, classbodies, cfcs = analyse(None, functions, module, annotations)
        tsource = ''
        for classobj in classes:
            functionproxy.scanclass(None, None, classobj.__name__)

        for function in functions:
            if function in tainted:
                printlambada('skip tainted', function)
            else:
                printlambada('move', function)
                t = moveinternal(moveglobals, function, args, bodies.get(function, []), local, lambdafunctions, imports, dependencies, tainted, features, lambdarolearn, debug, endpoint, globalvars, cfcs.get(function, None))
                if t:
                    tsource += t

        for classbody in classbodies:
            tsource += codegen.to_source(classbodies[classbody], indent_with='\t')

        if len(classbodies) > 0:
            tsource += netproxy_template
        if tsource:
            for globalvar in globalvars:
                tsource = '{:s} = {:s}\n'.format(globalvar[0], globalvar[1]) + tsource

            tsource = "__lambdalog = ''\n" + tsource
            for importmodule in imports + ['json', 'subprocess']:
                tsource = 'import {:s}\n'.format(importmodule) + tsource

            if debug:
                print(tsource)
            lambmodule = module.replace('.py', '_lambdafied.py')
            printlambada('store', lambmodule)
            f = open(lambmodule, 'w')
            f.write(tsource)
            f.close()