from constants import *
from hp import *
agent             = "RL"
filename          = ""
game_hp           = HP(grid_size = 20, max_iter = 3000, discount = 0.9)
depth             = lambda s,a : survivorDfunc(s, a , 2, 0.5)
num_trials        = 1000
opponents         = []
comment           = ""
