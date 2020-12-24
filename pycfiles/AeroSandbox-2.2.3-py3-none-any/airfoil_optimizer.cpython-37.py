# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\tools\airfoil_optimizer\airfoil_optimizer.py
# Compiled at: 2020-04-22 01:22:30
# Size of source mod 2**32: 2900 bytes
from aerosandbox.geometry import *
from scipy import optimize
Re = 500000.0
CL = 1.25
CM = -0.133
lower_guess = -0.1 * np.ones(3)
upper_guess = 0.1 * np.ones(3)
n_lower = len(lower_guess)
n_upper = len(upper_guess)
pack = lambda lower, upper: np.concatenate((lower, upper))
unpack = lambda pack: (pack[:n_lower], pack[n_lower:])

def make_airfoil(x):
    lower, upper = unpack(x)
    return Airfoil(name='Optimization Airfoil',
      coordinates=kulfan_coordinates(lower_weights=lower,
      upper_weights=upper,
      TE_thickness=0.005,
      n_points_per_side=200))


x0 = pack(lower_guess, upper_guess)
initial_airfoil = make_airfoil(x0)

def draw(airfoil):
    fig = plt.figure()
    plt.plot((initial_airfoil.coordinates[:, 0]),
      (initial_airfoil.coordinates[:, 1]),
      ':',
      label='Initial Airfoil')
    plt.plot((airfoil.coordinates[:, 0]),
      (airfoil.coordinates[:, 1]),
      '-',
      label='Current Airfoil')
    plt.show()


def augmented_objective(x):
    lower, upper = unpack(x)
    airfoil = make_airfoil(x)
    xfoil = airfoil.xfoil_a(alpha=3,
      Re=Re,
      verbose=False,
      max_iter=30,
      reset_bls=True,
      repanel=False)
    Cd = xfoil['Cd']
    if np.isnan(Cd):
        Cd = 0.1
    objective = Cd / 0.02
    penalty = 0
    penalty += np.sum(np.maximum(0, lower + 0.05) ** 2 / 0.01)
    penalty += np.sum(np.minimum(0, upper - 0.05) ** 2 / 0.01)
    return objective + penalty


def callback(x):
    airfoil = make_airfoil(x)
    draw(airfoil)


if __name__ == '__main__':
    method = 'TNC'
    if method == 'Nelder-Mead':
        initial_simplex = (0.5 + 1 * np.random.random((len(x0) + 1, len(x0)))) * x0
        res = optimize.minimize(fun=augmented_objective,
          x0=(pack(lower_guess, upper_guess)),
          method=method,
          callback=callback,
          options={'maxiter':1000000, 
         'initial_simplex':initial_simplex})
    elif method == 'TNC':
        res = optimize.minimize(fun=augmented_objective,
          x0=(pack(lower_guess, upper_guess)),
          method=method,
          callback=callback,
          options={'maxiter':1000000, 
         'eps':0.001, 
         'stepmx':0.04})
    final_airfoil = make_airfoil(res.x)