#Example16-7. coroaverager3.py: using yield from to drive averager and report statistics
from collections import namedtuple

Result = namedtuple('Result', 'count average')

# the subgenerator
def averager():
    total = 0.0
    count = 0
    average = None
    #print('111')
    while True:
        #print('222')
        term = yield  #Each value sent by the client code in main will be bound to term here
        #print('333')
        if term is None: #terminating condition, without it , a yield from calling this coroutine will block forever
            break
        total += term
        count += 1
        average = total/count
        #print('444')
    #print('555')
    return Result(count, average)


# the delegating generator
def grouper(results, key):
    #每一次的循环都会创建一个新的averager实例
    #每一个averager实例都是一个可以作为coroutine操作的generator object
    while True: 
        #Whenever grouper is sent a value, it’s piped into the averager instance by the
        #yield from. grouper will be suspended here as long as the averager instance
        #is consuming values sent by the client. When an averager instance runs to the
        #end, the value it returns is bound to results[key]. The while loop then
        #proceeds to create another averager instance to consume more values.

        #每当client向grouper发送一个value，grouper就可以作为一个管道，这个value就会通过
        #yield from关键字从管道传入averager 实例。当averager实例运行完返回，返回的值就会
        #绑定到results[key]中。while循环继续处理创建下一个averager实例。

        #print('11')
        results[key] = yield from averager()    
        #print('22')

# the client code, a.k.a. the caller
def main(data):
    results = {}
    for key, values in data.items():
        #group is a generator object resulting from calling grouper with the results dict
        #to collect the results, and a particular key. It will operate as a coroutine.
        #print('1')
        group = grouper(results, key)
  
        #Prime the coroutine.
        #print('2')
        next(group)
        #print('++++++')
        for value in values:
            #往grouper发送value，这个value会在averager中的yield这行终止
            #这个value对grouper不可见
            group.send(value)
        #print('------')

        #非常重要！！！！！
        #向grouper发送None会触发当前averager实例的终止，
        #而后grouper中进入while的下一个循环，创建另一个averager实例用于处理下一次从client过来的value
        
        
        #如果注释掉这行，results将会为空，因为:
        #最外层client这边在每一个循环里都创建了grouper实例group，每个group就是delegating generator

        #调用next(group)就是prime the grouper delegating generator，调用后会进入while True
        #循环并在调用subgenerator averager后suspend在yield from

        #client内层for循环调用了group.send(value)，将value直接送到averager里，与此同时，当前的group
        #实例仍旧suspend在yield from

        #当内层for循环终止，gourp实例仍旧suspend在yield from，此时grouper中results[key]仍旧未被
        #赋值

        #重点来了！ 如果没有client这边外城for循环的最后一行group.send(None)，averager subgenerator
        #永远不会被terminate, delegating generator group也永远不会reactivated(一直suspend)

        #当循环再次来到外层for循环时，一个新的grouper实例会被创建并绑定到group。之前创建的的grouper实例
        #会与其拥有的unfinished 的averager subgenerator实例一起被自动回收

        group.send(None)
        #print('******')

    report(results)


def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit
        ))

data = {
    'girls;kg':
    [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
    [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
    [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
    [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

if __name__ == "__main__":
    main(data)