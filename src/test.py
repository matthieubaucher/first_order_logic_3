from z3_planner import solve
from problem_generator import generate_states

def valid_move(state, move):
    """
    check whether the action `move` can be taken given the `state` the world is in
    """
    obj, source, dest = move
    obj_is_clear = ('clear', obj) in state
    dest_is_clear = ('clear', dest) in state
    is_on = ('on', obj, source) in state
    return (obj_is_clear and dest_is_clear and is_on)

def apply_move(state, move):
    """
    apply action `move` to the `state`. Return new state of the world.
    """
    assert valid_move(state, move)
    obj, source, dest = move
    state.remove(('on', obj, source))
    state.add(('on', obj, dest))
    if dest != 'T':
        state.remove(('clear', dest))
    state.add(('clear', source))
    return state

def test(initial_state, final_state):
    """
    check whether the `solve` function from z3_planner can find a valid sequence of actions
    that turn `initial_state` into `final_state`. Print the result.
    initial_state: list of clauses describing the initial state. Each clause is a tuple of (predicate, arg1, arg2, ...).
    goal: list of clauses describing the goal state. Same format as initial_state.
    """
    plan = solve(initial_state, final_state)
    if plan is None:
        print("FAILED to find a solution with initial state\n{}\nand final state\n{}".format(
            initial_state, final_state))
        return
    # check the plan
    state = set(initial_state)
    plan_correct = True
    for move in plan:
        if not valid_move(state, move):
            plan_correct=False
            break
        state = apply_move(state, move)
    plan_correct = plan_correct and (set(final_state) == set(state))
    if plan_correct:
        print("SUCCESS with initial state\n{}\nand final state\n{}\nand plan\n{}".format(
            initial_state, final_state, plan))
    else:
        print("FAILED to find a valid plan with initial state\n{}\nand final state\n{}\nand plan\n{}".format(
            initial_state, final_state, plan))

for ii in range(2,10):
    print('TEST with {} blocks'.format(ii))
    initial_state, goal = generate_states(ii)
    test(initial_state, goal)
