# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/SRMspinanalysis/plot.py
# Compiled at: 2018-05-29 13:31:12
import matplotlib.pyplot as plt, numpy as np

def plot_Euler_angles(t, psi, theta, phi, title='Eulerian Angle Time Profiles', xlabel='Time (s)'):
    """Plots Euler angle time profiles of launch vehicle in degrees.

    Args:
        t (np.array()): Time vector (s).
        psi (np.array()): Array of Euler angle psi values (rad).
        theta (np.array()): Array of Euler angle theta values (rad).
        phi (np.array()): Array of Euler angle phi values (rad).
        title (str): OPTIONAL. Title of plot.
        xlabel (str): OPTIONAL. Label of x-axis of plot.

    """
    plt.figure(1)
    plt.subplot(311)
    plt.plot(t, psi)
    plt.title(title)
    plt.ylabel('$\\psi$ (rad)')
    plt.subplot(312)
    plt.plot(t, theta)
    plt.ylabel('$\\theta$ (rad)')
    plt.subplot(313)
    plt.plot(t, phi)
    plt.xlabel(xlabel)
    plt.ylabel('$\\phi$ (rad)')


def plot_nutation_angle(t, nutation_angle, title='Nutation Angle Time Profile', xlabel='Time (s)', ylabel='Nutation Angle (degrees)'):
    """Plots nutation angle time profile of launch vehicle in degrees.

    Args:
        t (np.array()): Time vector (s).
        nutation_angle (np.array()): Array of nutation angle values (rad).
        title (str): OPTIONAL. Title of plot.
        xlabel (str): OPTIONAL. Label of x-axis of plot.
        ylabel (str): OPTIONAL. Label of y-axis of plot.

    """
    plt.figure(2)
    plt.plot(t, nutation_angle)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def plot_longitudinal_axis(t, nutation_angle, precession_angle, title='Longitudinal Axis Path', xlabel='X Displacement', ylabel='Y Displacement'):
    """Plots path of longitudinal axis of launch vehicle at center of mass.

    Args:
        t (np.array()): Time vector (s).
        nutation_angle (np.array()): Array of nutation angle values (rad).
        precession_angle (np.array()): Array of precession angle values (rad).
        title (str): OPTIONAL. Title of plot.
        xlabel (str): OPTIONAL. Label of x-axis of plot.
        ylabel (str): OPTIONAL. Label of y-axis of plot.

    """
    plt.figure(3)
    plt.plot(np.multiply(nutation_angle, np.cos(precession_angle)), np.multiply(nutation_angle, np.sin(precession_angle)))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def plot_all(t, psi, theta, phi, nutation_angle, precession_angle):
    """Plots Euler angle time profiles, nutation angle time profile, and path of
    longitudinal axis of launch vehicle at center of mass.

    Args:
        t (np.array()): Time vector (s).
        psi (np.array()): Array of Euler angle psi values (rad).
        theta (np.array()): Array of Euler angle theta values (rad).
        phi (np.array()): Array of Euler angle phi values (rad).
        nutation_angle (np.array()): Array of nutation angle values (rad).
        precession_angle (np.array()): Array of precession angle values (rad).

    """
    plot_Euler_angles(t, psi, theta, phi)
    plot_nutation_angle(t, nutation_angle)
    plot_longitudinal_axis(t, nutation_angle, precession_angle)
    plt.show()