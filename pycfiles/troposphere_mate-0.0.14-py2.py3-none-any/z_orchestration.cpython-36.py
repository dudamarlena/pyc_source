# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/orch_example/web_app/z_orchestration.py
# Compiled at: 2019-08-08 16:17:45
# Size of source mod 2**32: 591 bytes
from superjson import json
from pathlib_mate import Path
from troposphere_mate.core.orch import Orchestration
from troposphere_mate.core.canned import Canned
from troposphere_mate.orch_example.web_app import t1_vpc, t99_master
orch = Orchestration()
orch.add_master_tier(t99_master.MasterTier)
orch.add_tier(t1_vpc.VPCTier)
orch.set_config_dir(Path(__file__).change(new_basename='config').abspath)
orch.add_execution_plan_file(Path(__file__).change(new_basename='plan.json').abspath)
orch.plan(workspace_dir=(Path(__file__).change(new_basename='tmp').abspath))