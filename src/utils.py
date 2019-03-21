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

import sys
import numpy as np

"""
Utils
"""

def softmax(x):
    """ Compute softmax values for each sets of scores in x """
    e_x = np.exp(x - np.max(x)) # subtract max(x) for stability
    return e_x / e_x.sum(axis = 0)

def add(tuple1, tuple2, mu = 1):
    """
    Return tuple1 + mu * tuple2.
    """
    return tuple([tuple1[i] + mu * tuple2[i] for i in range(len(tuple1))])

def mult(t, mu):
    return tuple([x * mu for x in t])

def dist(tuple1, tuple2):
    """Manhattan distance"""
    return abs(tuple1[0] - tuple2[0]) + abs(tuple1[1] - tuple2[1])

def norm1(tuple):
    """Norm 1"""
    return dist(tuple, tuple)

def rotate(p, dir):
    """Rotate position `p` in relative coordinates when snake has direction `dir`"""

    if dir == (0,-1):
        return mult(p, -1)
    elif dir == (1,0):
        return (-p[1], p[0])
    elif dir == (-1,0):
        return (p[1], - p[0])
    else:
        return p

def rotateBack(p, dir):
    """Rotate position `p` in aboslute coordinates when snake has direction `dir`"""

    if dir == (0,-1):
        return mult(p, -1)
    elif dir == (1,0):
        return (p[1], - p[0])
    elif dir == (-1,0):
        return (- p[1], p[0])
    else:
        return p

def isOnGrid(p, grid_size):
    """
    Check if position `p` is valid for the grid.
    """
    return p[0] >= 0 and p[1] >= 0 and p[0] < grid_size and p[1] < grid_size

def progressBar(iteration, n_total, size = 50, info = None):
    size = min(size, n_total)
    if iteration % (n_total/size) == 0:
        sys.stdout.write('\r')
        i = int(iteration*size//n_total)
        if info is not None:
            sys.stdout.write("[<{}>] {}% | {}".format('='*i, ' '*(size-i), (100//size)*i, info))
        else:
            sys.stdout.write("[<{}>{}] {}%".format('='*i, ' '*(size-i), (100//size)*i))
        sys.stdout.flush()
    if iteration == n_total:
        print("")
