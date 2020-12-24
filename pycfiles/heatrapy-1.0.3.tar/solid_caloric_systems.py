# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: heatrapy/systems/solid_caloric_systems.py
# Compiled at: 2018-04-19 10:39:50
from __future__ import unicode_literals
from .. import objects
from .. import fields
import time, numpy as np

def solid_active_regenerator(file_name, amb_temperature=293, left_thermalswitch_length=2, right_thermalswitch_length=2, MCM_length=20, right_reservoir_length=3, left_reservoir_length=3, MCM_material=((0.002, 'Gd'), ), left_thermalswitch_material=b'idealTS_hot', right_thermalswitch_material=b'idealTS_cold', left_reservoir_material=b'Cu', right_reservoir_material=b'Cu', freq=0.1, dt=0.01, dx=0.002, stop_criteria=0.005, solver=b'implicit_k(x)', min_cycle_number=30, max_cycle_number=31, field_removal_steps=3, field_applied_steps=1, field_removal_mode=b'accelerated_right', field_applied_mode=b'accelerated_left', cycle_points=25, boundaries=(293, 293), note=None, temperature_sensor=b'default', heat_points=b'default', mode=b'refrigerator', version=None, resting_time_hot=b'default', resting_time_cold=b'default', starting_field=b'applied', type_study=b'fixed_temperature_span', h_left=50000.0, h_right=50000.0, mod_freq=b'default'):
    """solid_active_regenerator class

    computes the thermal processes for 1-dimensional fully solid state
    ferroic-based systems. The active regenerative processes can be used with
    the several allowed modes for application and removal of fields. Cascades
    of materials can also be computed.

    file_name: file name where the temperature and heat flux are saved
    amb_temperature: ambient temperature of the whole system
    left_thermalswitch_length: length of the left thermal switch
    right_thermalswitch_length: length of the right thermal switch
    left_thermalswitch_material: string for the material of the
        left thermal switch
    right_thermalswitch_material: string for the material of the
        right thermal switch
    MCM_length: length of the caloric material
    MCM_material: string for the material of the caloric material
    left_reservoir_length: length of the left reservoir
    right_reservoir_length: length of the right reservoir
    left_reservoir_material: string for the material of the left reservoir
    right_reservoir_material: string for the material of the right reservoir
    freq: operating frequency
    dt: times step
    dx: space step
    stop_criteria: error threshold to stop the simulation
    solver: the solver
    min_cycle_number: minimum number of cycles that has to be computed
    max_cycle_number: maximum number of cycles that has to be computed
    field_removal_steps: number of steps during the field removal
    field_applied_steps: number of steps during the application of field
    field_removal_mode: mode of field removal
        modes can be constant_right, constant_left, accelerated_right,
        accelerated_left, decelerated_right, and decelerated_left
    field_applied_mode: mode of the application of field modes can be
        constant_right, constant_left, accelerated_right, accelerated_left,
        decelerated_right, and decelerated_left
    cycle_points: number of points recorded for each position for each cycle
    boundaries: tuple with the boundary conditions
    temperature_sensor: tuple of two space indexes used to determine the
        temperature span at the end of the simulation. The first term is
        the sensor at the hot end and the second at the cold end
    heat_points: tuple of two space indexes used to determine the heat
        flux for the hot end (first term) and cold end (second term)
    mode: mode used for the power calculations (e.g. COP) performed at the end
        of the simulation. It can be 'refrigerator' or 'heat_pump'
    version: heatrapy version (default is None)
    type_study: 'no_load' or 'fixed_temperature_span'
    h_left: left heat transfer coefficient
    h_right: right heat transfer coefficient
    mod_freq: if not 'default', i.e. if tuple, allows to modulate the
        frequency according to a specific temperature. The first element is
        the file_name, and second the sensor point.

    """
    cond01 = isinstance(file_name, unicode)
    cond01 = cond01 or isinstance(file_name, str)
    cond02 = isinstance(amb_temperature, float)
    cond02 = cond01 or isinstance(amb_temperature, int)
    cond03 = isinstance(left_thermalswitch_length, int)
    cond04 = isinstance(right_thermalswitch_length, int)
    cond05 = isinstance(MCM_length, int)
    cond06 = isinstance(left_reservoir_length, int)
    cond07 = isinstance(right_reservoir_length, int)
    cond08 = isinstance(MCM_material, tuple)
    cond09 = isinstance(left_thermalswitch_material, str)
    cond09 = cond09 or isinstance(left_thermalswitch_material, unicode)
    cond10 = isinstance(left_thermalswitch_material, str)
    cond10 = cond10 or isinstance(left_thermalswitch_material, unicode)
    cond11 = isinstance(left_reservoir_material, str)
    cond11 = cond11 or isinstance(left_reservoir_material, unicode)
    cond12 = isinstance(right_reservoir_material, str)
    cond12 = cond12 or isinstance(right_reservoir_material, unicode)
    cond13 = isinstance(freq, int) or isinstance(freq, float)
    cond14 = isinstance(dx, int) or isinstance(dx, float)
    cond15 = isinstance(dt, int) or isinstance(dt, float)
    cond16 = isinstance(stop_criteria, int) or isinstance(stop_criteria, float)
    cond17 = isinstance(solver, unicode) or isinstance(solver, str)
    cond18 = isinstance(min_cycle_number, int)
    cond19 = isinstance(max_cycle_number, int)
    cond20 = isinstance(field_removal_steps, int)
    cond21 = isinstance(field_applied_steps, int)
    allowed_modes = [b'constant_right', b'constant_left', b'accelerated_right',
     b'accelerated_left', b'decelerated_right',
     b'decelerated_left']
    cond22 = field_removal_mode in allowed_modes
    cond23 = field_applied_mode in allowed_modes
    cond24 = isinstance(cycle_points, int)
    cond25 = isinstance(boundaries, tuple)
    cond26 = mode == b'refrigerator' or mode == b'heat_pump'
    cond27 = starting_field == b'applied' or starting_field == b'removal'
    cond28 = type_study == b'no_load' or type_study == b'fixed_temperature_span'
    cond29 = isinstance(h_left, int) or isinstance(h_left, float)
    cond30 = isinstance(h_left, int) or isinstance(h_right, float)
    condition = cond01 and cond02 and cond03 and cond04 and cond05
    condition = condition and cond06 and cond07 and cond08 and cond09
    condition = condition and cond10 and cond11 and cond12 and cond13
    condition = condition and cond14 and cond15 and cond16 and cond17
    condition = condition and cond18 and cond19 and cond20 and cond21
    condition = condition and cond22 and cond23 and cond24 and cond25
    condition = condition and cond26 and cond27 and cond28 and cond29
    condition = condition and cond30
    if not condition:
        raise ValueError
    if resting_time_hot == b'default':
        resting_time_hot = 0.0
    if resting_time_cold == b'default':
        resting_time_cold = 0.0
    print b''
    print b''
    print b'######################################################'
    print b''
    print b'------------------------------------------------------'
    print file_name
    print b'------------------------------------------------------'
    print b''
    print b'heatconpy version:', version
    print b'Module: solid_active_regenerator'
    if note is not None:
        print b''
        print b'Note:', note
    print b''
    print b'Mode:', mode
    print b'System:',
    print left_reservoir_material + b'/' + left_thermalswitch_material + b'/MCM material/' + right_thermalswitch_material + b'/' + right_reservoir_material
    print b'Dimensions (m):',
    print str(dx * left_reservoir_length) + b'/' + str(dx * left_thermalswitch_length) + b'/' + str(dx * MCM_length) + b'/' + str(dx * right_thermalswitch_length) + b'/' + str(dx * right_reservoir_length)
    print b'Number of points:',
    print str(left_reservoir_length) + b'/' + str(left_thermalswitch_length) + b'/' + str(MCM_length) + b'/' + str(right_thermalswitch_length) + b'/' + str(right_reservoir_length)
    print b'MCM material:', MCM_material
    print b'Left heat transfer coefficient (W /(m2 K)):', h_left
    print b'Right heat transfer coefficient (W /(m2 K)):', h_right
    print b'dx (m):', dx
    print b'dt (s):', dt
    print b'Frequency (Hz):', freq
    print b'Hot resting time ratio:', resting_time_hot
    print b'Cold resting time ratio:', resting_time_cold
    print b'Solver:', solver
    print b'Frequency modulation:', mod_freq
    print b'Applied field mode:', field_applied_mode
    print b'Applied field steps:', field_applied_steps
    print b'Field removal mode:', field_removal_mode
    print b'Field removal steps:', field_removal_steps
    print b'Starting Field:', starting_field
    print b'Boundaries:', boundaries
    print b'Ambient temperature (K):', amb_temperature
    print b'Stop criteria:', stop_criteria
    print b'Time:', time.ctime()
    print b''
    start_time = time.time()
    if heat_points == b'default':
        if left_reservoir_length - 3 > 0:
            leftHeatSensor = left_reservoir_length - 3
        else:
            leftHeatSensor = 2
        if -right_reservoir_length + 3 < 0:
            rightHeatSensor = -right_reservoir_length + 3
        else:
            rightHeatSensor = -2
    else:
        leftHeatSensor = heat_points[0]
        rightHeatSensor = heat_points[1]
    if starting_field != b'applied':
        initial_state = True
    else:
        initial_state = False
    materials = (
     left_reservoir_material, left_thermalswitch_material,
     MCM_material[0][1], right_thermalswitch_material,
     right_reservoir_material)
    lRl = left_reservoir_length
    rRl = right_reservoir_length
    ltsl = left_thermalswitch_length
    rtsl = right_thermalswitch_length
    borders = (1, lRl + 1,
     lRl + ltsl + 1,
     lRl + ltsl + MCM_length + 1,
     lRl + ltsl + MCM_length + rtsl + 1,
     lRl + ltsl + MCM_length + rtsl + rRl + 1)
    heat_points = (leftHeatSensor, rightHeatSensor)
    a = objects.single_object(amb_temperature, dx=dx, dt=dt, file_name=file_name, materials=materials, borders=borders, materials_order=(0,
                                                                                                                                         1,
                                                                                                                                         2,
                                                                                                                                         3,
                                                                                                                                         4), boundaries=boundaries, heat_points=heat_points, initial_state=initial_state, h_left=50000.0, h_right=50000.0)
    k = left_reservoir_length + left_thermalswitch_length
    for i in range(len(MCM_material)):
        from .. import mats
        import os
        tadi = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + MCM_material[i][1] + b'/' + b'tadi.txt'
        tadd = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + MCM_material[i][1] + b'/' + b'tadd.txt'
        cpa = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + MCM_material[i][1] + b'/' + b'cpa.txt'
        cp0 = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + MCM_material[i][1] + b'/' + b'cp0.txt'
        k0 = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + MCM_material[i][1] + b'/' + b'k0.txt'
        ka = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + MCM_material[i][1] + b'/' + b'ka.txt'
        rho0 = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + MCM_material[i][1] + b'/' + b'rho0.txt'
        rhoa = os.path.dirname(os.path.realpath(__file__)) + b'/../database/' + MCM_material[i][1] + b'/' + b'rhoa.txt'
        a.materials.append(mats.calmatpro(tadi, tadd, cpa, cp0, k0, ka, rho0, rhoa))
        for j in range(k, k + int(MCM_material[i][0] / dx + 1)):
            a.materials_index[j] = len(a.materials) - 1

        k = k + int(MCM_material[i][0] / dx)

    if temperature_sensor == b'default':
        righttemperature_sensor = -(right_reservoir_length / 2)
        lefttemperature_sensor = left_reservoir_length / 2
    else:
        righttemperature_sensor = temperature_sensor[1]
        lefttemperature_sensor = temperature_sensor[0]
    value1 = amb_temperature
    value2 = amb_temperature
    i = 0
    period = 1.0 / freq
    stop_criteria2 = 0.0
    maximumPower = 0.0
    maximumWorkingPower = 0.0
    while (abs((value1 - value2) / value2) > stop_criteria or i < min_cycle_number or abs((value1 - value2) / value2) > stop_criteria2) and i < max_cycle_number:
        stop_criteria2 = abs((value1 - value2) / value2)
        heatLeft = a.heatLeft
        heatRight = a.heatRight
        if mod_freq != b'default':
            temperature_sensor = a.temperature[mod_freq[1]][0]
            input = open(mod_freq[0], b'r')
            s = input.readlines()
            xMod = []
            yMod = []
            for line in s:
                pair = line.split(b',')
                xMod.append(float(pair[0]))
                yMod.append(float(pair[1]))

            input.close()
            freq = np.interp(temperature_sensor, xMod, yMod)
            period = 1.0 / freq
        if starting_field == b'applied':
            com = [
             b'constant_left', b'accelerated_left', b'decelerated_left']
            if field_applied_mode in com:
                step_range = range(field_applied_steps - 1, -1, -1)
            else:
                step_range = range(field_applied_steps)
            for j in step_range:
                first = left_reservoir_length + j * (left_thermalswitch_length + MCM_length + right_thermalswitch_length) / field_applied_steps + 1
                second = left_reservoir_length + (j + 1) * (left_thermalswitch_length + MCM_length + right_thermalswitch_length) / field_applied_steps + 1
                a.activate(first, second)
                delta_t = fields.operating_mode(field_applied_mode, resting_time_cold, resting_time_hot, field_applied_steps, freq, j)
                a.compute(delta_t, int(1 / (freq * dt * cycle_points)), solver=solver)

            a.compute(resting_time_hot * period, int(1 / (freq * dt * cycle_points)), solver=solver)
            com = [
             b'constant_left', b'accelerated_left', b'decelerated_left']
            if field_removal_mode in com:
                step_range = range(field_removal_steps - 1, -1, -1)
            else:
                step_range = range(field_removal_steps)
            for j in step_range:
                first = left_reservoir_length + j * (left_thermalswitch_length + MCM_length + right_thermalswitch_length) / field_removal_steps + 1
                second = left_reservoir_length + (j + 1) * (left_thermalswitch_length + MCM_length + right_thermalswitch_length) / field_removal_steps + 1
                a.deactivate(first, second)
                delta_t = fields.operating_mode(field_removal_mode, resting_time_cold, resting_time_hot, field_removal_steps, freq, j)
                a.compute(delta_t, int(1 / (freq * dt * cycle_points)), solver=solver)

            time_interval = resting_time_cold * period
            write_interval = int(1 / (freq * dt * cycle_points))
            a.compute(time_interval, write_interval, solver=solver)
        if starting_field == b'removal':
            com = [
             b'constant_left', b'accelerated_left', b'decelerated_left']
            if field_removal_mode in com:
                step_range = range(field_removal_steps - 1, -1, -1)
            else:
                step_range = range(field_removal_steps)
            for j in step_range:
                first = left_reservoir_length + j * (left_thermalswitch_length + MCM_length + right_thermalswitch_length) / field_removal_steps + 1
                second = left_reservoir_length + (j + 1) * (left_thermalswitch_length + MCM_length + right_thermalswitch_length) / field_removal_steps + 1
                a.deactivate(first, second)
                delta_t = fields.operating_mode(field_removal_mode, resting_time_cold, resting_time_hot, field_removal_steps, freq, j)
                a.compute(delta_t, int(1 / (freq * dt * cycle_points)), solver=solver)

            time_interval = resting_time_cold * period
            write_interval = int(1 / (freq * dt * cycle_points))
            a.compute(time_interval, write_interval, solver=solver)
            com = [
             b'constant_left', b'accelerated_left', b'decelerated_left']
            if field_applied_mode in com:
                step_range = range(field_applied_steps - 1, -1, -1)
            else:
                step_range = range(field_applied_steps)
            for j in step_range:
                first = left_reservoir_length + j * (left_thermalswitch_length + MCM_length + right_thermalswitch_length) / field_applied_steps + 1
                second = left_reservoir_length + (j + 1) * (left_thermalswitch_length + MCM_length + right_thermalswitch_length) / field_applied_steps + 1
                a.activate(first, second)
                delta_t = fields.operating_mode(field_applied_mode, resting_time_cold, resting_time_hot, field_applied_steps, freq, j)
                a.compute(delta_t, int(1 / (freq * dt * cycle_points)), solver=solver)

            a.compute(resting_time_hot * period, int(1 / (freq * dt * cycle_points)), solver=solver)
        value1 = value2
        value2 = a.temperature[righttemperature_sensor][1]
        i = 1 + i

    before_final_cycle_time = a.time_passed - 1.0 / freq
    time_accumulated = 0.0
    file_temperature = open(file_name)
    lines = file_temperature.readlines()
    final_temperature_right = 0.0
    o = 1
    while float(lines[o].split(b',')[0]) < before_final_cycle_time:
        lines.pop(0)
        o = o + 1

    for o in range(1, len(lines)):
        time_before = float(lines[(o - 1)].split(b',')[0])
        time_now = float(lines[o].split(b',')[0])
        sensor = righttemperature_sensor - 2
        final_temperature_right = (time_now - time_before) * float(lines[o].split(b',')[sensor]) + final_temperature_right
        time_accumulated = time_accumulated + (time_now - time_before)

    final_temperature_right = final_temperature_right / time_accumulated
    file_temperature.close()
    before_final_cycle_time = a.time_passed - 1.0 / freq
    time_accumulated = 0.0
    file_temperature = open(file_name)
    lines = file_temperature.readlines()
    final_temperature_left = 0.0
    o = 1
    while float(lines[o].split(b',')[0]) < before_final_cycle_time:
        lines.pop(0)
        o = o + 1

    for o in range(1, len(lines)):
        time_before = float(lines[(o - 1)].split(b',')[0])
        time_now = float(lines[o].split(b',')[0])
        sensor = lefttemperature_sensor + 1
        final_temperature_left = (time_now - time_before) * float(lines[o].split(b',')[sensor]) + final_temperature_left
        time_accumulated = time_accumulated + (time_now - time_before)

    final_temperature_left = final_temperature_left / time_accumulated
    file_temperature.close()
    endTime = time.time()
    simulationTime = endTime - start_time
    hours = int(simulationTime / 3600)
    minutes = int((simulationTime - hours * 3600) / 60)
    seconds = int(simulationTime - hours * 3600 - minutes * 60)
    hours = b'%02d' % hours
    minutes = b'%02d' % minutes
    seconds = b'%02d' % seconds
    print b'------------------------------------------------------'
    print b''
    print b'Number of cycles:', i
    print b'Final cycle error:', abs((value1 - value2) / value2)
    if type_study == b'fixed_temperature_span':
        heating_power = -(a.heatLeft - heatLeft) / period
        cooling_power = -(a.heatRight - heatRight) / period
        working_power = heating_power - cooling_power
        print b'Heating power (W):', heating_power
        print b'Cooling power (W):', cooling_power
        print b'Working power (W):', working_power
        if mode == b'refrigerator':
            print b'COP:', cooling_power / working_power
        if mode == b'heat_pump':
            print b'COP:', heating_power / working_power
    else:
        temperature_span = -final_temperature_right + final_temperature_left
        if mode == b'refrigerator':
            print b'No load temperature span (K):', temperature_span
        if mode == b'heat_pump':
            print b'No load temperature span (K):', -temperature_span
    print b'Final time (s):', a.time_passed
    print b'Simulation duration:', hours + b':' + minutes + b':' + seconds
    print b''
    print b'------------------------------------------------------'
    print b''
    print b''
    print b''
    return