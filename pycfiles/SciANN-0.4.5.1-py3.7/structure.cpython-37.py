# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/docs/structure.py
# Compiled at: 2020-03-28 23:01:31
# Size of source mod 2**32: 2577 bytes
"""
General documentation architecture:

Home
Index

- Getting started
    Guide to SciANN model
    Guide to Functional
    FAQ

- SciModels
    About SciANN models
        explain when one should use Sequential or functional API
        explain compilation step
        explain weight saving, weight loading
        explain serialization, deserialization
    Sequential
    Model (functional API)

- Functionals
    About SciANN functionals
        explain common functional operations: get_weights, set_weights, get_config
        explain input_shape
        explain usage on non-Keras tensors
    Variables
    Fields
    Functionals 

Operations
Constraints 

"""
from sciann import utils
from sciann import Functional
from sciann import Variable
from sciann import Field
from sciann import SciModel
from sciann import constraints
from sciann import utils
from sciann import Parameter
EXCLUDE = {
 'Constraint'}
PAGES = [
 {'page':'scimodels.md', 
  'classes':[
   SciModel], 
  'methods':[
   SciModel.train,
   SciModel.predict,
   SciModel.loss_functions]},
 {'page':'functionals.md', 
  'classes':[
   Functional,
   Variable,
   Field,
   Parameter]},
 {'page':'variables.md', 
  'classes':[
   Variable]},
 {'page':'fields.md', 
  'classes':[
   Field]},
 {'page':'constraints.md', 
  'classes':[
   constraints.Data,
   constraints.PDE,
   constraints.Tie]},
 {'page':'utils.md', 
  'methods':[
   utils.math.grad,
   utils.math.diag_grad,
   utils.math.div,
   utils.math.radial_basis,
   utils.math.sin,
   utils.math.asin,
   utils.math.cos,
   utils.math.acos,
   utils.math.tan,
   utils.math.atan,
   utils.math.tanh,
   utils.math.exp,
   utils.math.pow,
   utils.math.add,
   utils.math.sub,
   utils.math.mul,
   utils.math.div]}]
ROOT = 'https://sciann.com/'
template_np_implementation = '# Numpy implementation\n\n    ```python\n{{code}}\n    ```\n'
template_hidden_np_implementation = '# Numpy implementation\n\n    <details>\n    <summary>Show the Numpy implementation</summary>\n\n    ```python\n{{code}}\n    ```\n\n    </details>\n'