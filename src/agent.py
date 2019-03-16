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

"""
Agent interface
"""

class Agent:
    """
    An agent defined by a strategy.
    """

    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.player_id = None

    def __str__(self):
        return self.name

    def setPlayerId(self, i):
        self.player_id = i

    def getPlayerId(self):
        return self.player_id

    def nextAction(self, state):
        if self.player_id is None:
            raise("Player ID missing")
        return self.strategy(self.player_id, state)

    def lastReward(self, game):
        if self.player_id is None:
            raise("Player ID missing")
        return game.agentLastReward(self.player_id)

    def isAlive(self, game):
        if self.player_id is None:
            raise("Player ID missing")
        return game.isAlive(self.player_id)
