# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/bprc/core.py
# Compiled at: 2016-08-21 13:59:18
# Size of source mod 2**32: 4757 bytes
"""This module provides the main functionality of bprc.
Invocation flow:
  - Read, validate and process the input (args).
  - Parse the YAML file.
  - Create a Variables object from the yaml file.
    - Parse it and create the Variables object
  - Create the Recipe object from the yaml file.
    - Validate the Recipe Opbject
  - Iterate over the Recipe object
    - Invoke each step by:
      - Substiting any response, variable or file data into the current step
      - Executing the call
      - Updating all response objects
      - Writing the output
  - Exit.

"""
import os, sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import select, yaml, bprc.utils
from bprc.utils import vlog, errlog, verboseprint, logleveldict
import logging, bprc.cli
from bprc.recipe import Recipe
from bprc.variables import Variables
from bprc.stepprocessor import StepProcessor
from bprc.varprocessor import VarProcessor

def main():
    """
    The main function.
    Pre-process args
    and run the main program with error handling.
    Return exit status code.
    """
    if bprc.cli.args.yamlfile == sys.stdin and not select.select([sys.stdin], [], [], 0.0)[0]:
        bprc.cli.parser.print_usage()
        bprc.cli.parser.exit(status=1)
    if bprc.cli.args.loglevel == 'none':
        logging.basicConfig(level=logleveldict[bprc.cli.args.loglevel], format='%(levelname)s:%(asctime)s: %(message)s', handlers=[
         logging.NullHandler()])
    else:
        logging.basicConfig(level=logleveldict[bprc.cli.args.loglevel], filename=bprc.cli.args.logfile, format='%(levelname)s:%(asctime)s: %(message)s')
    logging.info('----------------Initialising log----------------')
    try:
        vlog('Loading yaml input...')
        datamap = yaml.safe_load(bprc.cli.args.yamlfile)
    except Exception as e:
        errlog('An error occured parsing the yaml input file', e)
        sys.exit(1)

    vlog('Yaml file parsed ok...')
    vlog('Instantiating variables object...')
    try:
        variables = Variables(datamap['variables'])
    except Exception as e:
        vlog('No variable object in YAML file')
        variables = Variables({})

    vlog('Variables object instantiated ok... (albeit maybe empty)')
    try:
        vlog('Instantiating recipe object...')
        r = Recipe(datamap)
        vlog('Recipe object instantiated ok...')
        vlog('Recipe-' + str(r))
    except Exception as e:
        errlog('Could not create Recipe Object.', e)
        sys.exit(2)

    vlog('Commencing variable parsing and substitution...')
    varprocessor = VarProcessor(variables)
    for varname, varval in variables.items():
        vlog('Commencing variable substitutions for variable ' + str(varname) + '=' + str(varval))
        variables[varname] = varprocessor.parse(varval, variables)
        vlog('Substituted ' + str(varname) + '=' + str(variables[varname]))

    for varname, varval in variables.items():
        vlog('Commencing filename-- substitutions for variable ' + str(varname) + '=' + str(varval))
        variables[varname] = varprocessor.fileparse(varval, variables)
        vlog('Substituted filespec ' + str(varname) + '=' + str(variables[varname]))

    vlog('Commencing processing loop...')
    for i, step in enumerate(r.steps):
        vlog('Commencing php-like substitutions for step ' + str(i) + ':' + r.steps[i].name)
        processor = StepProcessor(recipe=r, stepid=i, variables=variables)
        r.steps[i] = processor.prepare()
        vlog('Php-like substitutions complete for step ' + str(i) + ':' + r.steps[i].name)
        p_statement = processor.call()
        processor.generateOutput(p_statement)

    sys.exit(0)