# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/penkit/turtle.py
# Compiled at: 2017-12-27 16:46:32
# Size of source mod 2**32: 4409 bytes
"""The ``turtle`` module contains a basic implementation of turtle graphics.

The turtle language also includes a "branching" extension that allows the
turtle to return to a previously remembered state.
"""
import numpy as np
DEFAULT_TURN = 45.0
DEFAULT_INITIAL_ANGLE = 90.0
VISIBLE_FORWARD_COMMANDS = set('ABCDEFGHIJ')
FORWARD_COMMANDS = VISIBLE_FORWARD_COMMANDS | set('abcdefghij')
CW_TURN_COMMAND = '+'
CCW_TURN_COMMAND = '-'
PUSH_STATE_COMMAND = '['
POP_STATE_COMMAND = ']'

def branching_turtle_generator(turtle_program, turn_amount=DEFAULT_TURN, initial_angle=DEFAULT_INITIAL_ANGLE, resolution=1):
    """Given a turtle program, creates a generator of turtle positions.
    
    The state of the turtle consists of its position and angle.
    The turtle starts at the position ``(0, 0)`` facing up. Each character in the
    turtle program is processed in order and causes an update to the state.
    The position component of the state is yielded at each state change. A
    ``(nan, nan)`` separator is emitted between state changes for which no line
    should be drawn.

    The turtle program consists of the following commands:

    - Any letter in ``ABCDEFGHIJ`` means "move forward one unit and draw a path"
    - Any letter in ``abcdefghij`` means "move forward" (no path)
    - The character ``-`` means "move counter-clockwise"
    - The character ``+`` means "move clockwise"
    - The character ``[`` means "push a copy of the current state to the stack"
    - The character ``]`` means "pop a state from the stack and return there"
    - All other characters are silently ignored (this is useful when producing
      programs with L-Systems)
    
    Args:
        turtle_program (str): a string or generator representing the turtle program
        turn_amount (float): how much the turn commands should change the angle
        initial_angle (float): if provided, the turtle starts at this angle (degrees)
        resolution (int): if provided, interpolate this many points along each visible
            line

    Yields:
        pair: The next coordinate pair, or ``(nan, nan)`` as a path separator.
    """
    saved_states = list()
    state = (0, 0, DEFAULT_INITIAL_ANGLE)
    yield (0, 0)
    for command in turtle_program:
        x, y, angle = state
        if command in FORWARD_COMMANDS:
            new_x = x - np.cos(np.radians(angle))
            new_y = y + np.sin(np.radians(angle))
            state = (new_x, new_y, angle)
            if command not in VISIBLE_FORWARD_COMMANDS:
                yield (
                 np.nan, np.nan)
                yield (state[0], state[1])
            else:
                dx = new_x - x
                dy = new_y - y
                for frac in 1 - np.flipud(np.linspace(0, 1, resolution, False)):
                    yield (
                     x + frac * dx, y + frac * dy)

        elif command == CW_TURN_COMMAND:
            state = (
             x, y, angle + turn_amount)
        else:
            if command == CCW_TURN_COMMAND:
                state = (
                 x, y, angle - turn_amount)
            else:
                if command == PUSH_STATE_COMMAND:
                    saved_states.append(state)
                else:
                    if command == POP_STATE_COMMAND:
                        state = saved_states.pop()
                        yield (np.nan, np.nan)
                        x, y, _ = state
                        yield (x, y)


def texture_from_generator(generator):
    """Convert a generator into a texture.

    Args:
        generator (generator): a generator of coordinate pairs

    Returns:
        texture: A texture.
    """
    return np.array(list(zip(*list(generator))))


def turtle_to_texture(turtle_program, turn_amount=DEFAULT_TURN, initial_angle=DEFAULT_INITIAL_ANGLE, resolution=1):
    """Makes a texture from a turtle program.

    Args:
        turtle_program (str): a string representing the turtle program; see the
            docstring of `branching_turtle_generator` for more details
        turn_amount (float): amount to turn in degrees
        initial_angle (float): initial orientation of the turtle
        resolution (int): if provided, interpolation amount for visible lines

    Returns:
        texture: A texture.
    """
    generator = branching_turtle_generator(turtle_program, turn_amount, initial_angle, resolution)
    return texture_from_generator(generator)