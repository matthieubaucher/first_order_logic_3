from z3 import *
import itertools as it
import time

def to_bool(*args):
    """
    clauses are rewritten as predicate-arg1-arg2
    args: any number of string or integer arguments
    output: a boolean representing "args[0](args[1], args[2], ..., )"
    example: to_bool('clear', 'B', 15) -> clear-B-15
    """
    assert all(isinstance(x, int) or isinstance(x, str) for x in args), args
    output = '-'.join(str(x) for x in args)
    return Bool(output)

def recover_plan(model, blocks, times):
    """
    util function to recover plan from SAT model
    """
    # recover plan
    def get_result(*args):
        return model[to_bool(*args)]
    # at each time step, find block that is moved
    plan = []
    for tt in times[:-1]:
        action=set()
        for obj, src, dest in it.product(blocks, blocks, blocks):
            if get_result('object', obj, tt) and get_result('source', src, tt) and get_result('destination', dest, tt) :
                action.add((obj, src, dest))
        assert len(action) == 1, "more than one action or no action taken at time {}: {}".format(tt, action)
        plan.append(list(action).pop())
    return plan

def sat_plan(initial_state, goal, max_time):
    """
    initial_state: list of clauses describing the initial state. Each clause is a tuple of (predicate, arg1, arg2, ...).
    goal: list of clauses describing the goal state. Same format as initial_state.
    max_time: the maximum number of steps to plan for.
    """
    sat_solver = Solver()
    times = list(range(0,max_time+1))
    blocks=set()
    for clause in initial_state + goal:
        blocks |= set(clause[1:])
    # frame axioms of blocks world
    # no block is the table except T
    for block in blocks:
        if block == 'T':
            sat_solver.add(to_bool('table', block))
        else:
            sat_solver.add(Not(to_bool('table', block)))
    # no block is on top of itself
    for block, tt in it.product(blocks, times):
        sat_solver.add(Not(to_bool('on', block, block, tt)))
    # the table is never on top of anything
    for block, tt in it.product(blocks, times):
        sat_solver.add(Not(to_bool('on', 'T', block, tt)))
    # the table is always clear
    for tt in times:
        sat_solver.add(to_bool('clear', 'T', tt))
    # initial conditions
    # 1. describe Initial state
    all_states = [('on', block1, block2) for block1, block2 in it.product(blocks, blocks)] \
            + [('clear', block) for block in blocks]
    for item in all_states:
        assert isinstance(item, tuple)
        clause = item + (0,)
        assert all(isinstance(x, str) or isinstance(x, int) for x in clause), clause
        if item in initial_state:
            sat_solver.add(to_bool(*clause))
        else:
            sat_solver.add(Not(to_bool(*clause)))
    # 2. describe goal
    for item in goal:
        # TODO
        pass
    # actions
    for tt in times:
        for action in ['object', 'source', 'destination']:
            all_actions = [(action, block, tt) for block in blocks]
            # at least one action per time step
            # TODO
            # at most one action per time step
            # TODO
        # all three arguments must be distinct
        # TODO
        # table cannot be the object
        # TODO
    # 3. explanatory frame axioms
    # 'clear'
    for block, tt in it.product(blocks, times):
        sat_solver.add(
                Implies(
                    And(
                        Not(to_bool('clear', block, tt)),
                        to_bool('clear', block, tt+1)
                        ),
                    to_bool('source', block, tt)
                    )
                )
        sat_solver.add(
                Implies(
                    And(
                        to_bool('clear', block, tt),
                        Not(to_bool('clear', block, tt+1))
                        ),
                    to_bool('destination', block, tt)
                    )
                )
    # 'on'
    # TODO
    # 4. describe the actions
    # HINT: We have 3 distinct actions, depending on whether the BlockFrom or BlockTo is the special Table block. But here, we are using the same 'object', 'source' and 'destination' predicates regardless. So you will need to include this information in the preconditions of the action.
    """// Move block from atop one block to another block
    MoveBlocks(BlockMoved, BlockFrom, BlockTo)
    Pre: !Table(BlockMoved), !Table(BlockFrom), !Table(BlockTo), Clear(BlockMoved), Clear(BlockTo), On(BlockMoved, BlockFrom)
    Post: On(BlockMoved, BlockTo), !On(BlockMoved, BlockFrom), !Clear(BlockTo), Clear(BlockFrom)"""
    for blockmoved, blockfrom, blockto, tt in it.product(blocks, blocks, blocks, times[:-1]):
        sat_solver.add(
                Implies(
                    And(
                        to_bool('object', blockmoved, tt),
                        to_bool('source', blockfrom, tt),
                        to_bool('destination', blockto, tt),
                        Not(to_bool('table', blockmoved)),
                        Not(to_bool('table', blockfrom)),
                        Not(to_bool('table', blockto)),
                        ),
                    And(
                        to_bool('clear', blockmoved, tt),
                        Not(to_bool('clear', blockfrom, tt)),
                        to_bool('clear', blockto, tt),
                        to_bool('on', blockmoved, blockfrom, tt),
                        Not(to_bool('on', blockmoved, blockto, tt)),
                        Not(to_bool('on', blockfrom, blockto, tt)),

                        to_bool('clear', blockmoved, tt+1),
                        to_bool('clear', blockfrom, tt+1),
                        Not(to_bool('clear', blockto, tt+1)),
                        to_bool('on', blockmoved, blockto, tt+1),
                        Not(to_bool('on', blockmoved, blockfrom, tt+1)),
                        )
                    )
                )
    """// Move block from table to another block
    MoveFromTable(BlockMoved, BlockFrom, BlockTo)
    Pre: !Table(BlockMoved), Table(BlockFrom), !Table(BlockTo), Clear(BlockMoved), Clear(BlockTo), On(BlockMoved, BlockFrom)
    Post: On(BlockMoved, BlockTo), !On(BlockMoved, BlockFrom), !Clear(BlockTo)"""
    # TODO
    """// Move block from block to table
    MoveToTable(BlockMoved, BlockFrom, BlockTo)
    Pre: !Table(BlockMoved), Table(BlockTo), !Table(BlockFrom), Clear(BlockMoved), On(BlockMoved, BlockFrom)
    Post: On(BlockMoved, BlockTo), !On(BlockMoved, BlockFrom), Clear(BlockFrom)"""
    # TODO
    return sat_solver

def has_solution(sat_solver):
    """
    check whether a sat problem has a model
    """
    return str(sat_solver.check()) == 'sat'

def solve(initial_state, goal, return_statistics=False):
    """
    solve a blocks problem using a SAT solver: convert the blocks problem into n-time-steps SAT problem and run SAT solver. Increase n until you find a solution.
    initial_state: list of clauses describing the initial state. Each clause is a tuple of (predicate, arg1, arg2, ...).
    goal: list of clauses describing the goal state. Same format as initial_state.
    return_statistics: optionally return the number of clauses and variables and other statistics
    """
    blocks = set()
    for clause in initial_state+goal:
        blocks |= set(clause[1:])
    max_time = 2*(len(blocks)-1) # unpile all blocks, pile them up again
    plan_solver = None
    for tt in range(max_time):
        plan_solver = sat_plan(initial_state, goal, tt)
        start_time=time.time()
        plan_solver.check()
        end_time=time.time()
        num_steps=tt
        if has_solution(plan_solver):
            break
    if not has_solution(plan_solver):
        return None
    # get plan as a sat model
    model = plan_solver.model()
    plan = recover_plan(model, blocks, list(range(0,tt+1)))
    if return_statistics:
        g = Goal()
        g.add(plan_solver.assertions())
        t = Tactic('tseitin-cnf')
        cnf = t(g)
        cnf_str = cnf.sexpr() # this is way of doing things is a terrible hack, I hope students don't see this
        num_clauses = 0
        variables=set()
        for line in cnf_str.split('\n'):
            num_clauses += line.startswith('  ')
            variables |= set(line.split(' '))
        # filter out non-variables
        variables = filter(lambda x: '-' in x, variables)
        variables = map(lambda x: x.strip('()'), variables)
        num_variables = len(set(variables))
        return plan, {'num_clauses': num_clauses, 'num_variables': num_variables, 'time': end_time-start_time, 'num_steps': num_steps}
    else:
        return plan
