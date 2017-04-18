import pickle
from Page import Page

with open("memconfig.txt") as a:
    max_pages = a.read()

command_list = []
with open("commands.txt") as a:
    c_list = a.readlines()[0:]
    for ind, com in enumerate(c_list):
        sub_commands = com.split(" ")
        command_list.append(sub_commands)


class VMM:
    def __init__(self):
        self.max_memory = int(max_pages)
        self.main_memory = []  #list of Pages
        for i in range(self.max_memory):
            page = Page()
            self.main_memory.append(page)
        self.disk_memory = "vm.txt"
        self.command_list = command_list

    def store(self, variable_id, value):
        boolean, index = any_i(page.var_id == '' for page in self.main_memory)
        if boolean:
            self.main_memory[index].var_id = variable_id
            self.main_memory[index].var_value = value
            self.main_memory[index].was_used()
        else:
            with open(self.disk_memory, 'a') as the_file:
                the_file.write(str(variable_id) + " " + value)
        # self.main_memory.append(zip(variable_id, value))
        # with open(self.disk_memory, 'w') as f:
        #     pickle.dump(self.main_memory, f)

    def release(self, variable_id):
        boolean, index = any_i(page.var_id == variable_id for page in self.main_memory)
        if boolean:
            self.main_memory.pop(index)
        with open(self.disk_memory) as disk:
            var_list = disk.readlines()[0:]
            for ind, var in enumerate(var_list):
                var_lines = var.split(" ")
                var_list.append(var_lines)       # probably wrong NEED TO FIX


    def lookup(self, variable_id):
        with open(self.disk_memory, 'r') as f:
            for variable in pickle.load(f):
                if variable is variable_id:
                    print variable

    def update_age_counters(self):
        for page in self.main_memory:
            page.update_age_counter()


def any_i(iterable):
    for i, element in enumerate(iterable):
        if element:
            return [True, i]
    return [False, '']
