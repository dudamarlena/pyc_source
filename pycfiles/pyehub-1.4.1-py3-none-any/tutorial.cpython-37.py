# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/pylp/tutorial.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 2658 bytes
__doc__ = '\nThis file serves as a tutorial/example of using PyLP.\n\nTo run the file from the root directory of this project, do\n\n    python3.6 -m pylp.tutorial\n\nThis is because this tutorial is inside the package it is using.\n'
import pylp
from pylp import RealVariable, IntegerVariable

def main():
    """The main function of the tutorial.

    For this tutorial, we will be finding a selection of candy that minimizes
    our costs but we get at least 400 grams of sugar.
    """
    sugar_amount = 400
    sweets = [
     'Chocolate Bar', 'Lollipop', 'Ice Cream']
    sugar_per_sweet = {'Chocolate Bar':40, 
     'Lollipop':20, 
     'Ice Cream':0.2}
    cost_per_sweet = {'Chocolate Bar':2.4, 
     'Lollipop':1.2, 
     'Ice Cream':0.02}
    amount_per_sweet = {'Chocolate Bar':IntegerVariable(), 
     'Lollipop':IntegerVariable(), 
     'Ice Cream':RealVariable()}
    total_cost = sum((cost_per_sweet[sweet] * amount_per_sweet[sweet] for sweet in sweets))
    sugar_constraint = sum((sugar_per_sweet[sweet] * amount_per_sweet[sweet] for sweet in sweets)) >= sugar_amount
    amount_constraints = [amount_per_sweet[sweet] >= 0 for sweet in sweets]
    constraints = [
     sugar_constraint] + amount_constraints
    status = pylp.solve(objective=total_cost, constraints=constraints, minimize=True,
      solver='glpk')
    print(f"Terminated in {status.time}s with a(n) {status.status} solution/problem")
    for sweet in sweets:
        print(f"Amount of {sweet}: {amount_per_sweet[sweet].evaluate()}")

    print(f"Total Cost: {total_cost.evaluate()}")


if __name__ == '__main__':
    main()