import asyncio
import itertools
import sys

'''
The yield from asyncio.sleep(3) expression handles the control flow to the
main loop, which will resume this coroutine after the sleep delay.

supervisor is now a coroutine as well, so it can drive slow_function with yield
from.

asyncio.async(…) schedules the spin coroutine to run, wrapping it in a Task
object, which is returned immediately.

Display the Task object. The output looks like <Task pending coro=<spin()
running at spinner_asyncio.py:12>>.

Drive the slow_function(). When that is done, get the returned value.
Meanwhile, the event loop will continue running because slow_function
ultimately uses yield from asyncio.sleep(3) to hand control back to the main
loop.

A Task object can be cancelled; this raises asyncio.CancelledError at the yield
line where the coroutine is currently suspended. The coroutine may catch the
exception and delay or even refuse to cancel.

Get a reference to the event loop.

Drive the supervisor coroutine to completion; the return value of the coroutine
is the return value of this call.
'''

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
    yield from asyncio.sleep(3) # 6
    return 42

@asyncio.coroutine
def supervisor():   # 7
    spinner = asyncio.async(spin('thinking!'))  # 8
    print('spinner object:', spinner)   # 9
    result = yield from slow_function() # 10
    spinner.cancel()    # 11
    return result

def main():
    loop = asyncio.get_event_loop() # 12
    result = loop.run_until_complete(supervisor())  # 13
    loop.close()
    print('Answer:', result)

if __name__ == '__main__':
    main()