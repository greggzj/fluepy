# Example 16-18. Simplified psedudocode equivalent to the statement
# RESULT = yield from EXPR in the delegating generetor (this covers the 
# simplest case: .throw(...) and .close() are not supported; the only
# exception handled is StopIteration)

# _i: The Subgenerator
# _y: A value yielded from the subgenerator
# _r: The eventual result (i.e., the value of the yield from expression when the subgenerator ends)
# _s: A value sent by the caller to the delegating generator, which is forwarded to the subgenerator
# _e: An exception (always an instance of StopIteration in this simplified pseudocode)

# EXPR可以是任意的iterable, 因为Iter()函数应用于它这样就可以返回一个Iterator _i，_i就是subgenerator
_i = iter(EXPR)
try:
    # prime subgenerator, 结果存储到后续会被yield的_y中
    _y = next(_i)
except StopIteration as _e:
    # 如果raise了StopIteration， 取出exception的value 作为RESULT
    _r = _e.value
else:
    # While this loop is running, the delegating generator is blocked, operating just
    # as a channel between the caller and the subgenerator.
    # 当这个while循环运行时， delegating generator被block， 只作为caller和subgenerator
    # 之间的一个channel
    while 1:
        # Yield 从subgenerator yield出来的当前item；
        # 等待从caller send的value _s. Note that this is the only yield in this listing.??
        _s = yield _y
        try:
            # 尝试 advance subgenerator,发送 caller send 过来的 _s 的值
            _y = _i.send(_s)
        except StopIteration as _e:
            # If the subgenerator raised StopIteration, get the value, assign to _r, and exit
            # the loop, resuming the delegating generator.

            # 如果subgenerator raise了StopIteration, 获取其中的value, 赋值给_r，
            # 而后退出循环，resume delegating generator.
            _r = _e.value
            break

#_r is the RESULT: the value of the whole yield from expression.
# _r 就是RESULT: yield from表达式整个的最终值
RESULT = _r



# Example 16-19. Pseudocode equivalent to the statement RESULT = yield from EXPR
# in the delegating generator
import sys















#同上
_i = iter(EXPR)
try:
    #同上
    _y = next(_i)
except StopIteration as _e:
    #同上
    _r = _e.value
else:
    #同上
    while 1:
        try:
            #同上
            _s = yield _y
        # 处理 caller close delegating generator 和 subgenerator。
        # 需要注意，由于subgenerator可以是任意的Iterator，所以可能不包含可调用的close()方法
        # 如果是这种情况，那么就抛出AttributeError 
        except GeneratorExit as _e:
            try:
                _m = _i.close
            except AttributeError:
                pass
            else:
                _m()
            raise _e
        # 处理caller抛出的exceptions
        # 会调用subgenerator的throw()方法
        # 注意，subgenerator可以是一个iterator，不包含可调用的throw()方法，这种情况下
        # AttributeError就会被抛出
        except BaseException as _e:
            _x = sys.exc_info()
            try:
                _m = _i.throw
            except AttributeError:
                raise _e
            # 如果subgenerator 包含可调用的throw 方法，那么就会被调用，并且入参就是caller传递过来的
            # exception。
            # subgenerator 可能会处理exception（这里的else分支）（并且会继续loop循环）；
            # subgenerator 可能会在处理exception过程中raise StopIteration，如果是这种情况，那么_r的值就是exception的value，同时循环终止
            # subgenerator 可能会在处理exception过程中raise 相同的或者其他的exception，对于这种情况，这里不做处理，直接将exception传递到delegating generator
            else:
                try:
                    _y = _m(*_x)
                except StopIteration as _e:
                    _r = _e.value
                    break
        # 如果yield时没有任何exception发生
        else:
            # 尝试advance subgenerator
            try:
                # 如果当前caller send的值为None，那么就对subgenerator调用next方法
                # 否则调用send 把caller send过来的value透传给subgenerator
                if _s is None:
                    _y = next(_i)
                else:
                    _y = _i.send(_s)
            # 如果subgenerator raise StopIteration，那么就获取exception的value到_r并退出循环
            # 同时resume delegating generator
            except StopIteration as _e:
                _r = _e.value
                break

#_同上
RESULT = _r