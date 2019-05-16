import abc
import random

from chapter_11.tombola import Tombola

import pdb

class BingoCage(Tombola):

    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(item)

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        self.pick()


class LotteryBlower(Tombola):
    def __init__(self, iterable):
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except:
            raise LookupError('pick from empty BingoCage')
        return self._balls.pop(position)
    
    def loaded(self):
        return bool(self._balls)

    def inspect(self):
        return tuple(sorted(self._balls))


class MySelf(Tombola):
    def __init__(self):
        pass

    def load(self):
        print("loading.....")

    def pick(self):
        print("picking.....")



if __name__ == "__main__":
    pdb.set_trace()
    newcls = MySelf()

    import tkinter
    import collections