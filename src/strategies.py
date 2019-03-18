"""
Strategies for players.
"""
from operator import itemgetter
from utils import *
import random

def humanStrategy(id, state):
    return None

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
    best_move = min(((dist(move.apply(head), fruit), move)
                    for fruit in state.fruits.keys() for move in actions), key=itemgetter(0))
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

    min_dist = dict(((fruit, min(dist(s.position[0], fruit) for s in state.snakes.values()))
                    for fruit in state.fruits.keys()), key=itemgetter(1))
    best_move = min(((dist(snake.predictHead(move), fruit) - min_dist[fruit],
                     dist(snake.predictHead(move), fruit), move)
                    for fruit in state.fruits.keys() for move in actions), key=itemgetter(0))
    return best_move[2]

def simpleHillClimbingStrategy(id, state):
    snake = state.snakes[id]
    # Get list of possible actions that do not result in collisions with other snakes
    actions = [move for move in state.simple_actions(id) if not state.onOtherSnakes(snake.predictHead(move), id)]

    # If all possible actions result in collisions, then simply return None
    if len(actions) == 0:
        return None
    # If there are no fruits left, move randomly
    if len(state.fruits) == 0:
        return random.sample(actions, 1)[0]
    # Choose the move that results in the greatest reduction in distance to a fruit
    best_move = min(((dist(snake.predictHead(move), fruit), move) for fruit in state.fruits.keys() for move in actions), key=itemgetter(0))
    return best_move[1]

def weightedHillClimbingStrategy1(id, state):
    snake = state.snakes[id]
    otherSnakes = []
    for x in list(state.snakes.keys()):
        if x != id:
            otherSnakes.append(state.snakes[x])
    # If there are no other snakes alive, the game is over, so return None
    if len(otherSnakes) == 0:
        return None
    # Get list of possible actions that do not result in collisions with other snakes
    actions = [move for move in state.simple_actions(id) if not state.onOtherSnakes(snake.predictHead(move), id)]

    # If all possible actions result in collisions, then simply return None
    if len(actions) == 0:
        return None
    # If there are no fruits left, move randomly
    if len(state.fruits) == 0:
        return random.sample(actions, 1)[0]
    # Choose the move that results in the greatest reduction in distance to a fruit
    minScore = (state.grid_size + 1) * 2
    minAction = None
    for action in actions:
        closestSnakeDist = min(dist(snake.predictHead(action), s.position[0]) for s in otherSnakes)
        closestFruitDist = min(dist(snake.predictHead(action), fruit) for fruit in state.fruits.keys())
        currentScore = closestFruitDist - closestSnakeDist
        if minScore > currentScore:
            minScore = currentScore
            minAction = action
    return minAction

def weightedHillClimbingStrategyPoint5(id, state):
    snake = state.snakes[id]
    otherSnakes = []
    for x in list(state.snakes.keys()):
        if x != id:
            otherSnakes.append(state.snakes[x])
    # If there are no other snakes alive, the game is over, so return None
    if len(otherSnakes) == 0:
        return None
    # Get list of possible actions that do not result in collisions with other snakes
    actions = [move for move in state.simple_actions(id) if not state.onOtherSnakes(snake.predictHead(move), id)]

    # If all possible actions result in collisions, then simply return None
    if len(actions) == 0:
        return None
    # If there are no fruits left, move randomly
    if len(state.fruits) == 0:
        return random.sample(actions, 1)[0]
    # Choose the move that results in the greatest reduction in distance to a fruit
    minScore = 999999
    minAction = None
    for action in actions:
        closestSnakeDist = min(dist(snake.predictHead(action), s.head()) for s in otherSnakes)
        closestFruitDist = min(dist(snake.predictHead(action), fruit) for fruit in state.fruits.keys())
        currentScore = closestFruitDist - (closestSnakeDist) * 0.5
        if minScore > currentScore:
            minScore = currentScore
            minAction = action
    return minAction

def weightedHillClimbingStrategyPoint33(id, state):
    snake = state.snakes[id]
    otherSnakes = []
    for x in list(state.snakes.keys()):
        if x != id:
            otherSnakes.append(state.snakes[x])
    # If there are no other snakes alive, the game is over, so return None
    if len(otherSnakes) == 0:
        return None
    # Get list of possible actions that do not result in collisions with other snakes
    actions = [move for move in state.simple_actions(id) if not state.onOtherSnakes(snake.predictHead(move), id)]

    # If all possible actions result in collisions, then simply return None
    if len(actions) == 0:
        return None
    # If there are no fruits left, move randomly
    if len(state.fruits) == 0:
        return random.sample(actions, 1)[0]
    # Choose the move that results in the greatest reduction in distance to a fruit
    minScore = 999999
    minAction = None
    for action in actions:
        closestSnakeDist = min(dist(snake.predictHead(action), s.head()) for s in otherSnakes)
        closestFruitDist = min(dist(snake.predictHead(action), fruit) for fruit in state.fruits.keys())
        currentScore = closestFruitDist - (closestSnakeDist) * 0.33
        if minScore > currentScore:
            minScore = currentScore
            minAction = action
    return minAction