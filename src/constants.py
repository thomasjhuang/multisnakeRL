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

from move import Move
from agent import Agent
from strategies import *

# global variables
ACCELERATION = False
DIRECTIONS = [(1,0), (0,1), (-1,0), (0,-1)]      # authorized moves
NORM_MOVES = [1]
if ACCELERATION:
    NORM_MOVES.append(2)                    # acceleration moves
MOVES = [Move(dir, norm) for dir in DIRECTIONS for norm in NORM_MOVES]
NO_MOVE = Move(direction = (0,0), norm = 0)
FRUIT_VAL = 1                               # default fruit value
FRUIT_BONUS = 3                             # fruit value for dead snakes

RandomAgent = Agent(name = "RandomAgent", strategy = randomStrategy)
HumanAgent = Agent(name = "human", strategy = humanStrategy)
SimpleHC = Agent(name = "SimpleHC", strategy=simpleHillClimbingStrategy)
WeightedHC1 = Agent(name = "WeightedHC1", strategy=weightedHillClimbingStrategy1)
WeightedHCPoint5 = Agent(name = "WeightedHCPoint5", strategy=weightedHillClimbingStrategyPoint5)
WeightedHCPoint33 = Agent(name = "WeightedHCPoint33", strategy=weightedHillClimbingStrategyPoint33)
GreedyAgent = Agent(name = "GreedyAgent", strategy = greedyStrategy)
OpportunistAgent = Agent(name = "OpportunistAgent", strategy = opportunistStrategy)

