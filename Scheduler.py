import threading

from Process import Process
from Queues import Q

from timeit import default_timer

p_list = []
with open("input.txt") as f:
    process_list = f.readlines()[2:]
    for index, proc in enumerate(process_list):
        process_sub_items = proc.split(" ")
        p_list.append(Process(int(index + 1), process_sub_items[1], process_sub_items[2], int(process_sub_items[3]),
                              process_sub_items[0]))
Q1 = Q(len(p_list))
Q2 = Q(len(p_list))


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
        self.start_time = default_timer()

        self.process_list = p_list
        self.active_queue = Q1  # At starting, Q1 is active queue and Q2 is expired queue
        self.expired_queue = Q2

    def swap(self):
        if len(self.active_queue.items) == 0 and len(self.expired_queue.items) != 0:  # swaps queues
            self.expired_queue.items.sort(key=lambda process: process.priority)
            self.active_queue.items, self.expired_queue.items = self.expired_queue.items, self.active_queue.items
            print "active queue: " + str(self.active_queue.items)
            print "expired queue: " + str(self.expired_queue.items)

    def run(self):
        process_length = len(p_list)
        flag = True
        terminated_processes = 0
        start_time = default_timer()
        while True and flag:
            if int((default_timer() - start_time) > 1):  # Start at time 1 second
                for i in range(0, process_length):
                    if p_list[i].get_arrival_time() < (default_timer() - start_time) and not p_list[i].has_started:
                        # send process in expired queue
                        self.expired_queue.enqueue_process(p_list[i])
                        p_list[i].has_started = True
                        print p_list[i].name + " arrived at " + str(default_timer() - start_time)
                self.swap()

                while len(self.active_queue.items) != 0:
                    if self.active_queue.getItem(0).get_burst_time() > 0:
                        # print self.active_queue.getItem(0).process.get_burst_time()
                        if self.active_queue.getItem(0).has_started:
                            for x in range(0, len(self.active_queue.items)):
                                if x == 0:
                                    self.active_queue.items[0].iteration += 1
                                else:
                                    self.active_queue.items[x].iteration = 0
                            self.active_queue.getItem(0).resume(default_timer() - start_time)
                        else:
                            for x in range(0, len(self.active_queue.items)):
                                if x == 0:
                                    self.active_queue.items[0].iteration += 1
                                else:
                                    self.active_queue.items[x].iteration = 0
                            self.active_queue.getItem(0).start(default_timer() - start_time)
                        process_start_time = default_timer() - start_time
                        process_end_time = process_start_time + self.active_queue.getItem(0).get_timeslot()
                        going_to_finish = False
                        if self.active_queue.getItem(0).get_timeslot() >= self.active_queue.getItem(0).get_burst_time():
                            process_end_time = process_start_time + self.active_queue.getItem(0).get_burst_time()
                            going_to_finish = True
                        i = 0
                        while (default_timer() - start_time) < process_end_time:
                            if p_list[i].get_arrival_time() < (default_timer() - start_time) and not p_list[
                                i].has_started:
                                # check if process has higher priority than running process
                                p_list[i].has_started = True
                                print p_list[i].name + " arrived at " + str(default_timer() - start_time)
                                self.expired_queue.enqueue_process(p_list[i])
                            i = (i + 1) % process_length
                        if going_to_finish:
                            self.active_queue.getItem(0).pause(default_timer() - start_time,
                                                               going_to_finish)  # pause current process
                            self.active_queue.getItem(0).update_burst_time(
                                self.active_queue.getItem(0).get_burst_time(),
                                (default_timer() - start_time))  # updates burst time
                            terminated_processes += 1
                            self.active_queue.pop()  # pops the first element in the queue
                            if terminated_processes == process_length:
                                flag = False
                        else:
                            self.active_queue.getItem(0).pause(default_timer() - start_time,
                                                               going_to_finish)  # pause current process
                            self.active_queue.getItem(0).update_burst_time(self.active_queue.getItem(0).get_timeslot(),
                                                                           (
                                                                           default_timer() - start_time))  # updates burst time
                            if self.active_queue.items[0].iteration == 2:
                                self.active_queue.items[0].iteration = 0
                                self.active_queue.items[0].update_priority(default_timer())
                            self.expired_queue.enqueue_process(
                                self.active_queue.getItem(0))  # adds the process into expired queue
                            self.active_queue.pop()  # pops the first element in the queue
