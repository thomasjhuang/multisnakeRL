from constants import *
from hp import *
agent             = "simplestrategies"
filename          = "nonrlrun"
game_hp           = HP(grid_size = 20, max_iter = 30, discount = 0.9)
depth             = lambda s,a : survivorDfunc(s, a , 2, 0.5)
num_trials        = 10
opponents         = [SmartGreedyAgent, OpportunistAgent, RandomAgent, GreedyAgent]
comment           = ""
