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

def humanStrategy(id, state):
    return None

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
        currentScore = closestFruitDist + closestSnakeDist
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
        currentScore = closestFruitDist + (closestSnakeDist) * 0.5
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
        currentScore = closestFruitDist + (closestSnakeDist) * 0.33
        if minScore > currentScore:
            minScore = currentScore
            minAction = action
    return minAction
