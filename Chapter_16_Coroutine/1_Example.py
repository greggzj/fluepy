#Example 16-2. A coroutine that yields twice
def simple_coro2(a):
    print('-> Started: a =', a)
    b = yield a
    print('-> Received: b =', b)
    c = yield a + b
    print('-> Received: c =', c)

def ex_16_2():
    my_coro2 = simple_coro2(14)
    from inspect import getgeneratorstate

    print(getgeneratorstate(my_coro2))

    next(my_coro2)

    c = getgeneratorstate(my_coro2)
    print(c)

    my_coro2.send(28)

    my_coro2.send(99)

    getgeneratorstate(my_coro2)


    """
    Output:
        GEN_CREATED
        -> Started: a = 14
        GEN_SUSPENDED
        -> Received: b = 28
        -> Received: c = 99
        Traceback (most recent call last):
        File "/home/gregg/.vscode/extensions/ms-python.python-2019.5.17517/pythonFiles/ptvsd_launcher.py", line 43, in <module>
            main(ptvsdArgs)
        File "/home/gregg/.vscode/extensions/ms-python.python-2019.5.17517/pythonFiles/lib/python/ptvsd/__main__.py", line 434, in main
            run()
        File "/home/gregg/.vscode/extensions/ms-python.python-2019.5.17517/pythonFiles/lib/python/ptvsd/__main__.py", line 312, in run_file
            runpy.run_path(target, run_name='__main__')
        File "/usr/lib/python3.6/runpy.py", line 263, in run_path
            pkg_name=pkg_name, script_name=fname)
        File "/usr/lib/python3.6/runpy.py", line 96, in _run_module_code
            mod_name, mod_spec, pkg_name, script_name)
        File "/usr/lib/python3.6/runpy.py", line 85, in _run_code
            exec(code, run_globals)
        File "/home/gregg/01_hzj/03_fluentpython/fluepy/Chapter_16/Example.py", line 22, in <module>
            my_coro2.send(99)
        StopIteration

        GENCLOSED (环境要单步执行，否则不会运行到这里，报错就退出了)
    """


#Example 16-4. coroaverage0.py: doctest for the running average coroutine in example 16-3
def ex_16_4():
    from coroaverager0 import averager
    coro_avg = averager()
    next(coro_avg)
    print(coro_avg.send(10))
    print(coro_avg.send(30))
    print(coro_avg.send(5))


    """
    Output
        10.0
        20.0
        15.0
    """



if __name__ == "__main__":
    ex_16_4()