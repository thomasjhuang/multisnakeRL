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

import utils

class Move:
    """
    Move object including norm and direction
    """

    def __init__(self, direction, norm=1):
        self.dir = direction
        self.n = norm

    def norm(self):
        return self.n

    def direction(self):
        return self.dir

    def apply(self, point):
        return utils.add(point, self.direction(), mu=self.norm())

    def applyDirection(self, point, mu=1):
        return utils.add(point, self.direction(), mu=mu)

    def __repr__(self):
        return str(self.dir)
        #return "({}, {})".format(self.dir, self.norm)
