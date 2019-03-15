import pickle
class HP:
    def __init__(self, grid_size, max_iter, discount):
        self.grid_size = grid_size
        self.max_iter = max_iter
        self.discount = discount

    def __str__(self):
        return " | ".join(["{} = {}".format(k,v) for k,v in self.__dict__.iteritems()])
