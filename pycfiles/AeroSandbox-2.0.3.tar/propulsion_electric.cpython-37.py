# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\projects\github\aerosandbox\aerosandbox\library\propulsion_electric.py
# Compiled at: 2020-03-15 02:07:39
# Size of source mod 2**32: 11799 bytes
import numpy as np, casadi as cas

def motor_electric_performance(voltage=None, current=None, rpm=None, torque=None, kv=1000, resistance=0.1, no_load_current=0.4):
    """
    A function for predicting the performance of an electric motor.
    Performance equations based on Mark Drela's First Order Motor Model:
    http://web.mit.edu/drela/Public/web/qprop/motor1_theory.pdf
    Instructions: Input EXACTLY TWO of the following parameters: voltage, current, rpm, torque.
    Exception: You cannot supply the combination of current and torque - this makes for an ill-posed problem.
    The function will output a tuple of all four parameters, plus efficiency: (voltage, current, rpm, torque, efficiency)
    :param voltage: Voltage across motor terminals [Volts]
    :param current: Current through motor [Amps]
    :param rpm: Motor rotation speed [rpm]
    :param torque: Motor torque [N m]
    :param kv: voltage constant, in rpm/volt
    :param resistance: resistance, in ohms
    :param no_load_current: no-load current, in amps
    :return: tuple of all four parameters, plus efficiency: (voltage, current, rpm, torque, efficiency)
    """
    voltage_known = voltage is not None
    current_known = current is not None
    rpm_known = rpm is not None
    torque_known = torque is not None
    assert voltage_known + current_known + rpm_known + torque_known == 2, 'You must give exactly two input arguments.'
    if current_known:
        if torque_known:
            raise AssertionError('You cannot supply the combination of current and torque - this makes for an ill-posed problem.')
    kv_rads_per_sec_per_volt = kv * np.pi / 30
    while voltage_known:
        if not (current_known and rpm_known and torque_known):
            if rpm_known:
                if current_known:
                    if not voltage_known:
                        speed = rpm * np.pi / 30
                        back_EMF_voltage = speed / kv_rads_per_sec_per_volt
                        voltage = back_EMF_voltage + current * resistance
                        voltage_known = True
        elif torque_known:
            current = current_known or torque * kv_rads_per_sec_per_volt + no_load_current
            current_known = True
        if voltage_known:
            if rpm_known:
                if not current_known:
                    speed = rpm * np.pi / 30
                    back_EMF_voltage = speed / kv_rads_per_sec_per_volt
                    current = (voltage - back_EMF_voltage) / resistance
                    current_known = True
            if not rpm_known:
                if current_known:
                    back_EMF_voltage = voltage - current * resistance
                    speed = back_EMF_voltage * kv_rads_per_sec_per_volt
                    rpm = speed * 30 / np.pi
                    rpm_known = True
        if current_known:
            torque = torque_known or (current - no_load_current) / kv_rads_per_sec_per_volt
            torque_known = True

    efficiency = rpm * np.pi / 30 * torque / (voltage * current)
    return (
     voltage, current, rpm, torque, efficiency)


def motor_resistance_from_no_load_current(no_load_current):
    """
    Estimates the internal resistance of a motor from its no_load_current. Gates quotes R^2=0.93 for this model.
    Source: Gates, et. al., "Combined Trajectory, Propulsion, and Battery Mass Optimization for Solar-Regen..."
        https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=3932&context=facpub
    :param no_load_current: No-load current [amps]
    :return: motor internal resistance [ohms]
    """
    return 0.0467 * no_load_current ** (-1.892)


def mass_ESC(max_power):
    """
    Estimates the mass of an ESC.
    Informal correlation I did to Hobbyking ESCs in the 8s 100A range
    :param max_power: maximum power [W]
    :return: estimated ESC mass [kg]
    """
    return 2.38e-05 * max_power


def mass_battery_pack(battery_capacity_Wh, battery_cell_specific_energy_Wh_kg=240, battery_pack_cell_fraction=0.7):
    """
    Estimates the mass of a lithium-polymer battery.
    :param battery_capacity_Wh: Battery capacity, in Watt-hours [W*h]
    :param battery_cell_specific_energy: Specific energy of the battery at the CELL level [W*h/kg]
    :param battery_pack_cell_fraction: Fraction of the battery pack that is cells, by weight.
    :return: Estimated battery mass [kg]
    """
    return battery_capacity_Wh / battery_cell_specific_energy_Wh_kg / battery_pack_cell_fraction


def mass_motor_electric(max_power, kv_rpm_volt=1000, voltage=20, method='astroflight'):
    r"""
    Estimates the mass of a brushless DC electric motor.
    Curve fit to scraped Hobbyking BLDC motor data as of 2/24/2020.
    Estimated range of validity: 50 < max_power < 10000
    :param max_power: maximum power [W]
    :param kv: Voltage constant of the motor, measured in rpm/volt, not rads/sec/volt! [rpm/volt]
    :param voltage: Operating voltage of the motor [V]
    :param method: method to use. "burton", "hobbyking", or "astroflight" (increasing level of detail).
    Burton source: https://dspace.mit.edu/handle/1721.1/112414
    Hobbyking source: C:\Projects\GitHub\MotorScraper, https://github.com/austinstover/MotorScraper
    Astroflight source: Gates, et. al., "Combined Trajectory, Propulsion, and Battery Mass Optimization for Solar-Regen..."
        https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=3932&context=facpub
        Validity claimed from 1.5 kW to 15 kW, kv from 32 to 1355.
    :return: estimated motor mass [kg]
    """
    if method == 'burton':
        return max_power / 4128
    if method == 'hobbyking':
        return 10 ** (0.8205 * cas.log10(max_power) - 3.155)
    if method == 'astroflight':
        max_current = max_power / voltage
        return 2.464 * max_current / kv_rpm_volt + 0.368


def mass_wires(wire_length, max_current, allowable_voltage_drop, material='aluminum', insulated=True, max_voltage=600, wire_packing_factor=1, insulator_density=1700, insulator_dielectric_strength=12000000.0):
    """
    Estimates the mass of wires used for power transmission.
    Materials data from: https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity#Resistivity-density_product
        All data measured at STP; beware, as this data (especially resistivity) can be a strong function of temperature.
    :param wire_length: Length of the wire [m]
    :param max_current: Max current of the wire [Amps]
    :param allowable_voltage_drop: How much is the voltage allowed to drop along the wire?
    :param material: Conductive material of the wire ("aluminum")
    :param insulated: Should we add the mass of the wire's insulator coating? Usually you'll want to leave this True.
    :param max_voltage: Maximum allowable voltage (used for sizing insulator). 600 is a common off-the-shelf rating.
    :param wire_packing_factor: What fraction of the enclosed cross section is conductor? This is 1 for a solid-core wire and less than 1 for a stranded wire.
    :param insulator_density: Density of the wire insulator [kg/m^3]
    :param insulator_dielectric_strength: Dielectric strength of the wire insulator [V/m]. 12e6 corresponds to rubber.
    :return: Mass of the wire [kg]
    """
    if material == 'sodium':
        density = 970
        resistivity = 4.77e-08
    else:
        if material == 'lithium':
            density = 530
            resistivity = 9.28e-08
        else:
            if material == 'calcium':
                density = 1550
                resistivity = 3.36e-08
            else:
                if material == 'potassium':
                    density = 890
                    resistivity = 7.2e-08
                else:
                    if material == 'beryllium':
                        density = 1850
                        resistivity = 3.56e-08
                    else:
                        if material == 'aluminum':
                            density = 2700
                            resistivity = 2.65e-08
                        else:
                            if material == 'magnesium':
                                density = 1740
                                resistivity = 4.39e-08
                            else:
                                if material == 'copper':
                                    density = 8960
                                    resistivity = 1.678e-08
                                else:
                                    if material == 'silver':
                                        density = 10490
                                        resistivity = 1.587e-08
                                    else:
                                        if material == 'gold':
                                            density = 19300
                                            resistivity = 2.214e-08
                                        else:
                                            if material == 'iron':
                                                density = 7874
                                                resistivity = 9.61e-08
                                            else:
                                                raise ValueError("Bad value of 'material'!")
    resistance = allowable_voltage_drop / max_current
    area_conductor = resistivity * wire_length / resistance
    volume_conductor = area_conductor * wire_length
    mass_conductor = volume_conductor * density
    if insulated:
        insulator_thickness = max_voltage / insulator_dielectric_strength
        radius_conductor = (area_conductor / wire_packing_factor / np.pi) ** 0.5
        radius_insulator = radius_conductor + insulator_thickness
        area_insulator = np.pi * radius_insulator ** 2 - area_conductor
        volume_insulator = area_insulator * wire_length
        mass_insulator = insulator_density * volume_insulator
    else:
        mass_insulator = 0
    return mass_conductor + mass_insulator


if __name__ == '__main__':
    print(motor_electric_performance(rpm=100,
      current=3))
    print(motor_electric_performance(rpm=4700,
      torque=0.02482817))
    print(mass_battery_pack(100))
    pows = np.logspace(2, 4, 300)
    mass_mot_burton = mass_motor_electric(pows, method='burton')
    mass_mot_hobbyking = mass_motor_electric(pows, method='hobbyking')
    mass_mot_astroflight = mass_motor_electric(pows, method='astroflight')
    import matplotlib.pyplot as plt
    import matplotlib.style as style
    import plotly.express as px
    import plotly.graph_objects as go
    import dash, seaborn as sns
    sns.set(font_scale=1)
    plt.loglog(pows, (np.array(mass_mot_burton)), label='Burton Model')
    plt.plot(pows, (np.array(mass_mot_hobbyking)), label='Hobbyking Model')
    plt.plot(pows, (np.array(mass_mot_astroflight)), label='Astroflight Model')
    plt.xlabel('Motor Power [W]')
    plt.ylabel('Motor Mass [kg]')
    plt.title('Motor Mass Models')
    plt.tight_layout()
    plt.legend()
    plt.show()
    print(mass_wires(wire_length=1,
      max_current=100,
      allowable_voltage_drop=1,
      material='aluminum'))