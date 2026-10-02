import string
import itertools
import random
from z3_planner import solve

def make_state(blocks, epsilon=.3):
    """
    generate a random state of the block world
    blocks: list of blocks e.g. ['A', 'B', 'C', ...]
    epsilon: float between 0 and 1, modulates the number of towers
    """
    assert 'T' not in blocks
    random.shuffle(blocks)
    # make towers, randomly cutting them
    towers = [[]]
    for b in blocks:
        if random.random() < epsilon:
            towers.append([])
        towers[-1].append(b)
    state = set()
    for tower in towers:
        if not len(tower):
            continue
        for a,b in zip(tower[:-1], tower[1:]):
            state.add(('on', b, a))
        state.add(('on', tower[0], 'T'))
        state.add(('clear', tower[-1]))
    state.add(('table', 'T'))
    state.add(('clear', 'T'))
    return sorted(state)

def generate_states(n_blocks):
    """
    generate an initial and a final_state of the blocks world with `n_blocks` blocks
    """
    blocks = ['B{}'.format(1+ii) for ii in range(n_blocks)]
    initial_state = make_state(blocks)
    final_state = make_state(blocks)
    return initial_state, final_state

""" Below are some util functions to convert the problem into the STRIPS format """

"""Initial state: Table(T), On(A,T), On(D,A), On(C,T), On(B,C), Clear(D), Clear(B)
Goal state: On(C,T), On(B,C), On(A,B)"""
def clause_to_strips(clause):
    pred=clause[0]
    args=clause[1:]
    output = "{}({})".format(pred.capitalize(), ",".join(args))
    return output

action_str="""
Actions:
  // Move block from atop one block to another block
  MoveBlocks(BlockMoved, BlockFrom, BlockTo)
  Pre: !Table(BlockMoved), Clear(BlockMoved), Clear(BlockTo), On(BlockMoved, BlockFrom)
  Post: On(BlockMoved, BlockTo), !On(BlockMoved, BlockFrom), !Clear(BlockTo), Clear(BlockFrom)

  // Move block from table to another block
  MoveFromTable(BlockMoved, BlockFrom, BlockTo)
  Pre: !Table(BlockMoved), Table(BlockFrom), Clear(BlockMoved), Clear(BlockTo), On(BlockMoved, BlockFrom)
  Post: On(BlockMoved, BlockTo), !On(BlockMoved, BlockFrom), !Clear(BlockTo)

  // Move block from block to table
  MoveToTable(BlockMoved, BlockFrom, BlockTo)
  Pre: !Table(BlockMoved), Table(BlockTo), Clear(BlockMoved), On(BlockMoved, BlockFrom)
  Post: On(BlockMoved, BlockTo), !On(BlockMoved, BlockFrom), Clear(BlockFrom)
"""

def print_to_strips(initial_state, goal):
    init_state_str = [clause_to_strips(clause) for clause in initial_state]
    init_state_str = "Initial state: " + ", ".join(init_state_str)
    goal_str = [clause_to_strips(clause) for clause in goal]
    goal_str = "Goal state: " + ", ".join(goal_str)
    return '\n\n'.join((init_state_str, goal_str, action_str))
