# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/erwincoumans/dev/tmp/bullet3/examples/pybullet/gym/pybullet_envs/bullet/minitaur_env_randomizer.py
# Compiled at: 2020-04-29 23:02:34
# Size of source mod 2**32: 2904 bytes
"""Randomize the minitaur_gym_env when reset() is called."""
import random, numpy as np
from . import env_randomizer_base
MINITAUR_BASE_MASS_ERROR_RANGE = (-0.2, 0.2)
MINITAUR_LEG_MASS_ERROR_RANGE = (-0.2, 0.2)
BATTERY_VOLTAGE_RANGE = (14.8, 16.8)
MOTOR_VISCOUS_DAMPING_RANGE = (0, 0.01)
MINITAUR_LEG_FRICTION = (0.8, 1.5)

class MinitaurEnvRandomizer(env_randomizer_base.EnvRandomizerBase):
    __doc__ = 'A randomizer that change the minitaur_gym_env during every reset.'

    def __init__(self, minitaur_base_mass_err_range=MINITAUR_BASE_MASS_ERROR_RANGE, minitaur_leg_mass_err_range=MINITAUR_LEG_MASS_ERROR_RANGE, battery_voltage_range=BATTERY_VOLTAGE_RANGE, motor_viscous_damping_range=MOTOR_VISCOUS_DAMPING_RANGE):
        self._minitaur_base_mass_err_range = minitaur_base_mass_err_range
        self._minitaur_leg_mass_err_range = minitaur_leg_mass_err_range
        self._battery_voltage_range = battery_voltage_range
        self._motor_viscous_damping_range = motor_viscous_damping_range

    def randomize_env(self, env):
        self._randomize_minitaur(env.minitaur)

    def _randomize_minitaur(self, minitaur):
        """Randomize various physical properties of minitaur.

    It randomizes the mass/inertia of the base, mass/inertia of the legs,
    friction coefficient of the feet, the battery voltage and the motor damping
    at each reset() of the environment.

    Args:
      minitaur: the Minitaur instance in minitaur_gym_env environment.
    """
        base_mass = minitaur.GetBaseMassFromURDF()
        randomized_base_mass = random.uniform(base_mass * (1.0 + self._minitaur_base_mass_err_range[0]), base_mass * (1.0 + self._minitaur_base_mass_err_range[1]))
        minitaur.SetBaseMass(randomized_base_mass)
        leg_masses = minitaur.GetLegMassesFromURDF()
        leg_masses_lower_bound = np.array(leg_masses) * (1.0 + self._minitaur_leg_mass_err_range[0])
        leg_masses_upper_bound = np.array(leg_masses) * (1.0 + self._minitaur_leg_mass_err_range[1])
        randomized_leg_masses = [np.random.uniform(leg_masses_lower_bound[i], leg_masses_upper_bound[i]) for i in range(len(leg_masses))]
        minitaur.SetLegMasses(randomized_leg_masses)
        randomized_battery_voltage = random.uniform(BATTERY_VOLTAGE_RANGE[0], BATTERY_VOLTAGE_RANGE[1])
        minitaur.SetBatteryVoltage(randomized_battery_voltage)
        randomized_motor_damping = random.uniform(MOTOR_VISCOUS_DAMPING_RANGE[0], MOTOR_VISCOUS_DAMPING_RANGE[1])
        minitaur.SetMotorViscousDamping(randomized_motor_damping)
        randomized_foot_friction = random.uniform(MINITAUR_LEG_FRICTION[0], MINITAUR_LEG_FRICTION[1])
        minitaur.SetFootFriction(randomized_foot_friction)