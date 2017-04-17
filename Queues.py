class Q:
    """
        Queue functionality:
        1. Automatically sorts the processes in the queue based on priority
    """
    def __init__(self):
        self.items = []

    def get_item(self, key):
        return self.items[key]

    def is_empty(self):
        return self.items == []

    def enqueue_process(self, item):
        return self.items.append(item)

    def de_queue(self, item):
        return self.items.remove(item)

    def pop(self):
        self.items.pop(0)
        # if len(self.items) == 1:
        #     self.items = []
        # else:
        #     self.items = self.items[1:]

    def size(self):
        return len(self.items)

    def get_pid(self, pid):
        return self.items.__getitem__(pid)

    def get_all_process(self):
        return self.items

