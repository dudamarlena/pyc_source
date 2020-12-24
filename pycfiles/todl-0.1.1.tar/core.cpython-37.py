# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/utils/flags/core.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 4616 bytes
"""Public interface for flag definition.

See _example.py for detailed instructions on defining flags.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys
from six.moves import shlex_quote
from absl import app as absl_app
from absl import flags
from official.utils.flags import _base
from official.utils.flags import _benchmark
from official.utils.flags import _conventions
from official.utils.flags import _device
from official.utils.flags import _distribution
from official.utils.flags import _misc
from official.utils.flags import _performance

def set_defaults(**kwargs):
    for key, value in kwargs.items():
        flags.FLAGS.set_default(name=key, value=value)


def parse_flags(argv=None):
    """Reset flags and reparse. Currently only used in testing."""
    flags.FLAGS.unparse_flags()
    absl_app.parse_flags_with_usage(argv or sys.argv)


def register_key_flags_in_core(f):
    """Defines a function in core.py, and registers its key flags.

  absl uses the location of a flags.declare_key_flag() to determine the context
  in which a flag is key. By making all declares in core, this allows model
  main functions to call flags.adopt_module_key_flags() on core and correctly
  chain key flags.

  Args:
    f:  The function to be wrapped

  Returns:
    The "core-defined" version of the input function.
  """

    def core_fn(*args, **kwargs):
        key_flags = f(*args, **kwargs)
        [flags.declare_key_flag(fl) for fl in key_flags]

    return core_fn


define_base = register_key_flags_in_core(_base.define_base)
define_base_eager = define_base
define_log_steps = register_key_flags_in_core(_benchmark.define_log_steps)
define_benchmark = register_key_flags_in_core(_benchmark.define_benchmark)
define_device = register_key_flags_in_core(_device.define_device)
define_image = register_key_flags_in_core(_misc.define_image)
define_performance = register_key_flags_in_core(_performance.define_performance)
define_distribution = register_key_flags_in_core(_distribution.define_distribution)
help_wrap = _conventions.help_wrap
get_num_gpus = _base.get_num_gpus
get_tf_dtype = _performance.get_tf_dtype
get_loss_scale = _performance.get_loss_scale
DTYPE_MAP = _performance.DTYPE_MAP
require_cloud_storage = _device.require_cloud_storage

def _get_nondefault_flags_as_dict():
    """Returns the nondefault flags as a dict from flag name to value."""
    nondefault_flags = {}
    for flag_name in flags.FLAGS:
        flag_value = getattr(flags.FLAGS, flag_name)
        if flag_name != flags.FLAGS[flag_name].short_name and flag_value != flags.FLAGS[flag_name].default:
            nondefault_flags[flag_name] = flag_value

    return nondefault_flags


def get_nondefault_flags_as_str():
    """Returns flags as a string that can be passed as command line arguments.

  E.g., returns: "--batch_size=256 --use_synthetic_data" for the following code
  block:

  ```
  flags.FLAGS.batch_size = 256
  flags.FLAGS.use_synthetic_data = True
  print(get_nondefault_flags_as_str())
  ```

  Only flags with nondefault values are returned, as passing default flags as
  command line arguments has no effect.

  Returns:
    A string with the flags, that can be passed as command line arguments to a
    program to use the flags.
  """
    nondefault_flags = _get_nondefault_flags_as_dict()
    flag_strings = []
    for name, value in sorted(nondefault_flags.items()):
        if isinstance(value, bool):
            flag_str = '--{}'.format(name) if value else '--no{}'.format(name)
        else:
            if isinstance(value, list):
                flag_str = '--{}={}'.format(name, ','.join(value))
            else:
                flag_str = '--{}={}'.format(name, value)
        flag_strings.append(flag_str)

    return ' '.join((shlex_quote(flag_str) for flag_str in flag_strings))