import threading
from Process import Process
from Queues import Q

from timeit import default_timer

p_list = []
with open("input.txt") as f:
    process_list = f.readlines()[2:]
    for ind, proc in enumerate(process_list):
        process_sub_items = proc.split(" ")
        p_list.append(Process(int(ind + 1), process_sub_items[1], process_sub_items[2], int(process_sub_items[3]),
                              process_sub_items[0]))

with open("threadconfig.txt") as f:
    thread_num = f.readline()

Q1 = Q()


class SchedulerThread(threading.Thread):
    """
        Main Scheduler thread: Priority based scheduler
        1. Can pause/resume processes - Done
        2. Switch between the active and expired queue - Done
        3. Updates the priority of the processes if they run twice
        4. Give time slots to the processes
        Each process is responsible to keep track of its total execution and inform the scheduler thread when it is
        finished. This process continues until all processes are done.
        Active/Expired Queue will contain the PID's of the processes.
    """

    def __init__(self):
        super(SchedulerThread, self).__init__()
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.start_time = 0
        self.process_list = p_list
        # At starting, Q1 is active queue and Q2 is expired queue
        self.expired_queue = Q1
        self.cores = []
        self.cores_isempty_flag = []
        self.core_len = int(thread_num)
        self.process_length = len(p_list)
        self.terminated_processes = 0
        self.arrived_processes = 0
        self.flag = True
        self.arrival_lock = threading.Lock()

    def swap(self, core_index):
        self.arrival_lock.acquire()
        self.expired_queue.items.sort(key=lambda process: process.priority)
        for x, item in enumerate(self.expired_queue.items):
            if x == 0:
                item.iteration += 1
            else:
                item.iteration = 0
        self.cores[core_index].items.append(self.expired_queue.get_item(0))
        self.expired_queue.pop()
        self.arrival_lock.release()
        # print "active queue: " + str(self.active_queue.items)
        # print "expired queue: " + str(self.expired_queue.items)

    def run_core(self, num):
        while self.flag:
            while len(self.cores[num].items) != 0:
                if self.cores[num].get_item(0).has_started:
                    self.cores[num].get_item(0).resume(default_timer() - self.start_time)
                else:
                    self.cores[num].get_item(0).has_started = True
                    self.cores[num].get_item(0).start(default_timer() - self.start_time)
                process_start_time = default_timer() - self.start_time
                process_end_time = process_start_time + self.cores[num].get_item(0).get_timeslot()
                going_to_finish = False
                if self.cores[num].get_item(0).get_timeslot() >= self.cores[num].get_item(0).get_burst_time():
                    process_end_time = process_start_time + self.cores[num].get_item(0).get_burst_time()
                    going_to_finish = True
                while (default_timer() - self.start_time) < process_end_time:
                    i = 0  # <--- erase     NITESH HANDLE THE SWAPS AND THE RANDOM ACTIONS IN HERE
                self.cores[num].get_item(0).pause(default_timer() - self.start_time,
                                                       going_to_finish)  # pause current process
                if going_to_finish:
                    self.cores[num].get_item(0).update_burst_time(
                        self.cores[num].get_item(0).get_burst_time(),
                        (default_timer() - self.start_time))  # updates burst time
                    self.terminated_processes += 1
                    self.cores[num].pop()  # pops the first element in the queue
                    self.cores_isempty_flag[num] = True
                    if self.terminated_processes == self.process_length:
                        self.flag = False
                else:
                    self.cores[num].get_item(0).update_burst_time(self.cores[num].get_item(0).get_timeslot(),
                                                         (default_timer() - self.start_time))  # updates burst time
                    if self.cores[num].items[0].iteration == 2:
                        self.cores[num].items[0].iteration = 0
                        self.cores[num].items[0].update_priority(default_timer() - self.start_time)
                    self.expired_queue.enqueue_process(self.cores[num].get_item(0))  # add process into expired queue
                    self.cores[num].pop()  # pop process
                    self.cores_isempty_flag[num] = True

    def arrival_check(self):
        while self.arrived_processes != self.process_length:
            for process in p_list:
                if process.get_arrival_time() < (default_timer() - self.start_time) and not process.has_arrived:
                    # check if process has higher priority than running process
                    process.has_arrived = True
                    self.arrival_lock.acquire()
                    print process.name + " arrived at " + str(default_timer() - self.start_time)
                    self.expired_queue.enqueue_process(process)
                    self.arrived_processes += 1
                    self.arrival_lock.release()

    def run(self):
        self.start_time = default_timer()
        t = threading.Thread(target=self.arrival_check)
        t.start()
        for num in range(self.core_len):
            q_dynamic = Q()
            variable_thread = threading.Thread(target=self.run_core, args=[num])
            self.cores.append(q_dynamic)
            self.cores_isempty_flag.append(True)
            variable_thread.start()
        while self.flag:
            if int((default_timer() - self.start_time) > 1):  # Start at time 1 second
                count = 0
                while self.terminated_processes != self.process_length:
                    if not self.expired_queue.is_empty():
                        boolean, index = any_i(self.cores_isempty_flag)
                        if boolean:       # while any cores are empty
                            count += 1
                            self.cores_isempty_flag[index] = False
                            self.swap(index)



def any_e(iterable):
    for element in iterable:
        if element:
            return [True, element]
    return [False, '']


def any_i(iterable):
    for i, element in enumerate(iterable):
        if element:
            return [True, i]
    return [False, '']