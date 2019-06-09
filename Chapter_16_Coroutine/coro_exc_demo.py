from inspect import getgeneratorstate

class DemoException(Exception):
    """
    An exception type for the demonstration
    """
    pass


def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:
            print('*** DemoException handled. Continuing...')
        else:
            print('-> coroutine received: {!r}'.format(x))
    
    raise RuntimeError('This line should never run')


#Example 16-9. Activating and closing demo_exc_handling without an exception
def ex_16_9():
    exc_coro = demo_exc_handling()
    next(exc_coro)

    exc_coro.send(11)

    exc_coro.send(22)

    exc_coro.close()

    print(getgeneratorstate(exc_coro))


    """
    Output:
        -> coroutine started
        -> coroutine received: 11
        -> coroutine received: 22
        GEN_CLOSED
    """


#Example 16-10. Throwing DemoExceptino into demo_exc_handling does not break it
def ex_16_10():
    exc_coro = demo_exc_handling()
    next(exc_coro)

    exc_coro.send(11)

    exc_coro.throw(DemoException)

    print(getgeneratorstate(exc_coro))

    """
    Output
        -> coroutine started
        -> coroutine received: 11
        *** DemoException handled. Continuing...
        GEN_SUSPENDED
    """

#Example 16-11. Coutine terminates if it can't handle an exception thown into it
def ex_16_11():
    exc_coro = demo_exc_handling()
    next(exc_coro)

    exc_coro.send(11)
                                           
    exc_coro.throw(ZeroDivisionError)

    print(getgeneratorstate(exc_coro))


    """
    Output:
        -> coroutine started
        -> coroutine received: 11
        Traceback (most recent call last):
        ...
        ZeroDivisionError
        GEN_CLOSED
    """

if __name__ == "__main__":
    ex_16_11()
    #ex_16_10()