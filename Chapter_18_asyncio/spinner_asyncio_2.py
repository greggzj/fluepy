import asyncio
import itertools
import sys


'''
Coroutines intended for use with asyncio should be decorated with @asyn
cio.coroutine. This not mandatory, but is highly advisable. See explanation
following this listing.
'''
@asyncio.coroutine  # 1
def spin(msg):  # 2 不需要spinner_thread_1.py中的spin函数有signal入参来关闭线程
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            # Use yield from asyncio.sleep(.1) instead of just time.sleep(.1), to sleep
            # without blocking the event loop.
            yield from asyncio.sleep(.1)
        # 有cancel 请求(通过asyncio.CancelledError方式) 退出循环
        except asyncio.CancelledError:  # 4
            break
    write(' ' * len(status) + '\x08' * len(status))

@asyncio.coroutine
def slow_function(): 
    '''
    slow_function is now a coroutine, and uses yield from to let the event loop
    proceed while this coroutine pretends to do I/O by sleeping.
    '''
    # pretend waiting a long time for I/O
    # The yield from asyncio.sleep(3) expression handles the control flow to the
    # main loop, which will resume this coroutine after the sleep delay.
    # 
    yield from asyncio.sleep(3) # 6
    return 42

@asyncio.coroutine
def supervisor():   # 7 supervisor is now a coroutine as well, so it can drive slow_function with yield from.

    '''
    asyncio.async(…) schedules the spin coroutine to run, wrapping it in a Task
    object, which is returned immediately.
    '''
    spinner = asyncio.async(spin('thinking!'))  # 8
    # 9 打印Task object, 输出的消息类似: Task pending coro=<spin() running at spinner_asyncio.py:12
    print('spinner object:', spinner) 

    '''
    Drive the slow_function(). When that is done, get the returned value.
    Meanwhile, the event loop will continue running because slow_function
    ultimately uses yield from asyncio.sleep(3) to hand control back to the main
    loop.
    '''
    result = yield from slow_function() # 10

    '''
    A Task object can be cancelled; this raises asyncio.CancelledError at the yield
    line where the coroutine is currently suspended. The coroutine may catch the
    exception and delay or even refuse to cancel.
    '''
    spinner.cancel()    # 11
    return result

def main():
    # 12 Get a reference to the event loop.
    loop = asyncio.get_event_loop()
    '''
    Drive the supervisor coroutine to completion; the return value of the coroutine
    is the return value of this call.
    '''
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)

if __name__ == '__main__':
    main()



'''
永远不要在asyncio coroutines里面使用time.sleep(...)，除非你想阻塞main thread，freezing event loop和whole application。
如果一定要用sleep, 使用yield from asyncio.sleep(DELAY)
'''