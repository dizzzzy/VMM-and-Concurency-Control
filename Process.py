from math import ceil
import threading


class Process(threading.Thread):
    def __init__(self, pid, arrival_time, burst_time, priority, name):
        super(Process, self).__init__()
        self.pid = pid
        self.original_burst_time = (float(burst_time) / 1000)
        self.arrival_time = (float(arrival_time) / 1000)
        self.burst_time = (float(burst_time) / 1000)
        self.priority = priority if 1 < priority < 140 else exit()
        self.name = name
        self.has_started = False
        self.iteration = 0
        self.waiting_time = 0
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())

    def get_arrival_time(self):
        return self.arrival_time

    def get_burst_time(self):
        return self.burst_time

    def update_burst_time(self, time, endTime):
        self.burst_time -= time
        # if self.burst_time <= 0:
        #     print self.name + " has finished running at " + str(endTime)

    def get_timeslot(self):
        if self.priority < 100:
            time_slot = float((140 - self.priority) * 0.02)  # In Milliseconds
        else:
            time_slot = float((140 - self.priority) * 0.005)  # In Milliseconds
        return time_slot

    def update_priority(self, time_now):
        self.waiting_time = (time_now - self.arrival_time) - (self.original_burst_time - self.burst_time)
        bonus = ceil(10 * self.waiting_time / (time_now - self.arrival_time))
        self.priority = max(100, min(self.get_priority() - bonus + 5, 139))

    def get_priority(self):
        return self.priority

    def get_pid(self):
        return self.pid

    def get_name(self):
        return self.name

    def get_process_from_pid(self, pid):
        return self if self.pid == pid else None

    def pause(self, pauseTime, bool):
        if bool == 0:
            self.paused = True
            self.pause_cond.release()
            print self.name + " process has paused at " + str(pauseTime)
        else:
            print self.name + " process has terminated at " + str(pauseTime)

    def resume(self, resumeTime):
        self.paused = False
        self.pause_cond.acquire()
        if self.get_timeslot() >= self.burst_time:
            print self.name + " process has resumed at " + str(resumeTime) + ". Granted " + str(self.burst_time)
        else:
            print self.name + " process has resumed at " + str(resumeTime) + ". Granted " + str(self.get_timeslot())

    def start(self, startTime):
        self.pause_cond.acquire()
        print self.name + " process has started at " + str(startTime)
        super(Process, self).start()
        self.has_started = True
        self.pause_cond.release()