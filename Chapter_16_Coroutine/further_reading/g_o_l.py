# https://github.com/bslatkin/effectivepython/blob/master/example_code/item_40.py
from collections import namedtuple



ALIVE = '+'
EMPTY = '-'

def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state

Query = namedtuple("Query", ('y', 'x'))


def count_neighbors(y, x):
    """
    Calculating neighbour count
    """
    count = 0
    north = yield Query(y+1, x)
    south = yield Query(y-1, x)
    east = yield Query(y, x+1)
    ne = yield Query(y+1, x+1)
    se = yield Query(y-1, x+1)
    sw = yield Query(y-1, x-1)
    west = yield Query(y, x-1)
    nw = yield Query(y+1, x-1)

    direct = [north, south, east, west, ne, se, sw, nw]
    for i in direct:
        if i == ALIVE:
            count += 1

    return count

'''
it = count_neighbors(10, 5)
q1 = next(it)                  # Get the first query
print('First yield: ', q1)
q2 = it.send(ALIVE)            # Send q1 state, get q2
print('Second yield:', q2)
q3 = it.send(ALIVE)            # Send q2 state, get q3
print('...')
q4 = it.send(EMPTY)
q5 = it.send(EMPTY)
q6 = it.send(EMPTY)
q7 = it.send(EMPTY)
q8 = it.send(EMPTY)
try:
    it.send(EMPTY)     # Send q8 state, retrieve count
except StopIteration as e:
    print('Count: ', e.value)  # Value from return statement
'''

Transition = namedtuple("Transition", ('y', 'x', 'state'))
'''
def step_cell(y, x):
    currentstate = yield Query(y, x)
    count = yield from count_neighbors(y, x)
    newstate = game_logic(currentstate, count)
    return Transition(y, x, newstate)
'''

def step_cell(y, x):
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)

it = step_cell(10, 5)
q0 = next(it)           # Initial location query
print('Me:      ', q0)
q1 = it.send(ALIVE)     # Send my status, get neighbor query
print('Q1:      ', q1)
print('...')
q2 = it.send(ALIVE)
q3 = it.send(ALIVE)
q4 = it.send(ALIVE)
q5 = it.send(ALIVE)
q6 = it.send(EMPTY)
q7 = it.send(EMPTY)
q8 = it.send(EMPTY)
t1 = it.send(EMPTY)     # Send for q8, get game decision
print('Outcome: ', t1)