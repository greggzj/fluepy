#Example 12-3. DoppelDict2 and AnswerDict2 work as expected because they extend
#UserDict and not dict

import collections

class DoppelDict2(collections.UserDict):
    def __setitem__(self, key, value):
        return super().__setitem__(key, [value]*2)


class AnswerDict2(collections.UserDict):
    def __getitem__(self, key):
        return 42

import abc
import datetime
import inspect

class MessageDisplay(abc.ABC):
    @abc.abstractmethod
    def display(self, message):
        pass

class FriendMessageDisplay(MessageDisplay):
    def display(self, message):
        print(message)

    def greet(self):
        hourt = datetime.datetime.now().timetuple().tm_hour
        print('haha')

if __name__ == "__main__":
    print(inspect.isabstract(MessageDisplay))
    print(inspect.isabstract(FriendMessageDisplay))

    dd = DoppelDict2(one=1)
    print(dd)
    dd['two']  = 2
    print(dd['two'])
    dd.update(three=3)
    print(dd)

    ad = AnswerDict2(a='foo')
    print(ad['a'])
    d = {}
    d.update(ad)
    print(d['a'])
    print(d)


    