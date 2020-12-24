# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dinolemma/gui.py
# Compiled at: 2020-01-24 17:17:23
# Size of source mod 2**32: 5997 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from dinolemma.colors import BLACK, WHITE, GREEN, PURPLE, LIGHT_PURPLE, YELLOW
from dinolemma.game import DinosaurDilemma
import sys
try:
    import pygame
except:
    sys.exit('You must install pygame to use the game interface.')

def text_objects(text, font, color=WHITE):
    """return a text surface and surrounding rectangle
    """
    textSurface = font.render(text, True, color)
    return (textSurface, textSurface.get_rect())


def show_text(lines, screen, x, y, font_size=30, color=WHITE):
    """Given one or more lines of text, print to screen at center x,y
    """
    if isinstance(lines, str):
        lines = [
         lines]
    largeText = pygame.font.Font('freesansbold.ttf', font_size)
    for line in lines:
        TextSurf, TextRect = text_objects(line, largeText, color)
        TextRect.center = (x, y)
        screen.blit(TextSurf, TextRect)
        y += font_size


def button(message, screen, x_topleft, y_topleft, width, height, inactive_color=GREEN, active_color=YELLOW, font_color=BLACK, font_size=20):
    """Add a button to the game.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    clicked = False
    if x_topleft + width > mouse[0] > x_topleft:
        if y_topleft + height > mouse[1] > y_topleft:
            pygame.draw.rect(screen, active_color, (x_topleft, y_topleft, width, height))
            if click[0] == 1:
                clicked = True
            else:
                pygame.draw.rect(screen, inactive_color, (x_topleft, y_topleft, width, height))
    smallText = pygame.font.Font('freesansbold.ttf', font_size)
    textSurf, textRect = text_objects(message, smallText, font_color)
    textRect.center = (x_topleft + width / 2, y_topleft + height / 2)
    screen.blit(textSurf, textRect)
    return clicked


def run_game(grid_size=25, number_trees=None, number_dinos=None, grid_dim=30):
    """run the gui game. Currently, parameters are hard set to ensure that
       dimensions work out okay. This could be modified to be more dynamic

       Parameters
       ==========
       grid_dim: the width and height of a square in the grid
    """
    WIDTH = HEIGHT = grid_dim
    MARGIN = 5
    TEXT_AREA = 200
    simulation = DinosaurDilemma(grid_size=grid_size,
      number_trees=number_trees,
      number_dinos=number_dinos)
    pygame.init()
    SIZE = grid_size * (WIDTH + MARGIN) + MARGIN
    WINDOW_SIZE = [SIZE, SIZE + TEXT_AREA]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Dinosaur Dilemma')
    summary = simulation.summary(return_summary=True).split('\n')
    show_text(summary, screen, SIZE / 2, SIZE + 10)
    pygame.display.flip()
    done = False
    clock = pygame.time.Clock()

    def update_grid(screen, simulation):
        screen.fill(BLACK)
        for row in range(simulation.grid_size):
            for column in range(simulation.grid_size):
                color = WHITE
                if simulation.grid[row][column] is not None:
                    if simulation.grid[row][column].endswith('tree'):
                        color = GREEN
                    else:
                        color = PURPLE
                pygame.draw.rect(screen, color, [
                 (MARGIN + WIDTH) * column + MARGIN,
                 (MARGIN + HEIGHT) * row + MARGIN,
                 WIDTH,
                 HEIGHT])

        summary = simulation.summary(return_summary=True).split('\n')
        show_text(summary, screen, SIZE / 2, SIZE + 30)
        show_text([
         'Click to progress to next day...'],
          screen,
          (SIZE / 2),
          (SIZE + 150),
          color=LIGHT_PURPLE)
        clicked = button('Reset',
          screen,
          x_topleft=10,
          y_topleft=(SIZE + TEXT_AREA - 70),
          width=100,
          height=50)
        if clicked:
            simulation = DinosaurDilemma(grid_size=grid_size,
              number_trees=number_trees,
              number_dinos=number_dinos)
        clock.tick(60)
        pygame.display.flip()
        return simulation

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    simulation.run_day()
            simulation = update_grid(screen, simulation)

    pygame.quit()