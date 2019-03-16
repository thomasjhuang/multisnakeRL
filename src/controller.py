'''
MIT License

Copyright (c) 2018 Sebastien Dubois, Sebastien Levy, Felix Crevier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys, pickle
import pygame
import gui, move, config
from GameInterface import Game,Snake
from strategies import randomStrategy, humanStrategy
from features import FeatureExtractor
from pdb import set_trace as t
from constants import *

def controller(strategies, grid_size, fruit_ratio = 1., max_iter = None, verbose = 0, gui_active = False, game_speed = None):
    # Pygame Init
    pygame.init()
    clock = pygame.time.Clock()
    if gui_active:
        gui_options = gui.Options()
        win = gui.Window(grid_size,'Multiplayer Snake', gui_options)
        quit_game = False

    # Start Game
    game = Game(grid_size, len(strategies), fruit_ratio = fruit_ratio, max_iter = max_iter)
    # state = game.startState()
    state = game.start(strategies)
    prev_human_action = None
    game_over = False

    agent_names = [a.name for a in strategies]
    i_human = None
    if "human" in agent_names:
        i_human = agent_names.index("human")

    while not ((gui_active and quit_game) or ((not gui_active) and game_over)):
        # Print state
        #if verbose > 0:
            #state.printGrid(game.grid_size)
        # Get events
        if gui_active:
            events = pygame.event.get()
            if pygame.QUIT in [ev.type for ev in events]:
                quit_game = True
                continue

        # Compute the actions for each player following its strategy (except human)
        actions = game.agentActions()

        # Compute human strategy if necessary
        human_action = None
        if i_human is not None:
            speed = 2. if pygame.K_SPACE in [ev.key for ev in events if ev.type == pygame.KEYDOWN] else 1.
            arrow_key = False
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        human_action = move.Move((-1,0),speed)
                        arrow_key = True
                    if event.key == pygame.K_RIGHT:
                        human_action = move.Move((1,0),speed)
                        arrow_key = True
                    if event.key == pygame.K_UP:
                        human_action = move.Move((0,-1),speed)
                        arrow_key = True
                    if event.key == pygame.K_DOWN:
                        human_action = move.Move((0,1),speed)
                        arrow_key = True

            if not arrow_key and prev_human_action is None:
                human_action = move.Move((0,-1),speed)
            elif not arrow_key:
                human_action = prev_human_action

        # Assign human action
        if i_human is not None and i_human in list(actions.keys()):
            actions[i_human] = human_action
            prev_human_action = human_action

        #if verbose > 1:
            #print(state)
            #print(actions)

        # Update the state
        if not game_over:
            state = game.tick(state, actions, copy = False)
        # Pause
        if game_speed:
            clock.tick(game_speed)

        # Check if game over
        game_over = game.isEnd(state)
        # if game_over:
           # win.print_message('GAME OVER')

        # Update gui
        if gui_active:
            win.updateSprites(state)
            win.refresh()

    #if verbose > 0:
        #state.printGrid(game.grid_size)

    return state

if __name__ ==  "__main__":
    human_player = False
    if len(sys.argv) > 1 and sys.argv[1] == "h":
        human_player = True
    max_iter = None
    strategies = [RandomAgent, HumanAgent]

    if human_player:
        strategies.append(HumanAgent)

    controller(strategies, 40, max_iter = max_iter, gui_active = True, verbose = 0, game_speed = 10)
