import pickle

with open("memconfig.txt") as a:
    max_pages = a.read()


class VMM:
    def __init__(self):
        self.variable_list = []
        self.max_memory = int(max_pages)

    def store(self, variable_id, value):
        self.variable_list.append(zip(variable_id, value))
        with open("vm.txt", 'w') as f:
            pickle.dump(self.variable_list, f)

    def release(self, variable_id):
        return self.variable_list.remove(variable_id)

    def lookup(self, variable_id):
        with open("vm.txt", 'r') as f:
            for variable in pickle.load(f):
                if variable is variable_id:
                    print variable
