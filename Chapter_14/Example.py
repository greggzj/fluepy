#Example 14-14
def vowel(c):
    return c.lower() in 'aeiou'


#Example 14-15
sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
import itertools


#Example 14-16 Mapping generator function examples
def ex_14_16():
    a = list(enumerate('albatroz', 1))
    print(a)
    import operator
    b = list(map(operator.mul, range(11), range(11)))
    print(b)

    c = list(map(operator.mul, range(11), [2, 4, 8]))
    print(c)
    
    d = list(map(lambda a, b:(a, b), range(11), [2, 4, 8]))
    print(d)
    
    import itertools
    e = list(itertools.starmap(operator.mul, enumerate('albatroz', 1)))
    print(e)

    sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
    f = list(itertools.starmap(lambda a, b: b/a, 
        enumerate(itertools.accumulate(sample), 1)))
    print(f)
    """
    Results:
    Number the letters in the word, starting from 1
    [(1, 'a'), (2, 'l'), (3, 'b'), (4, 'a'), (5, 't'), (6, 'r'), (7, 'o'), (8, 'z')]

    Squares of integers from 0 to 10
    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

    Multiplying numbers from two iterables in parallel: results stop when the
    shortest iterable ends.
    [0, 4, 16]

    This is what the zip built-in function does.
    [(0, 2), (1, 4), (2, 8)]

    Repeat each letter in the word according to its place in it, starting from 1
    ['a', 'll', 'bbb', 'aaaa', 'ttttt', 'rrrrrr', 'ooooooo', 'zzzzzzzz']

    Running average:
    [5.0, 4.5, 3.6666666666666665, 4.75, 5.2, 5.333333333333333, 5.0, 4.375, 4.888888888888889, 4.5]
    """

#Example 14-17. Merging generator function examples
def ex_14_17():
    import itertools
    a = list(itertools.chain('ABC', range(2)))
    print(a)
    
    b = list(itertools.chain(enumerate('ABC')))
    print(b)

    c = list(itertools.chain.from_iterable(enumerate('ABC')))
    print(c)

    d = list(zip('ABC', range(5)))
    print(d)

    e = list(zip('ABC', range(5), [10, 20, 30, 40]))
    print(e)

    f = list(itertools.zip_longest('ABC', range(5)))
    print(f)

    g = list(itertools.zip_longest('ABC', range(5), fillvalue="?"))
    print(g)

    """
    Results:
    chain 通常用于两个以上iterable的连接
    ['A', 'B', 'C', 0, 1]

    chain 对于单个Iterable没有太大用处
    [(0, 'A'), (1, 'B'), (2, 'C')]


    chain.from_iterable 解析每一个iterable的每一个item，将其连接起来，对于单个iterable
    也能够将其扁平化
    [0, 'A', 1, 'B', 2, 'C']

    zip通常用来merge两个Iterable到tuple，而后将这些tuple组成一个系列
    [('A', 0), ('B', 1), ('C', 2)]

    Any number of iterables can be consumed by zip in parallel, but the generator
    stops as soon as the first iterable ends.
    [('A', 0, 10), ('B', 1, 20), ('C', 2, 30)]

    itertools.zip_longest works like zip, except it consumes all input iterables
    to the end, padding output tuples with None as needed.
    [('A', 0), ('B', 1), ('C', 2), (None, 3), (None, 4)]

    The fillvalue keyword argument specifies a custom padding value.
    [('A', 0), ('B', 1), ('C', 2), ('?', 3), ('?', 4)]
    """

#Example 14-18. itertools product generator function examples
def ex_14_18():
    import itertools
    a = list(itertools.product('ABC', range(2))) 
    print(a)

    suits = 'spades hearts diamonds clubs'.split()
    b = list(itertools.product('AK', suits))
    print(b)

    c = list(itertools.product('ABC'))
    print(c)

    d = list(itertools.product('ABC', repeat=2))
    print(d)

    e = list(itertools.product(range(2), repeat=3))
    print(e)

    rows = itertools.product('AB', range(2), repeat=2)
    for row in rows: print(row)


    """ 
    笛卡尔乘积个概念：
    1） For example, product(A, B) returns the same as ((x,y) for x in A for y in B).
    这个后续还要在理解理解
    2） def product(*args, repeat=1):
            # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
            # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
            pools = [tuple(pool) for pool in args] * repeat
            result = [[]]
            for pool in pools:
                result = [x+[y] for x in result for y in pool]  
            for prod in result:
                yield tuple(prod)

    Results:
    笛卡尔乘积： 3个字符的字符串和一个两个元素的数组，结果一共3*2=6个元素
    [('A', 0), ('A', 1), ('B', 0), ('B', 1), ('C', 0), ('C', 1)]


    [('A', 'spades'), ('A', 'hearts'), ('A', 'diamonds'), ('A', 'clubs'), ('K', 'spades'), ('K', 'hearts'), ('K', 'diamonds'), ('K', 'clubs')]
    
    单个iterable入参，不是很有用
    [('A',), ('B',), ('C',)]

    repeat表示重复消耗product的另外的入参的次数
    [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]
    [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    ('A', 0, 'A', 0)
    ('A', 0, 'A', 1)
    ('A', 0, 'B', 0)
    ('A', 0, 'B', 1)
    ('A', 1, 'A', 0)
    ('A', 1, 'A', 1)
    ('A', 1, 'B', 0)
    ('A', 1, 'B', 1)
    ('B', 0, 'A', 0)
    ('B', 0, 'A', 1)
    ('B', 0, 'B', 0)
    ('B', 0, 'B', 1)
    ('B', 1, 'A', 0)
    ('B', 1, 'A', 1)
    ('B', 1, 'B', 0)
    ('B', 1, 'B', 1)
    """

#Example 14-19. count, cycle, and repeat
def ex_14_19():
    import itertools
    ct = itertools.count()
    a = next(ct)
    print(a)

    b = next(ct), next(ct), next(ct)
    print(b)

    c = list(itertools.islice(itertools.count(1, .3), 3))
    print(c)

    cy = itertools.cycle('ABC')
    d = next(cy)
    print(d)

    e = list(itertools.islice(cy, 7))
    print(e)

    rp = itertools.repeat(7)
    f = next(rp)
    print(f)
    g = next(rp)
    print(g)

    h = list(itertools.repeat(8, 4))
    print(h)

    import operator
    i = list(map(operator.mul, range(11), itertools.repeat(5)))
    print(i)

    """
    Results:
    count generator 没有个数限制，不能用List来进行转换
    0
    (1, 2, 3)

    count generator可以通过isslice or takewhile来限制个数
    [1, 1.3, 1.6]
    
    cycle generator产生循环的items
    A
    ['B', 'C', 'A', 'B', 'C', 'A', 'B']

    cycle generator可以用第二个入参time来限制yield个数
    7
    7

    repeat generator产生重复的items，可以通过第二个入参time来限制重复个数
    [8, 8, 8, 8]
    [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    """

#Example 14-20. Combinatoric generator functions yield multiple values per input item
def ex_14_20():
    import itertools
    a = list(itertools.combinations('ABC', 2))
    print(a)

    b = list(itertools.combinations_with_replacement('ABC', 2))
    print(b)

    c = list(itertools.permutations('ABC', 2))
    print(c)

    d = list(itertools.product('ABC', repeat=2))
    print(d)

    """
    Results:
    长度为2的‘ABC’的组合：
    [('A', 'B'), ('A', 'C'), ('B', 'C')]

    长度为2，允许单个item重复的‘ABC’的组合
    [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]

    长度为2，‘ABC’的排列组合
    [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

    笛卡尔乘积
    [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]
    
    """

if __name__ == "__main__":
    #ex_14_16()
    #ex_14_17()
    #ex_14_18()
    #ex_14_19()
    ex_14_20()