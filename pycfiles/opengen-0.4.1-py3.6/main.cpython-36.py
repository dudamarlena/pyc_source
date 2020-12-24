# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/main.py
# Compiled at: 2020-04-13 16:50:17
# Size of source mod 2**32: 2070 bytes
import casadi.casadi as cs, opengen as og
u = cs.SX.sym('u', 5)
p = cs.SX.sym('p', 2)
phi = og.functions.rosenbrock(u, p)
f2 = cs.fmax(0.0, u[2] - u[3] + 0.1)
f1 = cs.vertcat(1.5 * u[0] - u[1], cs.sin(u[2] + cs.pi / 5) - 0.2)
C = og.constraints.Ball2(None, 1.0)
UA = og.constraints.FiniteSet([[1, 2, 3], [1, 2, 2], [1, 2, 4], [0, 5, -1]])
UB = og.constraints.Ball2(None, 1.0)
U = og.constraints.CartesianProduct(5, [2, 4], [UA, UB])
problem = og.builder.Problem(u, p, phi).with_constraints(U).with_aug_lagrangian_constraints(f1, C)
meta = og.config.OptimizerMeta().with_version('0.0.0').with_authors([
 'P. Sopasakis', 'E. Fresk']).with_licence('CC4.0-By').with_optimizer_name('the_optimizer')
build_config = og.config.BuildConfiguration().with_build_directory('my_optimizers').with_build_mode('debug').with_tcp_interface_config()
solver_config = og.config.SolverConfiguration().with_tolerance(1e-05).with_initial_penalty(1000).with_initial_tolerance(1e-05).with_max_outer_iterations(30).with_delta_tolerance(0.0001).with_penalty_weight_update_factor(2).with_sufficient_decrease_coefficient(0.5)
builder = og.builder.OpEnOptimizerBuilder(problem, metadata=meta,
  build_configuration=build_config,
  solver_configuration=solver_config)
builder.build()
mng = og.tcp.OptimizerTcpManager('my_optimizers/the_optimizer')
mng.start()
pong = mng.ping()
print(pong)
solution = mng.call([1.0, 50.0])
print(solution.get().solution)
mng.kill()