#Example A-6. taxi_sim.py: the taxi fleet simulator
import random
import collections
import queue
import argparse
import time

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERVAL = 5

Event = collections.namedtuple('Event', 'time proc action')

# BEGIN TAXI_PROCESS
def taxi_process(ident, trips, start_time=0): 
    """Yield to simulator issuing event at each state change"""
    time = yield Event(start_time, ident, 'leave garage')

    for i in range(trips):
        time = yield Event(time, ident, 'pick up passenger')
        time = yield Event(time, ident, 'drop off passenger')

    # 最后一个Yield中没有赋值给time是因为这个time没有意义了，该
    # process已经结束，后续simulator不会再有这个Process的time了
    yield Event(time, ident, 'going home')
    # end of taxi process ---># !!!When the coroutine falls off the end, the generator object raises StopIteration.
# END TAXI_PROCESS


# BEGIN TAXI_SIMULATOR
class Simulator:

    def __init__(self, procs_map):
        # PriorityQueue是一个根据item[0](这里是time值)的大小来自动排序的队列
        self.events = queue.PriorityQueue()

        # 这里根据procs_map重新build一个dict，相当于做了copy，因为在运行中self.procs
        # 的值会改变（删除），而作者不想改变用户传递进来的值，即Main中的taxis
        self.procs = dict(procs_map)

    def run(self, end_time):
        """Schedule and display events until time is up"""
        # schedule the first event for each cab
        for _, proc in sorted(self.procs.items()):
            first_event = next(proc)
            self.events.put(first_event)
        
        # main loop of the simulation
        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():
                print('*** end of events***')
                break

            current_event = self.events.get()
            sim_time, proc_id, previous_action = current_event
            print('taxi:', proc_id, proc_id * ' ', current_event)
            active_proc = self.procs[proc_id]
            next_time = sim_time + compute_duration(previous_action)
            try:
                next_event = active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)
        else:
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))
# END TAXI_SIMULATOR
    
def compute_duration(previous_action):
    """Compute action duration using exponential distribution"""
    if previous_action in ['leave garage', 'drop off passenger']:
        # new state is prowling
        interval = SEARCH_DURATION
    elif previous_action == 'pick up passenger':
        # new state is trip
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('Unknown previous_action: %s' % previous_action)
    return int(random.expovariate(1/interval)) + 1


def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS,
         seed=None):
    """Initialize random generator, build procs and run simulation"""
    if seed is not None:
        random.seed(seed) # get reproducible results
    taxis = {i: taxi_process(i, (i+1)*2, i*DEPARTURE_INTERVAL)
             for i in range(num_taxis)}
    sim = Simulator(taxis)
    sim.run(end_time)


if __name__ == "__main__":
    taxi = taxi_process(ident=13, trips=2, start_time=0)
    print(next(taxi))
    print(taxi.send(7))
    print(taxi.send(30))
    print(taxi.send(35))
    print(taxi.send(83))
    print(taxi.send(84))
    print(taxi.send(94)) # 上一个已经触发了going home, 这个send直接触发raise stopiteration
    '''
    Output
        Event(time=0, proc=13, action='leave garage')
        Event(time=7, proc=13, action='pick up passenger')
        Event(time=30, proc=13, action='drop off passenger')
        Event(time=35, proc=13, action='pick up passenger')
        Event(time=83, proc=13, action='drop off passenger')
        Event(time=84, proc=13, action='going home')
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        StopIteration
    '''

    '''
    parser = argparse.ArgumentParser(
                        description='Taxi fleet simulator.')
    parser.add_argument('-e', '--end-time', type=int,
                        default=DEFAULT_END_TIME,
                        help='simulation end time; default = %s'
                        % DEFAULT_END_TIME)
    parser.add_argument('-t', '--taxis', type=int,
                        default=DEFAULT_NUMBER_OF_TAXIS,
                        help='number of taxis running; default = %s'
                        % DEFAULT_NUMBER_OF_TAXIS)
    parser.add_argument('-s', '--send', type=int, default=None,
                        help='random generator seed (for testing)')
    args = parser.parse_args()
    main(args.end_time, args.taxis, args.send)
    '''