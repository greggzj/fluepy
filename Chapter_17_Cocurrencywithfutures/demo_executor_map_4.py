from time import sleep, strftime
from concurrent import futures

# Print消息，带上当前时间戳
def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done'
    display(msg.format('\t'*n, n))
    return n*10

def main():
    display('Script starting.')
    # 使用ThreadPoolExecutor初始化3个线程
    executor = futures.ThreadPoolExecutor(max_workers=3)

    # nonblocking call, 产生5个task到3个thread，只有3个task能够立即执行
    results = executor.map(loiter, range(5)) # 5

    # 立即显示results，results是generator
    display('results:', results)
    display('Waiting for individual results:')

    '''
    The enumerate call in the for loop will implicitly invoke next(results), which
    in turn will invoke _f.result() on the (internal) _f future representing the first
    call, loiter(0). The result method will block until the future is done, therefore
    each iteration in this loop will have to wait for the next result to be ready.

    This is where execution may block, depending on the parameters given to the
    loiter calls: the __next__ method of the results generator must wait until the
    first future is complete. In this case, it won’t block because the call to loi
    ter(0) finished before this loop started.
    '''
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))


main()


"""
Output:

[14:17:36] Script starting.
[14:17:36] loiter(0): doing nothing for 0s...
[14:17:36] loiter(0): done
[14:17:36]      loiter(1): doing nothing for 1s...
[14:17:36]              loiter(2): doing nothing for 2s...
[14:17:36][14:17:36]                    loiter(3): doing nothing for 3s... results:
 <generator object Executor.map.<locals>.result_iterator at 0x0000017FB19F1D00>
[14:17:36] Waiting for individual results:
[14:17:36] result 0: 0      # 6
[14:17:37]      loiter(1): done     # 7
[14:17:37]                              loiter(4): doing nothing for 4s...
[14:17:37] result 1: 10     # 8
[14:17:38]              loiter(2): done     # 9
[14:17:38] result 2: 20
[14:17:39]                      loiter(3): done
[14:17:39] result 3: 30
[14:17:41]                              loiter(4): done     # 10
[14:17:41] result 4: 40


"""
