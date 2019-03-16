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
