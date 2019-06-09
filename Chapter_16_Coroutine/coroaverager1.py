
from coroutil import coroutine

@coroutine
def average():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count


coro_avg = average()
from inspect import getgeneratorstate

print(getgeneratorstate(coro_avg))

print(coro_avg.send(10))
print(coro_avg.send(30))
print(coro_avg.send(5))


"""
Output:
    10.0
    20.0
    15.0
"""