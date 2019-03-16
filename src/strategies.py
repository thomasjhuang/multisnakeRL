"""
Strategies for players.
"""
from operator import itemgetter
from utils import *
import random

def randomStrategy(id, state):
    """
    Takes random actions
    """
    actions = state.actions(id)
    if len(actions) == 0:
        return None
    return random.sample(actions, 1)[0]


def greedyStrategy(id, state):
    """
    Take action which brings us closest to a fruit - without even
    looking at other snakes.
    """
    actions = state.simple_actions(id)
    head = state.snakes[id].position[0]
    if len(actions) == 0:
        return None
    if len(state.fruits) == 0:
        return random.sample(actions, 1)[0]

    best_move = min(((dist(move.apply(head), fruit), move) for fruit in list(state.fruits.keys()) for move in actions), key=itemgetter(0))
    return best_move[1]

def smartGreedyStrategy(id, state):
    """
    Take action which brings us closest to a fruit
    Checks if we're hitting another snake
    """
    snake = state.snakes[id]
    # Computing the list of actions that won't kill the snake
    actions = [move for move in state.simple_actions(id) if not state.onOtherSnakes(snake.predictHead(move), id)]

    # If it is empty, then the snake will die and we move randomly
    if len(actions) == 0:
        return None

    # If there is no fruit we move randomly
    if len(state.fruits) == 0:
        return random.sample(actions, 1)[0]
    '''
    vals = []
    for fruit in list(state.fruits.keys()):
        for move in actions:
            vals.append(dist(snake.predictHead(move), fruit)))
    print('type: ' + type(vals[0]))
    '''

    best_move = min(((dist(snake.predictHead(move), fruit), move)
                    for fruit in list(state.fruits.keys()) for move in actions), key = lambda t: t[0])
    return best_move[1]

def opportunistStrategy(id, state):
    """
    Take action which brings us closest to a fruit
    Checks if we're hitting another snake
    """
    snake = state.snakes[id]
    # Computing the list of actions that won't kill the snake
    actions = [m for m in state.simple_actions(id)
               if not state.onOtherSnakes(snake.predictHead(m), id)]

    # If it is empty, then the snake will die and we move randomly
    if len(actions) == 0:
        return None

    # If there is no fruit we move randomly
    if len(state.fruits) == 0:
        return random.sample(actions, 1)[0]

    min_dist = dict((fruit, min(dist(s.position[0], fruit) for s in list(state.snakes.values())))
                    for fruit in state.fruits.keys())
    best_move = min(((dist(snake.predictHead(move), fruit) - min_dist[fruit], dist(snake.predictHead(move), fruit), move)
                    for fruit in list(state.fruits.keys()) for move in actions), key = lambda t: t[0])
    return best_move[2]


def humanStrategy(id, state):
    return None
