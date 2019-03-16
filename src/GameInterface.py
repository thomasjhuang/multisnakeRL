import math
import random
from copy import deepcopy
from snake import *
from constants import DIRECTIONS, MOVES, FRUIT_VAL, FRUIT_BONUS

class State:
    """
    State object for the multiplayer snake game.
    Defined by a dictionary {id => snake} and {position => value} for fruits.
    """

    grid_size = None
    num_snakes = 0
    max_iter = None

    def __init__(self, snakes, fruits):
        self.snakes = snakes
        self.fruits = {f.position : f.value for f in fruits}
        self.scores = {}
        self.iter = 0

    def isAlive(self, snake_id):
        """
        Check if snake :snake_id: is still alive.
        """
        return (snake_id in self.snakes)

    def addFruit(self, pos, val, dead_snake=-1):
        """
        Adds a fruit of value val and position pos. If there is already a snake at the position, we don't add it
        :param pos: the position for the fruit as a tuple
        :param val: the value of the fruit
        :return: True if the fruit has been added, False if not
        """
        if all(not s.onSnake(pos) for a, s in self.snakes.items() if a != dead_snake) \
                and not pos in list(self.fruits.keys()):
            self.fruits[pos] = val
            return True
        return False

    def addNRandomFruits(self, n, grid_size):
        while n > 0:
            if self.addFruit(
                    (random.randint(0, grid_size-1), random.randint(0, grid_size-1)),
                    FRUIT_VAL
            ):
                n -= 1

    def onOtherSnakes(self, pos, id):
        return any(s.onSnake(pos) for i,s in self.snakes.items() if i != id)

    def oneAgentUpdate(self, id, m):
        #Remember changes
        snake_who_died = None
        fruits_to_add = []
        fruits_removed = []
        points_won = 0
        last_tail = self.snakes[id].last_tail
        last_pos = []

        # update positions

        accelerated = {}
        # If the snake couldn't move, then it's dead
        if m is None:
            snake_who_died = deepcopy(self.snakes[id])
        else:
            if m.norm() == 2:
                last_pos.append(self.snakes[id].position[-2])
            last_pos.append(self.snakes[id].position[-1])
            new_fruit_pos = self.snakes[id].move(m)

            # We remember where to add fruits when the snake accelerated
            if new_fruit_pos is not None:
               fruits_to_add.append(new_fruit_pos)

            # We collect fruits if head touches a fruit
            head = self.snakes[id].head()
            if head in self.fruits:
                points_won += self.fruits.get(head)
                fruits_removed.append((head, self.fruits.get(head)))
                self.snakes[id].addPoints(self.fruits.get(head))
                del self.fruits[head]

            # If the snake accelerated, we check if the second part of the body touches a fruit
            if m.norm() == 2:
                accelerated[id] = True
                second = self.snakes[id].position[1]
                if second in self.fruits:
                    points_won += self.fruits.get(second)
                    fruits_removed.append((second, self.fruits.get(second)))
                    self.snakes[id].addPoints(self.fruits.get(second))
                    del self.fruits[second]
            else:
                accelerated[id] = False

        # add fruits created by acceleration
        for cand_pos in fruits_to_add:
            self.addFruit(cand_pos, FRUIT_VAL)

        # remove snakes which bumped into other snakes
        # list of (x,y) points occupied by other snakes
        if snake_who_died is None and (self.onOtherSnakes(self.snakes[id].position[0], id)\
                or (accelerated[id] and self.onOtherSnakes(self.snakes[id].position[1], id))\
                or not utils.isOnGrid(self.snakes[id].position[0], self.grid_size)):
            snake_who_died = deepcopy(self.snakes[id])


        if snake_who_died is not None:
            # add fruits on the snake position before last move
            self.snakes[id].popleft()
            for p in self.snakes[id].position:
                if self.addFruit(p, FRUIT_BONUS, dead_snake=id):
                    fruits_to_add.append(p)
            # print "Snake {} died with {} points".format(id, self.snakes[id].points)
            del self.snakes[id]

        return last_pos, id, fruits_to_add, fruits_removed, points_won, last_tail, snake_who_died

    def reverseChanges(self, changes):
        last_pos, id, fruits_added, fruits_removed, points_won, last_tail, snake_who_died = changes
        if snake_who_died is not None:
            self.snakes[id] = snake_who_died
        self.snakes[id].removePoints(points_won)
        self.snakes[id].backward(last_pos, last_tail)
        for c in set(fruits_added):
            del self.fruits[c]
        for c, val in fruits_removed:
            self.addFruit(c, val)


    def update(self, moves):
        """
        `moves` is a dict {snake_id => move}
        Update the positions/points of every snakes and check for collisions.
        """
        self.iter += 1

        deads = []

        # update positions
        fruits_to_add = []
        accelerated = {}
        for id, m in moves.items():
            # If the snake couldn't move, then it's dead
            if m is None or not self.snakes[id].authorizedMove(m):
                deads.append(id)
                continue

            new_fruit_pos = self.snakes[id].move(m)

            # We remember where to add fruits when the snake accelerated
            if new_fruit_pos is not None:
               fruits_to_add.append(new_fruit_pos)

            # We collect fruits if head touches a fruit
            head = self.snakes[id].head()
            if head in self.fruits:
                self.snakes[id].addPoints(self.fruits.get(head))
                del self.fruits[head]

            # If the snake accelerated, we check if the second part of the body touches a fruit
            if m.norm() == 2:
                accelerated[id] = True
                second = self.snakes[id].position[1]
                if second in self.fruits:
                    self.snakes[id].addPoints(self.fruits.get(second))
                    del self.fruits[second]
            else:
                accelerated[id] = False

        # add fruits created by acceleration
        for cand_pos in fruits_to_add:
            self.addFruit(cand_pos, FRUIT_BONUS)

        # remove snakes which bumped into other snakes

        for id in list(moves.keys()):
            # list of (x,y) points occupied by other snakes
            if not id in deads and (self.onOtherSnakes(self.snakes[id].position[0], id)\
                    or (accelerated[id] and self.onOtherSnakes(self.snakes[id].position[1], id))\
                    or not utils.isOnGrid(self.snakes[id].position[0], self.grid_size)):
                deads.append(id)

        # save scores and add fruits
        rank = len(self.snakes)
        for id in deads:
            self.scores[id] = (rank, self.snakes[id].points)
            # add fruits on the snake position before last move
            for p in self.snakes[id].position:
                self.addFruit(p, FRUIT_BONUS, dead_snake=id)
            # print "Snake {} died with {} points".format(id, self.snakes[id].points)
            del self.snakes[id]

        if len(self.snakes) == 1:
            winner = list(self.snakes.keys())[0]
            self.scores[winner] = (1, self.snakes[winner].points)

        return self

    def isWin(self, agent):
        return len(self.snakes) == 1 and agent in list(self.snakes.keys())

    def isLose(self, agent):
        return len(self.snakes) >= 1 and agent not in list(self.snakes.keys())

    def isDraw(self):
        return len(self.snakes) == 0

    def timesUp(self):
        return self.iter == self.max_iter

    def getNextAgent(self, agent, agents=None):
        if agents is None:
            agents = list(self.snakes.keys())
        else:
            agents = set(agents).intersection(set(list(self.snakes.keys())))
        for i in range(1, self.num_snakes+1):
            next_snake = (agent+i) % self.num_snakes
            if next_snake in agents:
                return next_snake
        return agent

    def generateSuccessor(self, agent, move):
        return self.oneAgentUpdate(agent, move)

    def getScore(self, agent):
        if self.isDraw():
            return -1*(self.grid_size ** 2) * FRUIT_BONUS + 1
        if self.isWin(agent):
            return (self.grid_size ** 2) * FRUIT_BONUS
        if self.timesUp():
            return self.snakes[agent].points
        if self.isLose(agent) or len(self.actions(agent)) == 0:
            return -1*(self.grid_size ** 2) * FRUIT_BONUS
        return self.snakes[agent].points

    def currentScore(self, player):
        """
        Get the adjusted score for `player`: points/rank
        """
        s = self.scores.get(player)
        if s is None:
            return self.snakes[player].points / float(len(self.snakes))
        else:
            rank, points = s
            return points / float(rank)

    def actions(self, player):
        """
        List of possible actions for `player`.
        """
        snake = self.snakes.get(player)
        head = snake.position[0]
        return [m for m in MOVES
                if utils.isOnGrid(m.apply(head), self.grid_size)
                and snake.authorizedMove(m)]

    def simple_actions(self, player):
        """
        List of possible actions for `player`.
        """
        snake = self.snakes.get(player)
        head = snake.position[0]
        return [m for m in MOVES if m.norm() == 1
                and utils.isOnGrid(m.apply(head), self.grid_size)
                and snake.authorizedMove(m, possibleNorm=[1])]

    def all_actions(self, player):
        """
        List of all actions for `player`.
        """
        return [m for m in MOVES if m.norm() == 1]

    def all_rel_actions(self, player):
        """
        List of all relative actions for `player` (backwards move are excluded).
        """
        return [m for m in MOVES if m.norm() == 1 and m.direction() != (0,-1)]


class Game:
    def __init__(self, grid_size, num_snakes = 2, fruit_ratio = 1, max_iter = None):
        self.grid_size = grid_size
        self.num_snakes = num_snakes
        self.fruit_ratio = fruit_ratio
        self.max_iter = max_iter
        self.current_state = None
        self.previous_state = None
        self.agents = []

        # Update static variables of State
        State.grid_size = grid_size
        newSnake.grid_size = grid_size
        State.num_snakes = num_snakes
        State.max_iter = max_iter

    def startingState(self):
        """
        Divides the map into equally size squares before randomly assigning each snake to a spawn square. Snake spawn are
        guaranteed to be valid. Randomly spawns fruit_ratio fruits for each snake.
        Returns
        -------
        start_state : State
            State object representing the valid starting state of the game
        """

        # Ensuring that we can create enough square spawn sections of equal size to accomdate all snakes
        num_spawn_sections_row = int(math.ceil(math.sqrt(self.num_snakes))**2)
        spawn_section_size = self.grid_size // int(num_spawn_sections_row)
        # Assign snakes to spawn sections
        snake_assignment = random.sample(range(num_spawn_sections_row ** 2), self.num_snakes)

        assert self.grid_size >= 3*num_spawn_sections_row, "Map Grid is too small to guarantee all snakes will be spawned without overlap"

        snakes = {}
        for snake, assign in enumerate(snake_assignment):
            ''' Randomly chose a point for the head in the assigned spawn section that is at least 2 away from the 
            boundaries of the section to ensure that a snake of length 2 will not exceeed the section's boundaries '''
            head = (random.randint(1, spawn_section_size - 2) + (assign // num_spawn_sections_row) * spawn_section_size,
                    random.randint(1, spawn_section_size - 2) + (assign % num_spawn_sections_row) * spawn_section_size)
            # Create new snake with head at chosen location of length 2 with random starting direction
            snakes[snake] = newSnake([head, utils.add(head, random.sample(DIRECTIONS, 1)[0])], snake)

        start_state = State(snakes, {})
        # Randomly spawn fruit_ratio fruits for each snake
        start_state.addNRandomFruits(self.fruit_ratio * self.num_snakes, self.grid_size)
        return start_state


    def start(self, agents):
        """
        Creates a valid starting state for the game and performs necessary assignments
        Parameters
        ----------
        agents : List[Agent]
            List of Agent objects to be applied to snakes
        Returns
        -------
        current_state : State
            State object representing the current state of the game
        """
        self.current_state = self.startingState()
        self.agents = agents
        for i, agent in enumerate(self.agents):
            agent.setPlayerId(i)
        return self.current_state

    def isEnd(self, state = None):
        if state is None:
            state = self.current_state
        if self.max_iter:
            return len(state.snakes) <= 1 or state.iter == self.max_iter
        else:
            return len(state.snakes) <= 1

    def isAlive(self, agent_id):
        return self.current_state.isAlive(agent_id)

    def agentActions(self):
        return {i: self.agents[i].nextAction(self.current_state) for i in list(self.current_state.snakes.keys())}

    def tick(self, state, actions, copy=True):
        if copy:
            newState = deepcopy(state)
        else:
            newState = state
        self.previous_state = state
        newState.update(actions)
        rand_pos = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
        newState.addFruit(rand_pos, FRUIT_VAL)
        self.current_state = newState
        return newState

    def agentLastReward(self, agent_id):
        if agent_id in self.current_state.snakes:
            reward = self.current_state.snakes[agent_id].points - self.previous_state.snakes[agent_id].points
            if len(self.current_state.snakes) == 1: # it won
                reward += 10.
        else: # it died
            reward = - 10.
        return reward



