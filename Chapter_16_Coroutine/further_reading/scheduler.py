# http://www.cosc.canterbury.ac.nz/greg.ewing/python/yield-from/yf_current/Examples/Scheduler/scheduler.txt
current = None
ready_list = []

# Example 1
def schedule(g):
    ready_list.append(g)

def run():
    global current
    while ready_list:
        g = ready_list[0]
        current = g
        try:
            next(g)
        except StopIteration:
            unschedule(g)
        else:
            expire_timeslice(g)


def expire_timeslice(g):
    if ready_list and ready_list[0] is g:
        del ready_list[0]
        ready_list.append(g)

def unschedule(g):
    if g in ready_list:
        ready_list.remove(g)


def person(name, count):
    for i in range(count):
        print(name, 'running')
        yield

def ex_1():
    schedule(person('John', 2))
    schedule(person('Michael', 3))
    schedule(person('Terry', 4))

    run()


# Example 2
def block(queue):
    queue.append(current)
    unschedule(current)

def unblock(queue):
    if queue:
        g = queue.pop(0)
        schedule(g)

class Utensil:
    def __init__(self, id):
        self.id = id
        self.available = True
        self.queue = []

    def acquire(self):
        if not self.available:
            block(self.queue)
            yield
        self.available = False

    def release(self):
        self.avaiable = True
        unblock(self.queue)


def philosopher(name, lifetime, think_time, eat_time, left_fork, right_fork):
    for i in range(lifetime):
        for j in range(think_time):
            print(name, 'thinking')
            yield
        print(name, 'waiting for fork', left_fork.id)
        yield from left_fork.acquire()
        print(name, 'acquire fork', left_fork.id)
        print(name, 'waiting for fork', right_fork.id)
        yield from right_fork.acquire()
        print(name, 'acquire fork', right_fork.id)
        for j in range(eat_time):
            # They're Python philosophers, so they eat spam rather than spaghetti
            print(name, 'eating spam')
            yield
        print(name, 'releasing forks', left_fork.id, 'and', right_fork.id)
        left_fork.release()
        right_fork.release()
    print(name, 'leaving the table')



def ex_2():
    forks = [Utensil(i) for i in range(3)]
    schedule(philosopher("Plato", 7, 2, 3, forks[0], forks[1]))
    schedule(philosopher("Socrates", 8, 3, 1, forks[1], forks[2]))
    schedule(philosopher("Euclid", 5, 1, 4, forks[2], forks[0]))
    run()



# Example 3
def run2():
    while 1:
        run()
        if not wait_for_event():
            return

class FdQueues:
    def __init__(self):
        self.readq = []
        self.writeq = []

fd_queues = {}

def get_fd_queues(fd):
    q = fd_queues.get(fd)
    if not q:
        q = FdQueues()
        fd_queues[fd] = q
    return q

def block_for_reading(fd):
    block(get_fd_queues(fd).readq)

def block_for_writing(fd):
    block(get_fd_queues(fd).writeq)

def close_fd(fd):
    if fd in fd_queues:
        del fd_queues[fd]
    fd.close()

def wait_for_event():
    from select import select
    read_fds = []
    write_fds = []
    for fd, q in fd_queues.iteritems():
        if q.readq:
            read_fds.append(fd)
        if q.writeq:
            write_fds.append(fd)
    if not (read_fds or write_fds):
        return False
    read_fds, write_fds, _ = select(read_fds, write_fds, [])
    for fd in read_fds:
        unblock(fd_queues[fd].readq)
    for fd in write_fds:
        unblock(fd_queues[fd].writeq)
    return True

def loop():
    while 1:
        print('Waiting for input')
        block_for_reading(stdin)
        yield
        print('input is ready')
        line = stdin.readline()
        print('Input was:', repr(line))
        if not line:
            break

def ex_3():
    schedule(loop())
    run2()

if __name__ == "__main__":
    #ex_1()
    #ex_2()
    ex_3()