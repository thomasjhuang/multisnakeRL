import sys
import numpy as np
from time import sleep, time

import config
from hp import *
from utils import progressBar
from controller import controller
from strategies import randomStrategy, greedyStrategy, smartGreedyStrategy, opportunistStrategy
from features import FeatureExtractor

def simulate(n_simul, agents, grid_size, candy_ratio = 1., max_iter = 500):
    print("Simulations")
    wins = dict((id, 0.) for id in range(len(agents)))
    points = dict((id, []) for id in range(len(agents)))
    scores = dict((id, []) for id in range(len(agents)))

    iterations = []
    for it in range(n_simul):
        progressBar(it, n_simul)
        endState = controller(agents, grid_size, candy_ratio = candy_ratio, max_iter = max_iter, verbose = 0)
        if len(endState.snakes) == 1:
            wins[list(endState.snakes.keys())[0]] += 1. / n_simul
            points[list(endState.snakes.keys())[0]].append(list(endState.snakes.values())[0].points)

        for id in range(len(agents)):
            scores[id].append(endState.scores[id])

        iterations.append(endState.iter)
    progressBar(n_simul, n_simul)
    points = dict((id, sum(val)/len(val)) for id,val in points.items())
    return wins, points, scores, iterations


if __name__ ==  "__main__":
    MAX_ITER = 1000

    if len(sys.argv) > 1:
        n_simul = int(sys.argv[1])
    else:
        n_simul = 1000

    print("Simulation config:", ["{} = {}".format(k,v) for k,v in config.__dict__.items() if not k.startswith('__')])

    strategies = config.opponents
    game_hp = config.game_hp

    start = time()
    wins, points, scores, iterations = simulate(n_simul, strategies, game_hp.grid_size, max_iter = MAX_ITER)
    tot_time = time() - start

    with open("experiments/{}_{}_{}.txt".format(config.filename, "-".join([s.__str__() for s in strategies]), config.comment), "w") as fout:
        print("\n\n=======Results=======", file=fout)
        print("Run {} simulations".format(n_simul), file=fout)
        print("Max iteration:", MAX_ITER, "\n", file=fout)

        for i in range(len(strategies)):
            print("\t Snake {} ({}) wins {:.2f}% of the games, with {:.2f} points on average".format(i, strategies[i].name, wins[i]*100, points[i]), file=fout)
            print("\t Snake {} ({}) wins {:.2f}% of the games, with {:.2f} points on average".format(i, strategies[i].name, wins[i]*100, points[i]), file=fout)
        print("\nScores", file=fout)
        print("\nScores")
        for i in range(len(strategies)):
            print("\t Snake {} ({}): avg score = {:.2f}, finishes with {:.2f} points on average".format(i, strategies[i].name, np.mean([p/r for r,p in scores[i]]), np.mean([p for r,p in scores[i]])), file=fout)
            print("\t Snake {} ({}): avg score = {:.2f}, finishes with {:.2f} points on average".format(i, strategies[i].name, np.mean([p/r for r,p in scores[i]]), np.mean([p for r,p in scores[i]])))
        print("\nIterations per game: {:.2f} +- {:.2f}".format(np.mean(iterations), np.std(iterations)), file=fout)
        print("Time out is reached {:.2f}% of the time".format(100*sum(float(x==MAX_ITER) for x in iterations)/len(iterations)), file=fout)
        print("Simulations took {} sec on avg".format(tot_time / n_simul), file=fout)

        print("\n\nParams", file=fout)
        print("\n".join(
            ["{} = {}".format(k, config.__dict__[k] if k != "opponents" else ", ".join([str(o) for o in config.__dict__[k]])) for k in ["agent", "filename", "game_hp", "depth", "num_trials", "opponents", "comment"]]
        ), file=fout)
