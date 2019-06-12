from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
    total = 0.0
    count = 0
    averager = None
    while True:
        term = yield
        if term is None:
            break ##In order to return a value, a coroutine mus terminate normally
        total += term
        count += 1
        averager = total/count
    return Result(count, averager)#Before python3.3, it was a syntax error to return a value in a generator function


#Example 16-14. doctest showing the behavior of averager
def ex_16_14():
    coro_avg = averager()
    next(coro_avg)
    coro_avg.send(10) #This version do not yield values.
    coro_avg.send(30)
    coro_avg.send(6.5)
    coro_avg.send(None)
    """
    Last line of code will cause
    Traceback (most recent call last):
    ...
    StopIteration: Result(count=3, average=15.5)
    """

#Example 16-15. Catching StopIteration lets us get the value returned by averager
def ex_16_15():
    coro_avg = averager()
    next(coro_avg)
    coro_avg.send(10)
    coro_avg.send(30)
    coro_avg.send(6.5)
    try:
        coro_avg.send(None)
    except StopIteration as exc:
        result = exc.value

    print(result)
    """
    Output:
        Result(count=3, average=15.5)

    client 发送了None, 协程内部退出while循环，返回给client的是StopIteration异常，
    异常的value为generator function的返回值named tuple，外部的处理方式参考这里的
    try except
    """

if __name__ == "__main__":
    #ex_16_14()
    ex_16_15()