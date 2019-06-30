#Python cookbook: 12.12. Using Generators As an Alternative to Threads

# Two simple generator functions
def countdown(n):
    while n > 0:
        print('T-minux', n)
        yield
        n -= 1
    print('Blastoff!')

def countup(n):
    x = 0
    while x < n:
        print('Counting up', x)
        yield
        x += 1


from collections import deque

class TaskScheduler:
    def __init__(self):
        self._task_queue = deque()

    def new_task(self, task):
        '''
        Admit a newly started task to the scheduler
        '''
        self._task_queue.append(task)

    def run(self):
        '''
        Run until there are no more tasks
        '''
        while self._task_queue:
            task = self._task_queue.popleft()
            try:
                # Run util the next yield statement
                next(task)
                self._task_queue.append(task)
            except StopIteration:
                # Generator is no longer executing
                pass

if __name__ == "__main__":
    sched = TaskScheduler()
    sched.new_task(countdown(10))
    sched.new_task(countdown(5))
    sched.new_task(countup(15))
    sched.run()

'''
Output:
    T-minux 10
    T-minux 5
    Counting up 0
    T-minux 9
    T-minux 4
    Counting up 1
    T-minux 8
    T-minux 3
    Counting up 2
    T-minux 7
    T-minux 2
    Counting up 3
    T-minux 6
    T-minux 1
    Counting up 4
    T-minux 5
    Blastoff!
    Counting up 5
    T-minux 4
    Counting up 6
    T-minux 3
    Counting up 7
    T-minux 2
    Counting up 8
    T-minux 1
    Counting up 9
    Blastoff!
    Counting up 10
    Counting up 11
    Counting up 12
    Counting up 13
    Counting up 14
'''
