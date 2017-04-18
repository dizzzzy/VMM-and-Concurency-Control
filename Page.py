import numpy as np
import threading


class Page:
    def __init__(self):
        self.var_id = ''
        self.var_value = 0
        self.was_used = False
        self.aging_counter = 0
        self.lock = threading.Lock()

    def update_age_counter(self):
        self.lock.acquire()
        np.right_shift(np.uint8(self.aging_counter), 1)
        if self.was_used:
            self.aging_counter += 128
            self.was_used = False
        self.lock.release()

    def was_used(self):
        self.lock.acquire()
        self.was_used = True
        self.lock.release()