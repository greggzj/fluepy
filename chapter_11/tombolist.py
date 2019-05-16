from random import randrange

from tombola import Tombola

@Tombola.register
class TomboList(list):

    
    def pick(self):
        if self:
            position = randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))

class Struggle:
    def __len__(self):return 23

class AA:
    def __init__(self):return23

if __name__ == "__main__":
    a = TomboList([1,2,3,4])
    from collections import abc
    isinstance(Struggle(), AA)
