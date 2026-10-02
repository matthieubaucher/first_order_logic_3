from z3_planner import solve
from problem_generator import generate_states
from timeit import timeit
import random
import matplotlib
import matplotlib.pyplot as plt
import json
import tqdm
from strips import main

# TODO bonus: figure out where to sample the points to reconstruct the curve
data = {}
N=100
for n_blocks in range(2, 8):
    print(n_blocks)
    data[n_blocks]=[]
    for nn in tqdm.tqdm(range(N)): # N data points
        initial_state, goal = generate_states(n_blocks)
        _, stats = solve(initial_state, goal, return_statistics=True)
        data[n_blocks].append((stats['num_clauses']/stats['num_variables'], stats['time']))
    data[n_blocks].sort()
    data[n_blocks] = [list(x) for x in data[n_blocks]]
    fig, ax = plt.subplots(1,1)
    ax.plot([x[0] for x in data[n_blocks]], [x[1] for x in data[n_blocks]], label=n_blocks)
    fig.savefig('plot-{}.png'.format(n_blocks))
print(json.dumps(data, indent=2))
